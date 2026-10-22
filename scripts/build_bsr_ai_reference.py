"""Assemble an auditable AI transcription sidecar, NEVER a human gold benchmark.

Curated values live in a separate seed file authored after visual PDF review.
Predictions are read only AFTER reference creation to attach old IDs/pointers.
No production record, source PDF, human annotation or approval is modified.
"""
import argparse
from collections import Counter
from copy import deepcopy
from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path
import re
import sys
import unicodedata

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.extraction.source_v2 import atomic_json
from src.quality.records import FIELDS
from src.quality.evaluation import equal

STATUS = 'AI_reviewed_pending_human_review'
UNKNOWN = 'Chưa xác nhận trong phạm vi các trang đã rà; không khẳng định toàn báo cáo không công bố.'


def normal_text(text):
    return ' '.join(unicodedata.normalize('NFC', text).split())


def number(raw, unit, ambiguity=None):
    if ambiguity in ('ambiguous_separator', 'categorical'):
        return None, unit, None
    s = raw.replace(' ', '').replace('%đạtQCVN', '').replace('%', '')
    multiplier = Decimal(1)
    if s.endswith('triệu'):
        s = s[:-5]
        multiplier = Decimal(1000000)
    s = s.replace('.', '').replace(',', '.')
    value = Decimal(s)
    units = {'Người': ('people', 1), 'người': ('attendances', 1), 'Chương trình': ('programs', 1),
             'Tỷ đồng': ('VND', 1000000000), 'tỷ đồng': ('VND', 1000000000),
             'triệu USD': ('USD', 1000000), 'tấn': ('t', 1), 'm³': ('m3', 1),
             'm³/ngày': ('m3/day', 1), 'm³/h': ('m3/hour', 1), 'm3/h': ('m3/hour', 1),
             'kwh': ('kWh', 1), 'giờ': ('hours', 1), 'vụ': ('count', 1)}
    normalized_unit, scale = units.get(unit, (unit, 1))
    multiplier *= Decimal(scale)
    value *= multiplier
    value = int(value) if value == value.to_integral_value() else float(value)
    return value, normalized_unit, str(multiplier)


def make_reference(source, page, label, raw, unit, column, box, *, table, year=None,
                   concept=None, expected_extra=None, notes=None, ambiguity=None, quote=None):
    value, normalized_unit, scale = number(raw, unit, ambiguity)
    locator = f'pdf:p{page}:{table}:{label}:{column}'
    expected = {field: None for field in FIELDS}
    expected.update(value=value, unit=normalized_unit, observation_year=year, text=raw)
    expected.update(expected_extra or {})
    reasons = {field: UNKNOWN for field, v in expected.items() if v is None}
    if ambiguity == 'ambiguous_separator':
        reasons['value'] = 'PDF in 3.319 nhưng chưa chốt dấu chấm là thập phân hay phân nhóm; không suy bằng phép chia sản lượng.'
    elif ambiguity == 'categorical':
        reasons['value'] = 'Giá trị phân loại BB+, không phải số.'
    evidence = {'source_sha256': source, 'physical_page': page, 'anchor': locator,
                'bbox_normalized_xyxy': box, 'quote': quote or raw,
                'quote_origin': 'AI_visual_transcription',
                'table_context': {'table': table, 'row_label': label, 'column_label': column,
                                  'cell_text': raw, 'unit_text': unit}}
    boundary = {k: expected[k] for k in ('reporting_entity', 'consolidation', 'scope', 'counting_method', 'calculation_method')}
    boundary.update(included_entities=None, excluded_entities=None, consolidation_method=None)
    boundary['missing_fields'] = sorted(k for k, v in boundary.items() if v is None)
    return {'reference_id': 'ai_ref_'+sha256(f'{source}:{locator}'.encode()).hexdigest(),
            'annotation_status': STATUS, 'review_status': 'pending_human_review', 'is_gold': False,
            'source_sha256': source, 'physical_page': page, 'source_locator': locator,
            'record_kind': 'measurement', 'expected': expected,
            'reviewed_fields': sorted(k for k, v in expected.items() if v is not None),
            'unknown_reasons': reasons,
            'field_evidence': {k: [deepcopy(evidence)] for k, v in expected.items() if v is not None},
            'raw_transcription': evidence['table_context'], 'normalization': {'scale_factor': scale, 'value_ambiguous': value is None},
            'boundary': boundary,
            'missing_fields': sorted(['expected.'+k for k, v in expected.items() if v is None] +
                                     ['boundary.'+k for k in boundary['missing_fields']]),
            'standards_annotation': {'candidate_concept_id': concept, 'status': 'AI_proposed_not_domain_validated',
                                     'equivalence_verified': False, 'sasb_protocol_status': 'pending'},
            'evidence': [evidence], 'notes': notes or [], 'extract_record_bindings': [],
            'link_hint': {'label': label, 'year': year}}


