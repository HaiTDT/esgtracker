"""Standards-assisted, deliberately non-gold annotation packs and release gates.

The codebook never changes production extraction rules or fills reference values.
Reviewer identities are declarations; these gates are not authentication.
"""
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import date
from hashlib import sha256
import json
import math
import re
from pathlib import Path

import yaml

from src.quality.evaluation import make_template, location
from src.quality.records import FIELDS, required_fields


def load_codebook(path):
    book = yaml.safe_load(Path(path).read_text(encoding='utf-8'))
    if book.get('schema_version') != 'oil-gas-codebook/1.0':
        raise ValueError('Unsupported oil codebook.')
    for concept, spec in book['metrics'].items():
        if not spec['refs'] or not spec['units']:
            raise ValueError(f'Missing reference/unit: {concept}')
        for ref in spec['refs'] + spec.get('future_refs', []):
            if ref['source'] not in book['sources']:
                raise ValueError(f'Unknown source: {concept}')
    return book


def concept_candidates(row, book):
    """ID links/text hints for discovery ONLY, never reference answers."""
    metric = row.get('fields', {}).get('metric_id')
    linked = {k for k, spec in book['metrics'].items() if metric and
              any(metric in (alias, f'local:{alias}:v1') for alias in spec['aliases'])}
    text = (row.get('label', '') + ' ' + (row.get('fields', {}).get('text') or '')).casefold()
    hinted = {k for k, pattern in book.get('discovery_hints', {}).items() if re.search(pattern, text)}
    if linked & {'financial_employee_payables', 'financial_employee_advances'} or re.search('phải trả người lao động|tạm ứng cho nhân viên', text):
        hinted.discard('employee_count')
    return sorted(linked | hinted)


def applicability_dates(*, publication_date=None, period_start=None):
    """Date eligibility is NOT legal adoption, materiality, or declared compliance."""
    publication = date.fromisoformat(publication_date) if publication_date else None
    period = date.fromisoformat(period_start) if period_start else None
    def eligible(value, threshold):
        return None if value is None else value >= date.fromisoformat(threshold)
    return {'gri101_by_publication_date': eligible(publication, '2026-01-01'),
            'gri102_103_by_publication_date': eligible(publication, '2027-01-01'),
            'ifrs_s1_s2_by_period_start': eligible(period, '2024-01-01'),
            's2_2025_amendments_by_period_start': eligible(period, '2027-01-01'),
            'adoption_verified': False,
            'caution': 'Confirm declared edition, early application, jurisdiction and materiality. Never infer KPI scope from a standard.'}


def build_pack(prediction_data, book, *, pages=24, split='dev', development_sources=()):
    if pages < 1 or split not in ('train', 'dev', 'test'):
        raise ValueError('Invalid page limit/split.')
    records = prediction_data['records']
    known = set(development_sources)
    if split == 'test' and known & {r['source_sha256'] for r in records}:
        raise ValueError('Known development PDFs cannot be held-out test sources.')
    draft = make_template(records, split)
    groups = defaultdict(list)
    row_index = {(r['source_sha256'], r['record_id']): r for r in records}
    for unit in draft['evaluation_units']:
        concepts = {c for item in unit['items'] for c in concept_candidates(
            row_index[(unit['source_sha256'], item['suggested_record_id'])], book)}
        groups[unit['source_sha256']].append((len(concepts), unit))
    # Cover sources first, prioritise concept-bearing pages within each source.
    # Never claim representative random sampling or corpus recall.
    for source in groups:
        groups[source].sort(key=lambda x: (-x[0], x[1]['physical_page']))
    chosen = []
    while len(chosen) < pages and any(groups.values()):
        for source in sorted(groups):
            if groups[source] and len(chosen) < pages:
                chosen.append(groups[source].pop(0)[1])
    tasks = []
    duplicates = 0
    for unit in chosen:
        seen = set()
        unique = []
        for item in unit['items']:
            row = row_index[(unit['source_sha256'], item['suggested_record_id'])]
            choices = concept_candidates(row, book)
            tasks.append({'source_sha256': unit['source_sha256'], 'physical_page': unit['physical_page'],
                          'anchor': item['anchor'], 'record_type': item['record_type'],
                          'record_id': row['record_id'], 'candidate_concepts': choices,
                          'extracted_suggestion': deepcopy(row['fields']), 'is_gold': False})
            key = (item['anchor'], item['record_type'])
            if key in seen:
                duplicates += 1
                continue
            seen.add(key)
            unique.append(item)
            item.pop('suggested_prediction', None)
            item['standards_annotation'] = {'concept_id': None, 'relationship': None,
                                           'references': [], 'qualifiers': {}, 'unknown_reasons': {},
                                           'edition_adoption_evidence': None}
            item['field_evidence'] = {}
            item['unknown_reasons'] = {}
        unit['items'] = unique
        unit['annotation_note'] = 'Inspect the full page, headers, footnotes and linked boundary pages; add missed items and remove false candidates. Blind draft contains no suggested values.'
    draft.update(evaluation_units=chosen, development_source_sha256=sorted(known),
                 codebook_version=book['schema_version'], codebook_status=book['status'],
                 profile_selection={'industry': None, 'profile': None, 'publication_date': None,
                                    'period_start': None, 'adoption_verified': False},
                 adjudication={'reviewer': None, 'reviewed_against_pdf': False,
                               'reviewer_a_sha256': None, 'reviewer_b_sha256': None, 'decisions': []})
    counts = Counter(c for t in tasks for c in t['candidate_concepts'])
    plan = {'schema_version': 'oil-gas-annotation-plan/1.0', 'is_gold': False,
            'selected_pages': len(chosen), 'selected_sources': len({u['source_sha256'] for u in chosen}),
            'candidate_items': len(tasks),
            'unique_annotation_items': sum(len(u['items']) for u in chosen),
            'duplicate_locator_candidates': duplicates,
            'sampling_limits': 'Purposive candidate-bearing pages only. Add independent empty, scan, chart, missing-item and non-BSR test pages before claiming general accuracy.',
            'concept_coverage': {c: {'suggested_candidates': counts[c],
                'status': 'candidates_need_review' if counts[c] else 'not_sampled_or_not_detected_not_absent',
                'qualifiers_to_label': book['common_qualifiers'] + s['qualifiers']}
                for c, s in book['metrics'].items()},
            'release_status': 'DRAFT_NOT_GOLD', 'precision': None,
            'sasb_limit': 'Full SASB protocols not acquired; protocol_pending mappings cannot establish standard equivalence.'}
    return draft, tasks, plan


