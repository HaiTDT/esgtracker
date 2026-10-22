"""Independent field/record scoring and OCR edit distance. Never manufactures gold."""
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
import unicodedata

from src.quality.records import FIELDS, required_fields
from rapidfuzz.distance import Levenshtein


def location(row):
    return row['source_sha256'], row['physical_page'], row['anchor'], row['record_type']


def edit_distance(a,b):
    return Levenshtein.distance(a,b)


def ocr_errors(reference, prediction):
    # NFC only, not accent stripping/case folding: Vietnamese OCR errors count.
    reference=unicodedata.normalize('NFC',reference)
    prediction=unicodedata.normalize('NFC',prediction)
    chars=edit_distance(reference,prediction)
    words=edit_distance(reference.split(),prediction.split())
    return {'character_edits':chars,'reference_characters':len(reference),
            'word_edits':words,'reference_words':len(reference.split()),
            'cer':chars/len(reference) if reference else None,
            'wer':words/len(reference.split()) if reference.split() else None}


def equal(field,a,b):
    if field=='value' and a is not None and b is not None:
        try:
            return not isinstance(a,bool) and not isinstance(b,bool) and Decimal(str(a))==Decimal(str(b))
        except InvalidOperation:
            return False
    return type(a)==type(b) and a==b


def prf(tp,fp,fn):
    return {'tp':tp,'fp':fp,'fn':fn,'precision':tp/(tp+fp) if tp+fp else None,
            'recall':tp/(tp+fn) if tp+fn else None,'f1':2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else None}


def make_template(predictions, split='test'):
    units=[]
    grouped=defaultdict(list)
    for row in predictions:
        if row.get('source_sha256') and row.get('physical_page') and row.get('anchor'):
            grouped[(row['source_sha256'],row['physical_page'])].append(row)
    for (source,page),rows in sorted(grouped.items()):
        units.append({'source_sha256':source,'physical_page':page,'split':split,'annotator':None,
                      'reviewed_against_pdf':False,'fully_annotated':False,
                      'record_types':sorted({r['record_type'] for r in rows}),
                      'items':[{'anchor':r['anchor'],'record_type':r['record_type'],
                                'expected':{},'reviewed_fields':[], 'suggested_prediction':r['fields'],
                                'suggested_record_id':r['record_id']} for r in rows],
                      'ocr_reference':None})
    return {'schema_version':'esg-quality-gold/1.0','annotation_status':'draft',
            'instructions':'Human must inspect PDF, add omitted items, remove false candidates and fill expected fields. Suggested predictions are not gold. Use fully_annotated only after checking every record in the declared page/type scope.',
            'evaluation_units':units,'prediction_versions':None,'development_source_sha256':[]}