def build_references(seeds, pages):
    refs = []
    source_map = {alias: next(p['source_sha256'] for p in pages if p['source_sha256'].startswith(info['prefix']))
                  for alias, info in seeds['sources'].items()}
    page_map = {(p['source_sha256'], p['physical_page']): p for p in pages}
    for alias, values in seeds['financial'].items():
        info, source = seeds['sources'][alias], source_map[alias]
        entity = 'Công ty Cổ phần Lọc hóa dầu Bình Sơn'
        declared_scope = 'Công ty' if info['scope']=='Separate' else 'Công ty và công ty con'
        for col, raw in enumerate(values['employee_values']):
            year = info['year'] - col
            ref = make_reference(source, info['employees_page'], 'Tổng số nhân viên', raw, 'Người',
                f'tại ngày 31 tháng 12 năm {year}', values['employee_box'], table='Thuyết minh 1 - Thông tin khái quát',
                year=year, concept='employee_count', quote=values['employee_quote'],
                expected_extra={'metric_id': 'local:employee_headcount_at_date:v1', 'measurement_date': f'{year}-12-31',
                    'period_type': 'at_date', 'reporting_entity': entity, 'consolidation': info['scope'], 'scope': declared_scope},
                notes=['Số nhân viên được nêu trực tiếp; headcount/FTE và danh sách từng pháp nhân vẫn chưa xác nhận.'])
            refs.append(ref)
        for kind, metric, label, concept in (
            ('payables', 'employee_payables', 'Phải trả người lao động', 'financial_employee_payables'),
            ('advances', 'employee_advances', 'Tạm ứng cho nhân viên', 'financial_employee_advances')):
            if kind not in values:
                continue
            page = info['balance_page'] if kind=='payables' else info['advances_page']
            for col, raw in enumerate(values[kind]):
                # Read the opening column as printed. Do not assert a 31/12 date
                # for it without further period/adjustment evidence.
                known = {'metric_id': f'local:{metric}:v1', 'period_type': 'at_date',
                         'reporting_entity': entity, 'consolidation': info['scope'],
                         'scope': 'Báo cáo tài chính riêng' if info['scope']=='Separate' else 'Báo cáo tài chính hợp nhất'}
                if col==0:
                    known['measurement_date'] = f"{info['year']}-12-31"
                ref = make_reference(source, page, label, raw, 'VND', 'Số cuối năm' if col==0 else 'Số đầu năm',
                    values[kind+'_box'], table='Bảng cân đối kế toán' if kind=='payables' else 'Thuyết minh - Phải thu khác',
                    year=info['year'] if col==0 else None, concept=concept, expected_extra=known,
                    notes=['Khoản tiền, không phải số người. Đơn vị VND đọc từ đầu bảng/cột.'] +
                          (['Số đầu năm giữ nguyên nhãn cột; ngày đo/năm quan sát chưa chốt trong lượt rà này.'] if col else []))
                ref['link_hint'].update(metric_id=f'local:{metric}:v1', year=info['year']-col)
                ref['year_basis'] = 'closing_balance' if col==0 else 'opening_balance_date_not_yet_adjudicated'
                ref['evidence'].append({'source_sha256': source, 'physical_page': page,
                    'anchor': f'pdf:p{page}:table_headers', 'bbox_normalized_xyxy': [0.14, 0.05, 0.95, 0.23] if kind=='payables' else [0.14, 0.06, 0.95, 0.20],
                    'quote': 'Đơn vị: VND' if kind=='payables' else 'Số cuối năm | Số đầu năm | VND | VND',
                    'quote_origin': 'AI_visual_transcription_of_header_cells',
                    'note': 'Dấu | phân tách các ô tiêu đề độc lập, không phải câu nguyên văn liên tục.'})
                ref['field_evidence']['unit'].append(deepcopy(ref['evidence'][-1]))
                ref['field_evidence']['period_type'].append(deepcopy(ref['evidence'][-1]))
                refs.append(ref)
    source = source_map['esg2025']
    workforce = seeds['esg2025_workforce']
    for row in workforce['rows']:
        for year, raw in zip(workforce['years'], row['values']):
            col = workforce['years'].index(year)
            extra = {}
            if row['label']=='Tổng số lao động': extra['metric_id']='local:employee_headcount_at_date:v1'
            ref = make_reference(source, workforce['page'], row['label'], raw, row['unit'], str(year),
                [0.145, row['y'][0], 0.44, row['y'][1]], table='Quy mô lao động và ổn định nhân sự', year=year,
                concept=row['concept'], expected_extra=extra,
                notes=['Không gán ngày 31/12, headcount/FTE hoặc phạm vi riêng/hợp nhất nếu bảng chưa nêu.'])
            ref['population'] = row.get('population')
            refs.append(ref)
    chart = seeds['esg2024_chart']
    for series in chart['series']:
        for year, raw in zip(chart['years'], series['values']):
            ref = make_reference(source_map['esg2024'], chart['page'], series['label'], raw, 'Người', str(year),
                series['box'], table=chart['title'], year=year,
                notes=['Chép nhãn số trên cột và nối năm bằng chú giải màu, không đo chiều cao cột để suy số.'])
            ref['evidence'][0]['chart_context'] = {'series':series['label'],'year':year,
                'legend_color':{2022:'xanh đậm',2023:'xanh lá',2024:'xanh nhạt'}[year]}
            refs.append(ref)
    appendix = seeds['esg2025_appendix']
    for side in ('left', 'right'):
        for index, row in enumerate(appendix[side+'_rows']):
            label, unit, raw, concept = row[:4]
            if side=='left':
                y = 0.213 + index*0.0269
                box = [0.13, y-0.012, 0.44, y+0.013]
                ambiguity = row[4] if len(row)>4 else None
            else:
                box = [0.70, row[4]-0.012, 0.95, row[4]+0.013]
                ambiguity = row[5] if len(row)>5 else None
            ref = make_reference(source, appendix['page'], label, raw, unit, '2025', box,
                table=appendix[side+'_table_title'], year=2025, concept=concept, ambiguity=ambiguity,
                notes=[ambiguity] if ambiguity else [])
            if ambiguity=='hse_subset_not_all_training':
                ref['expected']['unit'] = 'hours/person/year'
                ref['field_evidence']['unit'][0]['note'] = 'Mẫu số người/năm nằm trong tên hàng; ĐVT riêng chỉ ghi giờ.'
            if side=='right' and label=='Tổng năng lượng tiêu thụ trong tổ chức':
                ref['expected']['scope'] = 'trong tổ chức'
                ref['unknown_reasons'].pop('scope')
                ref['reviewed_fields'].append('scope')
                ref['field_evidence']['scope'] = deepcopy(ref['field_evidence']['text'])
            ref['link_hint']['table_index'] = 0 if side=='left' else 1
            # PDF text is independent of the extractor. Require literal cell
            # text in the PDF text layer, allowing layout whitespace only.
            source_text = normal_text(page_map[(source, appendix['page'])]['embedded_text'])
            if normal_text(raw) not in source_text:
                raise ValueError(f'Curated cell not found in PDF text layer: {raw}')
            refs.append(ref)
    for seed in seeds['narratives']:
        source = source_map[seed['source']]
        text = normal_text(page_map[(source, seed['page'])]['embedded_text'])
        if seed.get('exact'):
            quote = seed['exact']
            if normal_text(quote) not in text:
                # Do not synthesize a quote when text extraction has special
                # glyphs or superscripts; use only the visually checked title.
                quote = seed['start']
        else:
            start = text.find(normal_text(seed['start']))
            end = text.find(normal_text(seed['end']), start)
            if start < 0 or end < 0:
                raise ValueError(f'Narrative source segment not found: {seed["start"]}')
            quote = text[start:end+len(normal_text(seed['end']))]
        locator = f'pdf:p{seed["page"]}:paragraph:{seed["start"]}'
        ref = make_reference(source, seed['page'], seed['classification'], '0', 'text', 'narrative',
                             [0, 0, 1, 1], table='Narrative', quote=quote, concept=seed.get('concept'))
        ref['source_locator'] = locator
        ref['reference_id'] = 'ai_ref_'+sha256(f'{source}:{locator}'.encode()).hexdigest()
        ref['record_kind'] = 'narrative'
        ref['expected'] = {field: None for field in FIELDS}
        ref['expected']['text'] = quote
        ref['reviewed_fields'] = ['text']
        ref['unknown_reasons'] = {field: UNKNOWN for field in FIELDS if field!='text'}
        ref['field_evidence'] = {'text': [{**ref['evidence'][0], 'anchor': locator,
                                         'quote': quote, 'quote_origin': 'PDF_text_layer_whitespace_normalized_after_visual_review'}]}
        ref['evidence'] = ref['field_evidence']['text']
        ref['evidence'][0].pop('table_context', None)
        ref['raw_transcription'] = {'verbatim_text_whitespace_normalized': quote}
        ref['normalization'] = None
        ref['classification'] = seed['classification']
        ref['notes'] = [seed['note']]
        ref['link_hint'] = {'narrative_excerpt': quote}
        refs.append(ref)
    for seed in seeds.get('supplemental_measurements', []):
        source=source_map[seed['source']]
        ref=make_reference(source,seed['page'],seed['label'],seed['raw'],seed['unit'],str(seed['year']),
            seed['box'],table='Supplemental source table/chart/paragraph',year=seed['year'],concept=seed['concept'],
            notes=[seed['note']])
        refs.append(ref)
    # Recompute both missing-field lists after field-specific adjustments.
    for ref in refs:
        for k in ('reporting_entity','consolidation','scope','counting_method','calculation_method'):
            ref['boundary'][k] = ref['expected'][k]
        ref['boundary']['missing_fields'] = sorted(k for k,v in ref['boundary'].items() if k!='missing_fields' and v is None)
        ref['missing_fields'] = sorted(['expected.'+k for k,v in ref['expected'].items() if v is None] +
                                      ['boundary.'+k for k in ref['boundary']['missing_fields']])
    return refs, source_map


