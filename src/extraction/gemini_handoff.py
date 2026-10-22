"""Corporate adapter for explicit cloud-LLM candidates, not native text proof."""
from decimal import Decimal, localcontext
from pathlib import Path

from jsonschema import Draft202012Validator

from src.extraction.gemini import read_json
from src.extraction.source_v2 import stable_id, file_hash


def convert(document, source_info=None):
    from src.extraction.corporate_handoff import _unit, _number, CONTRACT
    from src.extraction.corporate_review import identify, CATALOG
    out, info = document['output'], source_info or {}
    report = out['reports'][0]
    work = Path(document['workspace']).resolve()
    for artifact in out['source_artifacts']:
        path = (work / artifact['path']).resolve()
        if not path.is_relative_to(work) or not path.is_file() or file_hash(path) != artifact['sha256']:
            raise ValueError('Gemini source artifact đã thay đổi; không bàn giao.')
    financial = report['report_type'] == 'financial_statements'
    meta = out.get('metadata', {})
    scope = {'separate': 'Separate', 'consolidated': 'Consolidated'}.get(meta.get('statement_scope', {}).get('value')) if financial else None
    if financial and scope is None:
        raise ValueError('Gemini chưa xác định được riêng/hợp nhất có evidence; giữ native JSON, chưa xuất Financial corporate.')
    source_sha = report['source_sha256']
    doc_id = stable_id('corporate_document', source_sha)
    records, issues = [], []

    def issue(code, message, pages=(), record_id=None):
        issues.append({'issue_id': stable_id('issue', doc_id, code, message, record_id), 'code': code,
                       'message': message, 'source_pages': sorted(set(p for p in pages if p)),
                       'record_id': record_id, 'status': 'needs_review'})

    for original in out['records']:
        payload, kind = original['payload'], original['record_type']
        # Corporate v1 cannot mix financial records into an ESG/annual document.
        # Preserve those records in native JSON and explicitly log the gap.
        if (financial and (kind != 'measurement' or original['domain'] != 'financial')) or (
                not financial and (original['domain'] == 'financial' or kind == 'financial_context')):
            issue('GEMINI_NATIVE_RECORD_NOT_IN_CORPORATE', 'Corporate v1 domain/type limitation; native record retained: ' + original['record_id'])
            continue
        if not financial and original['classification']['pillar'] not in ('E', 'S', 'G'):
            issue('GEMINI_DIMENSION_UNKNOWN', 'Không suy dimension; native record retained: ' + original['record_id'])
            continue
        evidence = []
        for observation in original['gemini_evidence']:
            ref = observation['source']
            quote = observation['quote']
            role = {'column_header': 'year', 'unit': 'unit', 'date': 'period', 'boundary': 'scope'}.get(observation['role'], 'other')
            headers = [{'role': role, 'text': quote, 'physical_page': ref['pdf_page'], 'row': None, 'column': None, 'bbox': None}] if role != 'other' else []
            evidence.append({'evidence_id': stable_id('evidence', source_sha, original['record_id'], ref['artifact_id'], ref['native_json_pointer']),
                'source_sha256': source_sha, 'physical_page': ref['pdf_page'], 'printed_page': None,
                'exact_quote': quote, 'context_text': quote, 'section': None,
                'element_id': ref['native_json_pointer'], 'char_start': None, 'char_end': None,
                'bbox': None, 'table_id': None, 'row': None, 'column': None, 'headers': headers, 'footnotes': []})
        if not evidence:continue
        raw, parsed, raw_unit = payload['raw_value'], payload['parsed_value'], payload['unit_raw']
        _, base, factor, scale = _unit(raw_unit, [raw_unit] if raw_unit else [])
        numeric = normalization_factor = None
        if parsed is not None and factor is not None:
            with localcontext() as context:
                context.prec = 256
                numeric = _number(Decimal(parsed) * factor)
            normalization_factor = _number(factor)
        value_status = 'available' if numeric is not None else 'unknown' if raw is None else 'ambiguous'
        period = original.get('content_period') or {}
        year = period.get('year')
        key = identify(payload['row_label_raw'])
        topic, definition = CATALOG[key] if key else ('financial_unclassified' if financial else 'esg_unclassified', None)
        uncertainty = ['cloud_llm_visual_candidate_not_independently_verified', 'semantic_completeness_not_verified',
                       'reporting_boundary_not_verified', 'metadata_input_requires_review']
        if key:uncertainty.append('local_metric_mapping_pending_human_review')
        model_version = original['extraction_provenance'].get('model')
        records.append({'record_id': original['record_id'], 'dimension': 'X' if financial else original['classification']['pillar'],
            'record_type': 'financial_measurement' if financial else {'action': 'claim', 'governance': 'governance_evidence'}.get(kind, kind),
            'topic': topic, 'metric_id': 'local:' + key + ':v1' if key else None,
            'metric_label': payload['row_label_raw'], 'metric_definition': definition,
            'statement': {'original_quote': original['original_text'], 'interpretation': '\n'.join(original['interpretation_notes']) or None,
                          'assertion_kind': 'target' if kind == 'target' else 'policy' if kind == 'policy' else 'reported_result' if kind == 'measurement' else 'context'},
            'value': {'status': value_status, 'original_value': raw, 'original_unit': raw_unit,
                'original_scale': scale, 'normalized_value': numeric, 'normalized_unit': base,
                'normalization_factor': normalization_factor,
                'normalization_note': 'Code Decimal conversion from model-proposed literal number/unit; scale applied once; visual/semantic review pending.'},
            'period': {'observation_year': year, 'observation_start': period.get('start_date'), 'observation_end': period.get('end_date'),
                'measurement_date': period.get('as_of_date'), 'period_type': 'at_date' if period.get('as_of_date') else 'range' if period.get('start_date') and period.get('end_date') else 'unknown',
                'year_basis': 'table_header' if year is not None and any(str(year) in h for h in payload['column_headers_raw']) else 'explicit_quote' if year is not None else 'unknown',
                'baseline_year': None, 'target_deadline': None},
            'boundary': {'reporting_entity': original.get('reported_entity'), 'consolidation': scope if financial else
                         {'separate': 'Separate', 'consolidated': 'Consolidated'}.get(payload.get('statement_scope'), 'unknown'),
                         'scope': payload.get('scope'), 'population': None, 'counting_method': None, 'calculation_method': None, 'verified': False},
            'restatement': {'status': 'unknown', 'note': None}, 'evidence': evidence,
            'quality': {'extraction_method': 'cloud_llm', 'parser_name': 'Gemini PDF candidate adapter/1; source pointers refer to MODEL observations, not Docling/OCR truth',
                'model_id': model_version, 'prompt_version': out['prompt_version'], 'uncertainty': uncertainty,
                'review_status': 'pending_human_review', 'reviewer': None, 'reviewed_at_utc': None, 'review_basis': None}, 'comparison_group_id': None})
        issue('GEMINI_RECORD_REQUIRES_HUMAN_REVIEW', 'Literal model snippets are NOT independent PDF verification; check row/year/unit/entity on original PDF.',
              [e['physical_page'] for e in evidence], original['record_id'])
    for item in out['issues']:
        issue(item['code'], str(item.get('details', 'See native output')), [item.get('pdf_page')])
    issue('SOURCE_PROVENANCE_UNCONFIRMED', 'Uploaded PDF and supplied URL are not an independent official-source verification.')
    issue('GEMINI_SEARCH_NOT_ADJUDICATED', 'Model page processing is not a confirmed topic search or evidence of disclosure absence.')
    coverage = out['coverage']
    year_field = meta.get('reporting_year', {})
    year = year_field.get('value') if year_field.get('status') == 'available' else report['reporting_year']
    handoff = {'schema_version': 'corporate-extract-1.0',
        'document': {'document_id': doc_id, 'company_id': report['company_id'], 'report_type': 'Financial' if financial else 'ESG',
            'source_document_type': 'financial_statement' if financial else 'annual_report' if report['report_type'] == 'annual_report' else 'sustainability_report',
            'report_year': year, 'financial_scope': scope, 'reporting_entity': meta.get('company_name', {}).get('value'),
            'reporting_period_start': None, 'reporting_period_end': None, 'publication_date': None,
            'source': {'source_id': stable_id('source', source_sha), 'file_name': document['filename'], 'url': info.get('url'),
                'downloaded_at_utc': info.get('downloaded_at_utc'), 'sha256': source_sha, 'page_count': report['pdf_page_count'], 'page_system': 'physical_pdf_page_1_based'}},
        'coverage': {'status': 'partial', 'scope_description': 'Gemini PDF candidates; human verification and semantic completeness pending.',
            'search_status': 'not_searched', 'pages_checked': [p['pdf_page'] for p in coverage['pages'] if p['status'] == 'processed'],
            'pages_unreadable': [p['pdf_page'] for p in coverage['pages'] if p['status'] == 'failed'], 'topics_searched': [], 'search_outcomes': []},
        'records': records, 'issue_log': issues}
    errors = list(Draft202012Validator(read_json(CONTRACT / 'schema.json')).iter_errors(handoff))
    if errors:
        raise ValueError('Gemini corporate schema invalid: ' + '; '.join(e.message for e in errors[:4]))
    return handoff