def _items(gold, book):
    if gold.get('schema_version') != 'esg-quality-gold/1.0' or gold.get('annotation_status') != 'human_reviewed':
        raise ValueError('Requires human_reviewed annotation, not a draft.')
    entries, scopes, reviewers = {}, set(), set()
    def evidence_valid(evidence, source):
        return bool(evidence) and all(isinstance(e, dict) and isinstance(e.get('quote'), str)
            and e['quote'].strip() and isinstance(e.get('anchor'), str) and e['anchor'].strip()
            and type(e.get('physical_page')) is int and e['physical_page'] > 0
            and e.get('source_sha256') == source for e in evidence)
    for unit in gold['evaluation_units']:
        reviewer = (unit.get('annotator') or '').strip()
        if not reviewer or unit.get('reviewed_against_pdf') is not True or unit.get('fully_annotated') is not True:
            raise ValueError('Each released page/type scope must be fully annotated against PDF by a named reviewer.')
        reviewers.add(reviewer.casefold())
        if not re.fullmatch(r'[0-9a-f]{64}', unit.get('source_sha256', '')) or type(unit.get('physical_page')) is not int or unit['physical_page'] < 1:
            raise ValueError('Invalid source hash/physical page.')
        if not unit.get('record_types') or unit.get('split') not in ('train', 'dev', 'test'):
            raise ValueError('Missing record types/split.')
        for kind in unit['record_types']:
            scope = (unit['source_sha256'], unit['physical_page'], kind, unit['split'])
            if scope in scopes:
                raise ValueError('Overlapping annotation scope.')
            scopes.add(scope)
        for item in unit['items']:
            key = (unit['source_sha256'], unit['physical_page'], item['anchor'], item['record_type'])
            if key in entries or not item['anchor'] or item['record_type'] not in unit['record_types']:
                raise ValueError('Duplicate/invalid locator.')
            expected = item.get('expected', {})
            if not set(required_fields(item)) <= set(expected) or set(expected) - set(FIELDS):
                raise ValueError('Incomplete expected extraction fields.')
            if not set(expected) <= set(item.get('reviewed_fields', [])):
                raise ValueError('Unreviewed expected fields.')
            if expected.get('value') is not None and (isinstance(expected['value'], bool)
                or not isinstance(expected['value'], (int, float)) or not math.isfinite(expected['value'])):
                raise ValueError('Expected value must be finite numeric or null.')
            if expected.get('observation_year') is not None and (type(expected['observation_year']) is not int or not 1900 <= expected['observation_year'] <= 2200):
                raise ValueError('Invalid observation year.')
            for field, value in expected.items():
                if value is None:
                    if not item.get('unknown_reasons', {}).get(field, '').strip():
                        raise ValueError(f'Null {field} requires an explicit reason.')
                    continue
                evidence = item.get('field_evidence', {}).get(field, [])
                if not evidence_valid(evidence, unit['source_sha256']):
                    raise ValueError(f'{field} requires same-source PDF page/anchor/verbatim quote; cross-report inference is not allowed.')
            ann = item.get('standards_annotation', {})
            concept = ann.get('concept_id')
            if concept is None:
                if not ann.get('unknown_reasons', {}).get('concept_id', '').strip():
                    raise ValueError('Unmapped concept needs a reason.')
            else:
                if concept not in book['metrics']:
                    raise ValueError('Unknown codebook concept.')
                spec = book['metrics'][concept]
                allowed = spec['refs'] + spec.get('future_refs', [])
                if not ann.get('references') or any(r not in allowed for r in ann['references']):
                    raise ValueError('References must be versioned codebook references.')
                if ann.get('relationship') not in ('component_of', 'conditional_overlap', 'related_not_equivalent', 'not_equivalent', 'unresolved'):
                    raise ValueError('Missing/invalid standard relationship.')
                # This release supports extraction gold with unresolved mappings,
                # not a claim of complete SASB compliance.
                if any(r['relationship'] in ('protocol_pending', 'candidate_component') for r in ann['references']) and ann['relationship'] != 'unresolved':
                    raise ValueError('SASB/full-protocol pending reference must remain unresolved.')
                for qualifier in book['common_qualifiers'] + spec['qualifiers']:
                    if ann.get('qualifiers', {}).get(qualifier) is None:
                        if not ann.get('unknown_reasons', {}).get(qualifier, '').strip():
                            raise ValueError(f'Unknown qualifier {qualifier} needs a reason (including not applicable).')
                    elif not evidence_valid(item.get('field_evidence', {}).get('qualifier:' + qualifier, []), unit['source_sha256']):
                        raise ValueError(f'Known qualifier {qualifier} requires evidence.')
            entries[key] = {'expected': expected, 'standards_annotation': ann,
                            'field_evidence': item.get('field_evidence'), 'unknown_reasons': item.get('unknown_reasons')}
    if not scopes:
        raise ValueError('Empty benchmark scope.')
    return entries, scopes, reviewers