def attach_bindings(refs, predictions):
    """Link by source/row/column metadata only, NEVER by predicted numeric value."""
    for ref in refs:
        hint = ref['link_hint']
        for row in predictions:
            if row['source_sha256'] != ref['source_sha256'] or row['physical_page'] != ref['physical_page']:
                continue
            if 'narrative_excerpt' in hint:
                candidate = normal_text(row['fields'].get('text') or '')
                quote = normal_text(hint['narrative_excerpt'])
                match = len(candidate)>30 and (quote in candidate or candidate in quote)
                partial = match and quote != candidate
            else:
                label_match = normal_text(row.get('label') or '').casefold()==normal_text(hint['label']).casefold()
                metric_match = hint.get('metric_id') and hint['metric_id']==row['fields'].get('metric_id')
                if ref['expected'].get('metric_id')=='local:employee_headcount_at_date:v1' and hint['label']=='Tổng số nhân viên':
                    metric_match = row['fields'].get('metric_id')=='local:employee_headcount_at_date:v1'
                match = (label_match or metric_match) and hint['year']==row['fields'].get('observation_year')
                if 'table_index' in hint:
                    match = match and row['anchor'].startswith(f'/document/tables/{hint["table_index"]}/')
                partial = False
            if match:
                ref['extract_record_bindings'].append({'record_id': row['record_id'], 'json_pointer': row['anchor'],
                    'record_type': row['record_type'], 'fingerprint': row['fingerprint'],
                    'link_basis': 'same PDF/page and row/column metadata; values independently transcribed',
                    'partial_text_only': partial})
        ref.pop('link_hint')


