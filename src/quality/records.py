"""Small common projection for native and corporate records; source stays immutable."""
from copy import deepcopy
from decimal import Decimal, InvalidOperation
from datetime import date
from hashlib import sha256
import json
from pathlib import Path

FIELDS = ('metric_id', 'value', 'unit', 'observation_year', 'period_type',
          'measurement_date', 'reporting_entity', 'consolidation', 'scope',
          'counting_method', 'calculation_method', 'text')
MEASUREMENT_FIELDS = ('metric_id', 'value', 'unit', 'observation_year', 'period_type',
                      'reporting_entity', 'consolidation', 'scope')


def digest(value):
    return sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def versions(root):
    root = Path(root)
    files = ('config/metric_dictionary.yml', 'config/metrics.yml', 'config/esg_v2.yml',
             'src/extraction/corporate_review.py', 'src/extraction/financial_v2.py',
             'src/extraction/esg_v2.py', 'src/quality/records.py', 'src/quality/review_store.py',
             'src/quality/dictionary.py', 'dashboard/human_review.py',
             'src/extraction/gemini.py', 'src/extraction/gemini_handoff.py',
             'config/gemini.yml', 'contracts/gemini_response.schema.json')
    return {name: sha256((root/name).read_bytes()).hexdigest() if (root/name).is_file() else None for name in files}


def required_fields(record):
    return MEASUREMENT_FIELDS if record.get('record_type') in ('measurement', 'financial_measurement', 'target') else ('text',)


def project(record, document, *, linked_metric=None):
    corporate = 'quality' in record and 'statement' in record
    payload = record.get('payload', {})
    metric = linked_metric or {}
    if corporate:
        boundary = record['boundary']
        period = record['period']
        evidence = record['evidence'][0]
        fields = {'metric_id':record['metric_id'], 'value':record['value']['normalized_value'],
                  'unit':record['value']['normalized_unit'], 'observation_year':period['observation_year'],
                  'period_type':period['period_type'], 'measurement_date':period['measurement_date'],
                  'reporting_entity':boundary['reporting_entity'], 'consolidation':boundary['consolidation'],
                  'scope':boundary['scope'], 'counting_method':boundary['counting_method'],
                  'calculation_method':boundary['calculation_method'], 'text':record['statement']['original_quote']}
        source_sha = document['source']['sha256']
        page, anchor = evidence['physical_page'], evidence['element_id']
    else:
        refs = [r for group in record.get('field_sources', {}).values() for r in group]
        primary = next((record.get('field_sources', {}).get(k) for k in ('/payload/raw_value','/original_text') if record.get('field_sources', {}).get(k)), refs[:1])
        ref = primary[0] if primary else {}
        period = record.get('content_period') or {}
        boundary = record.get('boundary', {})
        concept = payload.get('metric_code') or payload.get('metric_id')
        if concept and concept.startswith('record_'):
            concept = None  # Native row ID is not a conceptual metric ID.
        fields = {'metric_id':concept, 'value':payload.get('parsed_value',payload.get('value',payload.get('target_value'))),
                  'unit':payload.get('unit'), 'observation_year':period.get('year'),
                  'period_type':period.get('period_type','unknown'), 'measurement_date':period.get('as_of_date'),
                  'reporting_entity':record.get('reported_entity'), 'consolidation':payload.get('statement_scope') or boundary.get('consolidation_method'),
                  'scope':payload.get('scope'), 'counting_method':None,'calculation_method':None,
                  'text':record.get('original_text')}
        source_sha = document.get('source_sha256')
        page, anchor = ref.get('pdf_page'), ref.get('native_json_pointer')
    label = record.get('metric_label') or payload.get('row_label_raw') or payload.get('name_raw') or metric.get('original_text') or record.get('original_text')
    snapshot = {'source_sha256':source_sha, 'record_id':record['record_id'], 'record_type':record['record_type'],
                'physical_page':page, 'anchor':anchor, 'label':label, 'fields':fields,
                'document_context':{k:document.get(k) for k in ('company_id','report_year','reporting_year','report_type','financial_scope')}}
    snapshot['extraction_provenance'] = deepcopy(record.get('quality')) if corporate else {'classification':deepcopy(record.get('classification'))}
    snapshot['fingerprint'] = digest({'record':record, 'document':document})
    snapshot['record_key'] = digest({'source_sha256':source_sha,'record_id':record['record_id']})
    return snapshot


def native_snapshots(result):
    rows = []
    for doc in result.get('documents', []):
        by_id = {r['record_id']:r for r in doc['output']['records']}
        for r in by_id.values():
            payload = r.get('payload', {})
            snapshot = project(r, doc['output']['reports'][0], linked_metric=by_id.get(payload.get('metric_record_id') or payload.get('metric_id')))
            snapshot['selection_id'] = f"{doc['document_index']}:{r['record_id']}"
            snapshot['extraction_provenance'].update({k:deepcopy(doc['output'].get(k)) for k in
                ('schema_version','parser_version','config','metrics_config_sha256','source_capture_sha256',
                 'provider','model','profile_id','prompt_version')})
            rows.append(snapshot)
    return rows


def valid_corrections(patch):
    if not isinstance(patch, dict) or set(patch)-set(FIELDS):
        raise ValueError('Chỉ được sửa các field dữ liệu được khai báo; không sửa ID/nguồn/OCR gốc.')
    for field,value in patch.items():
        if field == 'value' and value is not None:
            if isinstance(value,bool):
                raise ValueError('Giá trị số không thể là boolean.')
            try:
                if not Decimal(str(value)).is_finite():
                    raise ValueError('Giá trị phải hữu hạn.')
            except InvalidOperation as exc:
                raise ValueError('Giá trị số không hợp lệ.') from exc
        elif field == 'observation_year' and value is not None:
            if isinstance(value,bool) or not isinstance(value,int) or not 2000 <= value <= 2100:
                raise ValueError('Năm quan sát phải là số nguyên 2000–2100 hoặc null.')
        elif value is not None and not isinstance(value,str):
            raise ValueError(f'{field} phải là chuỗi hoặc null.')
        if field=='measurement_date' and value is not None:
            try: date.fromisoformat(value)
            except ValueError as exc: raise ValueError('measurement_date phải có dạng YYYY-MM-DD hợp lệ.') from exc
        if field=='consolidation' and value not in (None,'unknown','not_applicable','Separate','Consolidated','separate','consolidated'):
            raise ValueError('consolidation phải là Separate/Consolidated/unknown hoặc null.')
        if field=='metric_id' and value is not None:
            from src.quality.dictionary import load_dictionary
            dictionary=load_dictionary()
            allowed={'local:'+k+':v1' for k in dictionary['local_metrics']}|set(dictionary['legacy_esg_metrics'])
            if value not in allowed:
                raise ValueError('metric_id chưa có trong từ điển; không dùng record_id làm metric_id.')
    return deepcopy(patch)