def evaluate(predictions,gold,*,split='test',development_sources=(),ocr_predictions=()):
    if gold.get('schema_version')!='esg-quality-gold/1.0':
        raise ValueError('Unsupported gold schema.')
    units=[u for u in gold['evaluation_units'] if u['split']==split]
    if not units:
        raise ValueError('Không có evaluation unit trong split được chọn.')
    development=set(development_sources)|set(gold.get('development_source_sha256',[]))
    development|={u['source_sha256'] for u in gold['evaluation_units'] if u['split'] in ('train','dev')}
    if split=='test' and development & {u['source_sha256'] for u in units}:
        raise ValueError('Train/dev/test leakage: cùng PDF xuất hiện ở development và test.')
    if gold.get('annotation_status')!='human_reviewed':
        raise ValueError('Chưa có gold human_reviewed; template không được dùng để công bố precision.')
    field_stats={f:Counter() for f in FIELDS}
    tp=fp=fn=0
    errors=[]
    seen_units=set()
    seen_gold=set()
    ocr=[]
    ocr_by_page={(r['source_sha256'],r['physical_page']):r['text'] for r in ocr_predictions}
    breakdown=defaultdict(Counter)
    for unit in units:
        if unit.get('reviewed_against_pdf') is not True or not (unit.get('annotator') or '').strip():
            raise ValueError('Evaluation unit thiếu xác nhận PDF hoặc annotator.')
        types=unit.get('record_types',[])
        if not types or not isinstance(unit.get('fully_annotated'),bool):
            raise ValueError('Phải khai báo phạm vi loại record và fully_annotated.')
        for kind in types:
            key=(unit['source_sha256'],unit['physical_page'],kind)
            if key in seen_units:
                raise ValueError('Evaluation units có phạm vi trùng nhau.')
            seen_units.add(key)
        items=[]
        for item in unit['items']:
            row={**item,'source_sha256':unit['source_sha256'],'physical_page':unit['physical_page']}
            fields=item.get('expected',{})
            if item['record_type'] not in types or not item.get('anchor') or set(fields)-set(FIELDS):
                raise ValueError('Gold item không thuộc scope/field hợp lệ.')
            needed=set(required_fields(item))
            if not needed <= set(fields) or not set(fields) <= set(item.get('reviewed_fields',[])):
                raise ValueError('Gold chưa gán đủ field bắt buộc hoặc chưa xác nhận các field expected.')
            if location(row) in seen_gold:
                raise ValueError('Gold có locator trùng nhau; cần anchor phân biệt.')
            seen_gold.add(location(row))
            items.append(row)
        anchors={location(r) for r in items}
        predicted=[r for r in predictions if r['source_sha256']==unit['source_sha256'] and r['physical_page']==unit['physical_page'] and r['record_type'] in types
                   and (unit['fully_annotated'] or location(r) in anchors)]
        by_location=defaultdict(list)
        for r in predicted:
            by_location[location(r)].append(r)
        unit_tp=unit_fp=unit_fn=0
        for expected in items:
            found=by_location.get(location(expected),[])
            prediction=found.pop(0) if found else None
            differences=[]
            for field,value in expected['expected'].items():
                stats=field_stats[field]
                stats['support']+=1
                if prediction is not None and equal(field,value,prediction['fields'].get(field)):
                    stats['correct']+=1
                else:
                    differences.append(field)
                    stats['incorrect']+=1
            if prediction is None:
                fn+=1;unit_fn+=1
                errors.append({'kind':'missing_record','gold':location(expected),'fields':differences})
            elif differences:
                fp+=1;fn+=1;unit_fp+=1;unit_fn+=1
                errors.append({'kind':'field_mismatch','record_id':prediction['record_id'],'gold':location(expected),'fields':differences})
            else:
                tp+=1;unit_tp+=1
        for remaining in by_location.values():
            for r in remaining:
                fp+=1;unit_fp+=1
                errors.append({'kind':'extra_or_duplicate_record','record_id':r['record_id']})
        breakdown[unit['source_sha256']].update(tp=unit_tp,fp=unit_fp,fn=unit_fn)
        if unit.get('ocr_reference') is not None:
            prediction_text=ocr_by_page.get((unit['source_sha256'],unit['physical_page']))
            if not isinstance(prediction_text,str):
                raise ValueError('OCR scoring requires separately captured ocr_prediction, not a gold-derived prediction.')
            ocr.append(ocr_errors(unit['ocr_reference'],prediction_text))
    chars=sum(x['reference_characters'] for x in ocr)
    words=sum(x['reference_words'] for x in ocr)
    return {'schema_version':'esg-quality-report/1.0','split':split,'strict_record':prf(tp,fp,fn),
            'field_accuracy':{f:{**dict(s),'accuracy':s['correct']/s['support'] if s['support'] else None} for f,s in field_stats.items()},
            'by_source':{s:prf(c['tp'],c['fp'],c['fn']) for s,c in breakdown.items()},
            'ocr':{'scored_pages':len(ocr),'cer':sum(x['character_edits'] for x in ocr)/chars if chars else None,
                   'wer':sum(x['word_edits'] for x in ocr)/words if words else None},
            'scope':{'evaluation_units':len(units),'fully_annotated_units':sum(u['fully_annotated'] for u in units),
                     'selected_anchor_units':sum(not u['fully_annotated'] for u in units)},
            'errors':errors,'limits':'Strict correctness requires all declared fields. Partial units score selected anchors only, not corpus recall. Gold status/annotator are human declarations, not independently verified identities. No greenwashing verdict.'}