def validate_reference(data):
    if data.get('schema_version')!='oil-gas-ai-reference/1.0' or data.get('is_gold') is not False or data.get('annotation_status')!=STATUS:
        raise ValueError('AI reference must not claim human gold status.')
    seen = set()
    inventory = data['source_inventory']
    for ref in data['records']:
        if ref['reference_id'] in seen:
            raise ValueError('Duplicate reference ID.')
        seen.add(ref['reference_id'])
        if ref['annotation_status']!=STATUS or ref['review_status']!='pending_human_review' or ref['is_gold'] is not False:
            raise ValueError('AI cannot approve itself.')
        source = ref['source_sha256']
        if not 1<=ref['physical_page']<=inventory[source]['pages']:
            raise ValueError('Invalid PDF page.')
        boundary_missing = sorted(k for k,v in ref['boundary'].items() if k!='missing_fields' and v is None)
        if ref['boundary']['missing_fields'] != boundary_missing:
            raise ValueError('Boundary missing-fields mismatch.')
        outer_missing = sorted(['expected.'+k for k,v in ref['expected'].items() if v is None] + ['boundary.'+k for k in boundary_missing])
        if ref['missing_fields'] != outer_missing:
            raise ValueError('Outer missing-fields mismatch.')
        for field,value in ref['expected'].items():
            if value is None:
                if not ref['unknown_reasons'].get(field): raise ValueError('Null needs reason.')
            elif not ref['field_evidence'].get(field):
                raise ValueError('Known value needs source evidence.')
        for field, field_evidence in ref['field_evidence'].items():
            if ref['expected'][field] is None:
                raise ValueError('Null fields must not masquerade as resolved evidence.')
            for e in field_evidence:
                if e['source_sha256']!=source or not 1<=e['physical_page']<=inventory[source]['pages'] or not e.get('quote'):
                    raise ValueError('Invalid field-level source evidence.')
        for e in ref['evidence']:
            if e['source_sha256']!=source or not e.get('quote') or not e.get('anchor'):
                raise ValueError('Invalid evidence.')
            box=e['bbox_normalized_xyxy']
            if not (0<=box[0]<box[2]<=1 and 0<=box[1]<box[3]<=1):
                raise ValueError('Invalid normalized evidence box.')
    return {'status': 'PASS_AI_REFERENCE_STRUCTURE_ONLY', 'records':len(seen), 'human_approved_records':0,
            'precision':None, 'limits':'Not independent gold, not proof of source truth or full report coverage.'}


