from copy import deepcopy
from pathlib import Path

import pytest

from src.quality.oil_gold import (load_codebook, concept_candidates, applicability_dates,
                                  build_pack, release_check)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'a' * 64


@pytest.fixture
def book():
    return load_codebook(ROOT/'config/oil_gas_gold.yml')


def record(metric='GHG_SCOPE_2'):
    return {'source_sha256': SOURCE, 'physical_page': 1, 'anchor': '/tables/0/cells/1',
            'record_id': 'r1', 'record_type': 'measurement', 'fields': {'metric_id': metric, 'value': 123}}


def reviewed(name):
    return {'schema_version': 'esg-quality-gold/1.0', 'annotation_status': 'human_reviewed',
            'evaluation_units': [{'source_sha256': SOURCE, 'physical_page': 1, 'split': 'dev',
                'annotator': name, 'reviewed_against_pdf': True, 'fully_annotated': True,
                'record_types': ['claim'], 'items': [{'anchor': '/texts/0', 'record_type': 'claim',
                    'expected': {'text': 'Chính sách'}, 'reviewed_fields': ['text'],
                    'field_evidence': {'text': [{'source_sha256': SOURCE, 'physical_page': 1,
                        'anchor': '/texts/0', 'quote': 'Chính sách'}]},
                    'standards_annotation': {'concept_id': None, 'unknown_reasons': {'concept_id': 'Outside codebook scope'}}}]}]}


def final():
    f = reviewed('adjudicator')
    f['adjudication'] = {'reviewer': 'adjudicator', 'reviewed_against_pdf': True,
                         'reviewer_a_sha256': 'hash-a', 'reviewer_b_sha256': 'hash-b', 'decisions': []}
    return f


def check(f, a, b, book, **kwargs):
    return release_check(f, a, b, book, a_sha256='hash-a', b_sha256='hash-b', **kwargs)


def test_codebook_refs_and_no_money_headcount_equivalence(book):
    assert len(book['metrics']) >= 30
    assert concept_candidates(record('employee_payables'), book) == ['financial_employee_payables']
    assert book['metrics']['financial_employee_payables']['refs'][0]['relationship'] == 'not_equivalent'
    assert concept_candidates(record(), book) == ['scope2_location', 'scope2_market']
    assert concept_candidates(record(None), book) == []
    assert concept_candidates(record('local:employee_payables:v1'), book) == ['financial_employee_payables']
    hinted = record(None)
    hinted['label'] = 'Tổng lượng nước tiêu thụ'
    assert concept_candidates(hinted, book) == ['water_consumption']


def test_date_basis_not_reporting_year_and_not_adoption():
    a = applicability_dates(publication_date='2027-02-01', period_start='2026-01-01')
    assert a['gri102_103_by_publication_date'] is True
    assert a['s2_2025_amendments_by_period_start'] is False
    assert a['adoption_verified'] is False
    assert applicability_dates()['gri101_by_publication_date'] is None


def test_blind_drafts_do_not_inherit_prediction_or_promote(book):
    original = {'records': [record()]}
    before = deepcopy(original)
    draft, tasks, plan = build_pack(original, book)
    item = draft['evaluation_units'][0]['items'][0]
    assert draft['annotation_status'] == 'draft'
    assert item['expected'] == {} and item['standards_annotation']['concept_id'] is None
    assert 'suggested_prediction' not in item
    assert tasks[0]['extracted_suggestion']['value'] == 123 and tasks[0]['is_gold'] is False
    assert plan['precision'] is None and original == before
    with pytest.raises(ValueError, match='development'):
        build_pack(original, book, split='test', development_sources=[SOURCE])


def test_release_requires_independent_review_and_hashes(book):
    a, b, f = reviewed('one'), reviewed('two'), final()
    assert check(f, a, b, book)['status'] == 'PASS_MECHANICAL_GATES'
    b['evaluation_units'][0]['annotator'] = 'ONE'
    with pytest.raises(ValueError, match='distinct'):
        check(f, a, b, book)
    b['evaluation_units'][0]['annotator'] = 'two'
    f['adjudication']['reviewer_a_sha256'] = 'changed'
    with pytest.raises(ValueError, match='hash mismatch'):
        check(f, a, b, book)


def test_disagreement_and_added_or_removed_items_need_reason(book):
    a, b, f = reviewed('one'), reviewed('two'), final()
    b['evaluation_units'][0]['items'][0]['expected']['text'] = 'Other'
    with pytest.raises(ValueError, match='adjudication reason'):
        check(f, a, b, book)
    f['adjudication']['decisions'] = [{'locator': [SOURCE, 1, '/texts/0', 'claim'], 'reason': 'PDF transcription resolved by third reviewer'}]
    assert check(f, a, b, book)['adjudicated_differences'] == 1


@pytest.mark.parametrize('change', ['draft', 'no_pdf', 'partial', 'no_evidence', 'cross_source', 'null_no_reason'])
def test_release_blocks_incomplete_annotations(book, change):
    a, b, f = reviewed('one'), reviewed('two'), final()
    u = a['evaluation_units'][0]
    if change == 'draft': a['annotation_status'] = 'draft'
    if change == 'no_pdf': u['reviewed_against_pdf'] = False
    if change == 'partial': u['fully_annotated'] = False
    if change == 'no_evidence': u['items'][0]['field_evidence'] = {}
    if change == 'cross_source': u['items'][0]['field_evidence']['text'][0]['source_sha256'] = 'b'*64
    if change == 'null_no_reason': u['items'][0]['expected']['text'] = None
    with pytest.raises(ValueError):
        check(f, a, b, book)


def test_leakage_gate_and_full_scope_match(book):
    a, b, f = reviewed('one'), reviewed('two'), final()
    for g in (a, b, f): g['evaluation_units'][0]['split'] = 'test'
    with pytest.raises(ValueError, match='leakage'):
        check(f, a, b, book, development_sources=[SOURCE])
    b['evaluation_units'][0]['split'] = 'dev'
    with pytest.raises(ValueError, match='different page'):
        check(f, a, b, book)


def test_pending_sasb_cannot_be_declared_equivalent(book):
    a, b, f = reviewed('one'), reviewed('two'), final()
    item = a['evaluation_units'][0]['items'][0]
    item['standards_annotation'] = {'concept_id': 'scope1_gross', 'relationship': 'component_of',
        'references': [next(r for r in book['metrics']['scope1_gross']['refs'] if r['source']=='sasb_archive')]}
    with pytest.raises(ValueError, match='must remain unresolved'):
        check(f, a, b, book)


def test_duplicate_predictions_are_not_duplicate_reference_items(book):
    a, b = record(), record()
    b['record_id'] = 'r2'
    draft, tasks, plan = build_pack({'records': [a, b]}, book)
    assert len(tasks) == 2
    assert len(draft['evaluation_units'][0]['items']) == 1
    assert plan['duplicate_locator_candidates'] == 1
