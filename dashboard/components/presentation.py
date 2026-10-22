"""Display adapters only: never mutate extraction outputs or evidence states."""
import json

from dashboard.upload_v2 import record_rows


def review_label(record):
    human = record.get('human_review')
    if human:
        return ('REVIEWED', '✓ Đã rà soát') if human['status']=='reviewed' else ('NOT_REVIEWED', '○ Chưa rà soát · NOT_REVIEWED')
    status = record.get('review', {}).get('status')
    # Automatic candidate/needs_review is NOT a completed review.
    return ('REVIEWED', '✓ Đã rà soát') if status in ('reviewed', 'verified') else (
        'NOT_REVIEWED', '○ Chưa rà soát · NOT_REVIEWED')


def display_rows(result):
    records = {f"{d['document_index']}:{r['record_id']}": (r, d)
               for d in result.get('documents', []) for r in d['output']['records']}
    rows = record_rows(result)
    for row in rows:
        record, doc = records[row['id']]
        state, label = review_label(record)
        row.update(review_status=state, review_label=label,
                   pillar=record.get('classification', {}).get('pillar', 'unknown'),
                   report_year=doc['output']['reports'][0].get('reporting_year'))
        row['indicator'] = row.get('indicator') or record.get('original_text')
        human=record.get('human_review')
        if human:
            row['human_review_status']=human['status']
            row['review_revision']=human['revision']
            if human['status'] in ('reviewed','partially_reviewed'):
                for canonical,column in [('value','value'),('unit','unit'),('observation_year','year')]:
                    if canonical in human['reviewed_fields']:
                        value=human['effective_fields'][canonical]
                        row[column]=str(value) if canonical=='value' and value is not None else value
    return rows


def session_summary(result):
    if not result or result.get('status') != 'completed':
        return None
    claims = [r for d in result.get('documents', []) for r in d['output']['records'] if r['record_type'] == 'claim']
    reviewed = sum(review_label(r)[0] == 'REVIEWED' for r in claims)
    return {'reports': result['manifest']['document_count'], 'claims': len(claims),
            'reviewed': reviewed, 'unreviewed': len(claims) - reviewed}


def table_filter(search=None, company=None, year=None, pillar=None, review=None, kind=None):
    # Quote all values as JSON strings: user input cannot add filter operators.
    quote = lambda value: json.dumps(str(value), ensure_ascii=False)
    parts = [f'{{{key}}} = {quote(value)}' for key, value in (
        ('company', company), ('report_year', year), ('pillar', pillar),
        ('type', kind)) if value is not None and value != '']
    if review:
        label = '○ Chưa rà soát · NOT_REVIEWED' if review == 'NOT_REVIEWED' else '✓ Đã rà soát'
        parts.append(f'{{review_label}} = {quote(label)}')
    if search and search.strip():
        text = quote(search.strip())
        parts.append('(' + ' || '.join(f'{{{key}}} contains {text}' for key in ('original_text', 'indicator', 'file')) + ')')
    return ' && '.join(parts)