def comparison_proposals(refs, predictions):
    """Disagreements for human review, not precision or automatic corrections."""
    by_id = {r['record_id']: r for r in predictions}
    proposals=[]
    for ref in refs:
        for binding in ref['extract_record_bindings']:
            row = by_id[binding['record_id']]
            differences={}
            for field in ref['reviewed_fields']:
                expected=ref['expected'][field]
                if expected is None: continue
                if field=='text':
                    if binding['partial_text_only']: continue
                    same=normal_text(expected)==normal_text(row['fields'].get(field) or '')
                else:
                    same=equal(field,expected,row['fields'].get(field))
                if not same:
                    differences[field]={'extracted':row['fields'].get(field),'ai_reference':expected,
                        'status':'proposed_change_pending_human_review',
                        'evidence':deepcopy(ref['field_evidence'][field])}
            if differences:
                proposals.append({'reference_id':ref['reference_id'],'record_id':row['record_id'],
                    'source_sha256':ref['source_sha256'],'physical_page':ref['physical_page'],
                    'original_json_pointer':row['anchor'],'field_differences':differences,
                    'auto_applied':False,'is_gold':False})
    return proposals


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination',type=Path,required=True)
    args=parser.parse_args()
    if args.destination.exists(): raise ValueError('Choose a new directory; never overwrite reviewed annotations.')
    seeds_path=ROOT/'config/ai_reference_bsr_20261021.yml'
    seeds=yaml.safe_load(seeds_path.read_text(encoding='utf-8'))
    pack=ROOT/'outputs/oil_gold_bsr_v1_20261021_r2'
    pages=json.loads((ROOT/'tmp/ai_reference_pages_20261021/pages.json').read_text(encoding='utf-8'))
    inventory=json.loads((pack/'source_inventory.json').read_text(encoding='utf-8'))
    for source, info in inventory.items():
        target=ROOT/'outputs/ESG_extract_V2'/info['pdf_path']
        if sha256(target.read_bytes()).hexdigest()!=source: raise ValueError('Original PDF changed.')
    refs, source_map=build_references(seeds,pages)
    predicted=json.loads((pack/'predictions.json').read_text(encoding='utf-8'))['records']
    attach_bindings(refs,predicted)
    book=yaml.safe_load((ROOT/'config/oil_gas_gold.yml').read_text(encoding='utf-8'))
    for ref in refs:
        concept=ref['standards_annotation']['candidate_concept_id']
        ref['standards_annotation']['candidate_references']=deepcopy(book['metrics'][concept]['refs']) if concept else []
        ref['standards_annotation']['note']='Codebook proposal only, not confirmation that the reported item fully satisfies any disclosure.'
    proposals=comparison_proposals(refs,predicted)
    draft=json.loads((pack/'reviewer_a_draft.json').read_text(encoding='utf-8'))
    selected={(u['source_sha256'],u['physical_page']) for u in draft['evaluation_units']}
    selected_rows=[r for r in predicted if (r['source_sha256'],r['physical_page']) in selected]
    links={b['record_id']:[] for ref in refs for b in ref['extract_record_bindings']}
    for ref in refs:
        for b in ref['extract_record_bindings']: links[b['record_id']].append(ref['reference_id'])
    ledger=[]
    for row in selected_rows:
        index_page=(row['source_sha256']==source_map['esg2025'] and row['physical_page']==64) or (row['source_sha256']==source_map['esg2023'] and row['physical_page']==19)
        rejected=index_page and row['record_type']=='measurement'
        ledger.append({'record_id':row['record_id'],'source_sha256':row['source_sha256'],
            'physical_page':row['physical_page'],'json_pointer':row['anchor'],
            'status':'AI_rejected_as_company_measurement_pending_human_review' if rejected else
                     'AI_partially_reviewed_pending_human_review' if row['record_id'] in links else 'NOT_REVIEWED',
            'reference_ids':links.get(row['record_id'],[]),
            'reason':'Disclosure index/code/page number, not a company KPI value.' if rejected else
                     'Only declared reference fields/excerpts checked; full record still needs human review.' if row['record_id'] in links else
                     'Page visually inspected; this individual candidate has not been fully adjudicated.'})
    issues=[]
    for issue in seeds['issues']:
        item=deepcopy(issue)
        item['source_sha256']=source_map[item.pop('source')]
        if 'other_source' in item: item['other_source_sha256']=source_map[item.pop('other_source')]
        item.update(status='NeedsReview',review_status='pending_human_review',check_channel='ESG_INTERNAL' if issue['kind'].startswith('internal_consistency') else 'SOURCE_REVIEW')
        issues.append(item)
    coverage={'selected_pages':len(selected),'supplemental_pages':sum(p['role']=='supplemental' for p in pages),'visually_inspected_pages':len(pages),
        'fully_annotated_pages':0,'selected_candidate_predictions':len(selected_rows),
        'candidate_status_counts':dict(Counter(r['status'] for r in ledger)),
        'ai_reference_records':len(refs),'references_without_existing_record_binding':sum(not r['extract_record_bindings'] for r in refs),
        'record_reference_pairs_with_proposed_changes':len(proposals),
        'human_approved_records':0,'actual_precision':None,
        'limits':'Partial priority review, not all 601 reference slots or every record on inspected pages. No full-corpus recall or accuracy claim.'}
    data={'schema_version':'oil-gas-ai-reference/1.0','annotation_status':STATUS,'is_gold':False,
        'reviewer':{'type':'AI','independent_human_reviewers':0},'split':'dev',
        'source_inventory':inventory,'source_delivery':'outputs/ESG_extract_V2',
        'codebook_sha256':sha256((ROOT/'config/oil_gas_gold.yml').read_bytes()).hexdigest(),
        'transcription_seeds_sha256':sha256(seeds_path.read_bytes()).hexdigest(),
        'builder_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
        'prediction_snapshot_sha256':sha256((pack/'predictions.json').read_bytes()).hexdigest(),
        'coverage':coverage,'records':refs,'issue_log':issues,
        'guardrails':['Not human-reviewed gold','No automatic Contradicted/greenwashing conclusion',
                      'No IFRS compliance assertion','No automatic source-value harmonisation','SASB protocols remain pending']}
    validation=validate_reference(data)
    args.destination.mkdir(parents=True)
    atomic_json(args.destination/'ai_reference.json',data)
    atomic_json(args.destination/'candidate_review_ledger.json',ledger)
    atomic_json(args.destination/'coverage.json',coverage)
    atomic_json(args.destination/'issues_for_human_review.json',issues)
    atomic_json(args.destination/'validation.json',validation)
    atomic_json(args.destination/'proposed_field_changes_NOT_APPLIED.json',proposals)
    # Preserve exact source images used for inspection, not re-rendered PDFs.
    import shutil
    image_dir=args.destination/'source_page_images'
    image_dir.mkdir()
    image_index=[]
    for page in pages:
        img=Path(page['image_path'])
        dest=image_dir/img.name
        shutil.copyfile(img,dest)
        image_index.append({'source_sha256':page['source_sha256'],'physical_page':page['physical_page'],
                            'image_path':'source_page_images/'+dest.name,'sha256':sha256(dest.read_bytes()).hexdigest(),
                            'role':page['role'],'original_pdf_path':inventory[page['source_sha256']]['pdf_path']})
    atomic_json(args.destination/'source_page_images.json',image_index)
    image_lookup={(r['source_sha256'],r['physical_page']):r['image_path'] for r in image_index}
    atomic_json(args.destination/'review_index.json',[
        {'reference_id':ref['reference_id'],'source_pdf':inventory[ref['source_sha256']]['pdf_path'],
         'physical_page':ref['physical_page'],'image_path':image_lookup[(ref['source_sha256'],ref['physical_page'])],
         'kind':ref['record_kind'],'raw':ref['raw_transcription'],
         'value':ref['expected']['value'],'unit':ref['expected']['unit'],'year':ref['expected']['observation_year'],
         'notes':ref['notes'],'status':ref['annotation_status']} for ref in refs])
    print(json.dumps(coverage,ensure_ascii=False))


if __name__=='__main__':
    main()
