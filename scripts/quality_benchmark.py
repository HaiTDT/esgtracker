"""Prepare human gold drafts, measure independent predictions, inspect rule checks."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys
import yaml

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.quality.records import project, native_snapshots, versions
from src.quality.evaluation import make_template, evaluate
from src.quality.dictionary import load_dictionary
from src.quality.checks import financial_formula_checks, record_checks
from src.extraction.source_v2 import atomic_json, now


def benchmark_versions():
    return {'benchmark_environment':versions(ROOT),
            'extraction_version_source':'See each record.extraction_provenance and original native output. Current environment hashes are NOT historical extractor version proof.'}


def known_development_sources():
    path=ROOT/'config/quality_development_sources.yml'
    return set(yaml.safe_load(path.read_text(encoding='utf-8'))['source_sha256']) if path.is_file() else set()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def predictions(path):
    path=Path(path)
    records=[]
    ocr=[]
    natives=[]
    if path.is_dir():
        manifest=read(path/'manifest.json')
        for row in manifest['files']:
            if row['status']=='unavailable': continue
            target=(path/row['json_path']).resolve()
            if not target.is_relative_to(path.resolve()) or sha256(target.read_bytes()).hexdigest()!=row['json_sha256']:
                raise ValueError('Delivery JSON path/hash mismatch.')
            h=read(target)
            records.extend(project(r,h['document']) for r in h['records'])
            npath=path/'notes/native'/(row['pdf_sha256']+'.json')
            if npath.is_file():
                native=read(npath)
                natives.append(native)
                for artifact in native.get('source_artifacts',[]):
                    if artifact['kind']!='page_checkpoint':continue
                    cp=(path/'notes/native'/row['pdf_sha256']/artifact['path']).resolve()
                    if not cp.is_relative_to(path.resolve()) or sha256(cp.read_bytes()).hexdigest()!=artifact['sha256']:
                        raise ValueError('Native checkpoint hash/path mismatch.')
                    page=read(cp)
                    if native.get('provider') == 'gemini_api':
                        # Model snippets are predictions, NOT an independent OCR transcription.
                        continue
                    texts=[t['text'] for t in page.get('document',{}).get('texts',[]) if t.get('text')]
                    for table in page.get('document',{}).get('tables',[]):
                        texts.extend(c['text'] for c in table.get('data',{}).get('table_cells',[]) if c.get('text'))
                    ocr.append({'source_sha256':row['pdf_sha256'],'physical_page':page['pdf_page'],'text':'\n'.join(texts)})
        return {'schema_version':'esg-quality-predictions/1.0','records':records,'ocr_pages':ocr,'versions':benchmark_versions(),
                'source_documents':[{k:r[k] for k in ('document_id','report_year','report_type','financial_scope','pdf_path','pdf_sha256','json_path','json_sha256')} for r in manifest['files']],
                'source_manifest_sha256':sha256((path/'manifest.json').read_bytes()).hexdigest()},natives
    data=read(path)
    if data.get('schema_version')=='esg-quality-predictions/1.0': return data,[]
    if 'documents' in data:
        return {'schema_version':'esg-quality-predictions/1.0','records':native_snapshots(data),'ocr_pages':[],'versions':benchmark_versions()},[d['output'] for d in data['documents']]
    if 'document' in data and 'records' in data:
        records=[project(r,data['document']) for r in data['records']]
    elif 'reports' in data and 'records' in data:
        by_id={r['record_id']:r for r in data['records']}
        records=[project(r,data['reports'][0],linked_metric=by_id.get(r.get('payload',{}).get('metric_record_id') or r.get('payload',{}).get('metric_id'))) for r in data['records']]
        natives=[data]
    else: raise ValueError('Expected corporate delivery/JSON or native semantic result, not raw source capture.')
    return {'schema_version':'esg-quality-predictions/1.0','records':records,'ocr_pages':[],'versions':benchmark_versions()},natives


def write_new(path,data):
    path=Path(path)
    if path.exists():raise ValueError('Output already exists; choose a NEW path.')
    path.parent.mkdir(parents=True,exist_ok=True)
    atomic_json(path,data)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('template',help='Create a DRAFT, never gold. All fields require human annotation.')
    p.add_argument('input',type=Path)
    p.add_argument('--destination',type=Path,required=True)
    p.add_argument('--limit-pages',type=int,default=12)
    p.add_argument('--split',choices=['train','dev','test'],default='dev')
    p=sub.add_parser('evaluate')
    p.add_argument('--predictions',type=Path,required=True)
    p.add_argument('--gold',type=Path,required=True)
    p.add_argument('--split',choices=['train','dev','test'],default='test')
    p.add_argument('--development-source',action='append',default=[])
    p.add_argument('--output',type=Path,required=True)
    p=sub.add_parser('check')
    p.add_argument('input',type=Path)
    p.add_argument('--output',type=Path,required=True)
    p=sub.add_parser('dictionary')
    p.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    try:
        if args.command=='dictionary':
            write_new(args.output,load_dictionary())
        elif args.command=='template':
            if args.destination.exists() or args.limit_pages<=0:raise ValueError('Choose a NEW directory and a positive page limit.')
            data,_=predictions(args.input)
            known=known_development_sources()
            if args.split=='test' and known & {r['source_sha256'] for r in data['records']}:
                raise ValueError('Known development PDF in test template. Use --split dev or independently held-out sources.')
            gold=make_template(data['records'],args.split)
            gold['development_source_sha256']=sorted(known)
            # Stable round-robin by PDF: do not sample only the largest report.
            groups={}
            for unit in gold['evaluation_units']:groups.setdefault(unit['source_sha256'],[]).append(unit)
            for key in groups:groups[key].sort(key=lambda u:sha256(f"{key}:{u['physical_page']}".encode()).hexdigest())
            units=[]
            while len(units)<args.limit_pages and any(groups.values()):
                for key in sorted(groups):
                    if groups[key] and len(units)<args.limit_pages:units.append(groups[key].pop())
            gold['evaluation_units']=units
            gold['prediction_versions']=data['versions']
            args.destination.mkdir(parents=True)
            atomic_json(args.destination/'predictions.json',data)
            atomic_json(args.destination/'gold_draft.json',gold)
            atomic_json(args.destination/'sampling.json',{'created_at':now(),'pages':len(units),'sources':len({u['source_sha256'] for u in units}),'policy':'Stable round-robin by source, candidate-bearing pages only. Not a representative corpus accuracy estimate; add empty/missed/scan/chart pages manually.','gold_created':False})
            print('DRAFT ONLY: annotate PDF independently; no precision computed.')
        elif args.command=='evaluate':
            data,_=predictions(args.predictions)
            report=evaluate(data['records'],read(args.gold),split=args.split,development_sources=set(args.development_source)|known_development_sources(),ocr_predictions=data.get('ocr_pages',[]))
            report.update(created_at=now(),predictions_sha256=sha256(args.predictions.read_bytes()).hexdigest() if args.predictions.is_file() else None,
                          gold_sha256=sha256(args.gold.read_bytes()).hexdigest(),prediction_versions=data.get('versions'))
            write_new(args.output,report)
            print(json.dumps(report['strict_record'],ensure_ascii=False))
        else:
            data,natives=predictions(args.input)
            write_new(args.output,{'created_at':now(),'record_findings':[i for r in data['records'] for i in record_checks(r)],
                                  'financial_checks':[financial_formula_checks(n) for n in natives],
                                  'status':'NeedsReview','is_accuracy_measurement':False})
        return 0
    except (ValueError,KeyError,OSError) as exc:
        print(str(exc),file=sys.stderr)
        return 2


if __name__=='__main__':raise SystemExit(main())
