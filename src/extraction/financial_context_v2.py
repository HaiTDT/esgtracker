"""Evidence-based statement scope and conservative adjacent-page continuation.

Never infer KPI entity boundary from financial statement scope. OCR text is not
repaired. A continuation is a reviewable rule match, not manual verification.
"""
import re
import unicodedata

from src.extraction.source_v2 import stable_id


def normalized(text):
    value = unicodedata.normalize('NFD', text.lower().replace('đ', 'd'))
    return re.sub(r'\s+', ' ', ''.join(c for c in value if unicodedata.category(c) != 'Mn')).strip()


def scope_candidate(block):
    # A disclosure letter often lists BOTH attachments. These are not titles
    # establishing the scope of the financial statements in this PDF.
    if block.get('label') == 'list_item':
        return None
    text = normalized(block.get('original_text') or '')
    if len(text) > 350 or re.search(r'\bkhong\b|\bnot\b|\bnon[- ]', text):
        return None
    report_title = re.match(r'^(?:thuyet minh (?:cho )?)?(?:(?:bo|cac) )?bao cao tai chinh (rieng|hop nhat)\b', text)
    english = re.match(r'^(?:notes to (?:the )?)?(separate|consolidated) financial statements\b', text)
    statement = re.match(r'^(?:bang can doi ke toan|bao cao ket qua hoat dong kinh doanh|bao cao luu chuyen tien te) (rieng|hop nhat)\b', text)
    footer = re.search(r'\b(?:bo )?bao cao tai chinh (rieng|hop nhat) nay[. ]*$', text)
    match = report_title or english or statement or footer
    if not match:
        return None
    # A paragraph referring to both scopes is not a usable scope label.
    if re.search(r'\brieng\b', text) and re.search(r'\bhop nhat\b', text):
        return None
    scope = 'separate' if match.group(1) in ('rieng', 'separate') else 'consolidated'
    return {'scope': scope, 'source': block['source'], 'anchor_id': block['block_id'],
            'level': 'report_title' if report_title or english else 'page_statement'}


def resolve_scope(block, bundle):
    candidates = [c for b in bundle['source_blocks'] if b['kind'] == 'texts' and (c := scope_candidate(b))]
    local = [c for c in candidates if c['source']['pdf_page'] == block['source']['pdf_page']]
    # Local conflicting labels block fallback to the document title.
    selected = local or [c for c in candidates if c['level'] == 'report_title']
    values = {c['scope'] for c in selected}
    return {'value': next(iter(values)) if len(values) == 1 else None,
            'status': 'available' if len(values) == 1 else 'ambiguous' if values else 'unknown',
            'sources': [c['source'] for c in selected], 'anchor_ids': [c['anchor_id'] for c in selected],
            'basis': 'page_statement' if local else 'report_title' if selected else None}


def title_context(context):
    selected = None
    for block in context:
        raw = block.get('original_text') or ''
        text = normalized(raw)
        if (block.get('label') in ('section_header', 'title') or
                re.match(r'^(?:bang can doi ke toan|bao cao ket qua|bao cao luu chuyen|balance sheet|statement of|\d+[.)] )', text)):
            continuation = bool(re.search(r'tiep theo|continued|cont\.', text))
            title = re.sub(r'\(?\b(?:tiep theo|continued|cont\.)\)?', '', text).strip(' ():-')
            if title:
                selected = {'text': title, 'raw': raw, 'continued': continuation, 'source': block['source']}
    return selected


def column_count(block):
    return max((c['end_col_offset_idx'] for c in block['original_cells'] or []), default=0)


def header_signature(headers):
    result = {}
    for item in headers:
        cell = item['cell']
        for column in range(cell['start_col_offset_idx'], cell['end_col_offset_idx']):
            result.setdefault(column, []).append((cell['start_row_offset_idx'], normalized(cell.get('text', ''))))
    return {col: [text for _, text in sorted(values)] for col, values in result.items()}


def continuation_decision(previous, current, page_statuses, first_on_page, last_on_previous, unit_reader):
    """Require explicit continuation + same title/columns, reject conflicts/gaps."""
    prev, block = previous['block'], current['block']
    before, page = prev['source']['pdf_page'], block['source']['pdf_page']
    left, right = previous['title'], current['title']
    relevant = bool(right and right['continued']) or bool(left and right and left['text'] == right['text'])
    if not relevant:
        return None
    reasons = []
    if page != before + 1 or not first_on_page or not last_on_previous:
        reasons.append('not_adjacent_page_edge_tables')
    if page_statuses.get(before) != 'processed' or page_statuses.get(page) != 'processed':
        reasons.append('source_page_incomplete')
    if not left or not right or left['text'] != right['text'] or not right['continued']:
        reasons.append('explicit_matching_continuation_title_required')
    if not column_count(prev) or column_count(prev) != column_count(block):
        reasons.append('column_count_mismatch')
    if not previous['headers']:
        reasons.append('previous_header_mapping_missing')
    if current['headers'] and header_signature(previous['headers']) != header_signature(current['headers']):
        reasons.append('header_mapping_conflict')
    lscope, rscope = previous['scope'], current['scope']
    if lscope['status'] == 'ambiguous' or rscope['status'] == 'ambiguous' or (lscope['value'] and rscope['value'] and lscope['value'] != rscope['value']):
        reasons.append('statement_scope_conflict')
    units = []
    for item in (previous, current):
        context = [(b['original_text'] or '', b['source']) for b in item['context']]
        headers = [(h['cell'].get('text', ''), h['source']) for h in item['headers']]
        unit, scale, _ = unit_reader(context, headers)
        units.append((unit, scale))
        explicit_unit = any(re.match(r'^(?:don vi(?: tinh)?|unit)\s*[:：]|^(?:(?:trieu|ty|nghin|ngan|million|thousand|billion)\s+)?(?:vnd|usd|eur|dong)\s*$', normalized(raw)) for raw, _ in context)
        header_unit = any(re.search(r'\b(?:vnd|usd|eur|dong)\b', normalized(raw)) for raw, _ in headers)
        if (explicit_unit or header_unit) and unit is None:
            reasons.append('unit_context_ambiguous')
    if all(unit is not None for unit, _ in units) and units[0] != units[1]:
        reasons.append('unit_or_scale_conflict')
    return {'continuation_id': stable_id('continuation', prev['block_id'], block['block_id']),
            'from_table_anchor': prev['block_id'], 'to_table_anchor': block['block_id'],
            'status': 'rejected' if reasons else 'rule_matched', 'review_status': 'needs_review',
            'reasons': sorted(set(reasons)),
            'sources': [title['source'] for title in (left, right) if title]}