def verify_source_delivery(path, golds=()):
    """Read-only original-PDF hashes and page-range gate, including footnote pages."""
    import pymupdf
    root = Path(path).resolve()
    manifest = json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    inventory = {}
    for row in manifest['files']:
        if row['status'] == 'unavailable':
            continue
        target = (root/row['pdf_path']).resolve()
        if not target.is_relative_to(root) or sha256(target.read_bytes()).hexdigest() != row['pdf_sha256']:
            raise ValueError('Original PDF path/hash mismatch.')
        with pymupdf.open(target) as pdf:
            inventory[row['pdf_sha256']] = {'pdf_path': row['pdf_path'], 'pages': len(pdf), 'sha256_verified': True}
    for gold in golds:
        for unit in gold['evaluation_units']:
            source = unit['source_sha256']
            if source not in inventory or not 1 <= unit['physical_page'] <= inventory[source]['pages']:
                raise ValueError('Gold page/source not present in verified original PDFs.')
            for item in unit['items']:
                for evidence in item.get('field_evidence', {}).values():
                    for e in evidence:
                        if e.get('source_sha256') != source or type(e.get('physical_page')) is not int or not 1 <= e['physical_page'] <= inventory[source]['pages']:
                            raise ValueError('Evidence source/page not present in verified PDFs.')
    return inventory


def release_check(final, reviewer_a, reviewer_b, book, *, a_sha256, b_sha256, development_sources=()):
    """Validate independent declarations; never promote a draft or write gold."""
    a, sa, ra = _items(reviewer_a, book)
    b, sb, rb = _items(reviewer_b, book)
    resolved, sf, rf = _items(final, book)
    if ra & rb:
        raise ValueError('Reviewer A and B must be distinct.')
    if not sa == sb == sf:
        raise ValueError('Independent annotations/adjudication have different page/type/split scopes.')
    development = set(development_sources)
    for g in (final, reviewer_a, reviewer_b):
        development.update(g.get('development_source_sha256', []))
    development |= {s[0] for s in sf if s[3] in ('train', 'dev')}
    if development & {s[0] for s in sf if s[3] == 'test'}:
        raise ValueError('Development/test source leakage.')
    adj = final.get('adjudication', {})
    if not (adj.get('reviewer') or '').strip() or adj.get('reviewed_against_pdf') is not True:
        raise ValueError('Missing PDF adjudication declaration.')
    if adj.get('reviewer_a_sha256') != a_sha256 or adj.get('reviewer_b_sha256') != b_sha256:
        raise ValueError('Independent annotation hash mismatch.')
    decisions = {tuple(d['locator']): d for d in adj.get('decisions', [])}
    disagreements = 0
    for key in set(a) | set(b) | set(resolved):
        # Evidence wording/locators may differ; compare actual semantic answers.
        answer = lambda row: None if row is None else (row['expected'], row['standards_annotation'])
        if answer(a.get(key)) != answer(b.get(key)) or answer(resolved.get(key)) != answer(a.get(key)):
            disagreements += 1
            if not decisions.get(key, {}).get('reason', '').strip():
                raise ValueError('Every disagreement/addition/removal needs an adjudication reason.')
    if not resolved:
        raise ValueError('Cannot release an empty gold set.')
    return {'schema_version': 'oil-gas-gold-release/1.0', 'status': 'PASS_MECHANICAL_GATES',
            'records': len(resolved), 'page_type_units': len(sf), 'adjudicated_differences': disagreements,
            'independent_annotators': sorted(ra | rb), 'adjudicators': sorted(rf),
            'precision': None, 'identity_verified': False,
            'limits': 'Human declarations, not independent identity or source-truth certification. Run quality_benchmark evaluate on separately captured predictions. Unresolved SASB remains unresolved.'}
