import copy
import json
from pathlib import Path

import pymupdf
import pytest

from src.extraction import local_llm as llm
from src.extraction.source_v2 import capture_pdf


def settings(**changes):
    return llm.load_settings(**changes)


@pytest.mark.parametrize('url', ['https://api.example.com', 'http://192.168.1.2:11434',
    'http://0.0.0.0:11434', 'http://127.0.0.1:11434/api', 'http://user:pass@localhost:11434',
    'http://127.0.0.1:11434?x=y', 'file:///C:/x', 'http://localhost', 'http://localhost.evil:11434'])
def test_remote_credentials_and_unsafe_origins_rejected(url):
    with pytest.raises(ValueError):llm.validate_url(url)


@pytest.mark.parametrize('url', ['http://127.0.0.1:11434', 'http://localhost:11434', 'http://[::1]:11434'])
def test_loopback_origins_allowed(url):
    assert llm.validate_url(url) == url


def test_model_not_installed_is_not_downloaded(monkeypatch):
    client = llm.OllamaClient(settings())
    calls = []
    def request(path, body=None):
        calls.append(path)
        return {'models': []}
    monkeypatch.setattr(client, 'request', request)
    with pytest.raises(ValueError, match='No automatic pull'):client.preflight()
    assert calls == ['/api/tags']


def test_cloud_alias_with_local_endpoint_rejected(monkeypatch):
    client = llm.OllamaClient(settings())
    monkeypatch.setattr(client, 'request', lambda *_: {'models': [{'name': 'llama3:8b', 'size': 1,
        'digest': 'a' * 64, 'remote_host': 'remote.invalid'}]})
    with pytest.raises(ValueError, match='remote models prohibited'):client.preflight()


@pytest.mark.parametrize('change', [{'model': 'x:cloud'}, {'num_ctx': 100}, {'num_predict': 8192},
                                   {'retries': -1}, {'max_chunk_chars': 2}, {'number_format': 'guess'}])
def test_bad_settings_rejected(change):
    with pytest.raises(ValueError):settings(**change)


def source_catalog(text='Tổng số lao động năm 2025: 1.594 người'):
    return {'s000000': {'source_id': 's000000', 'text': text, 'physical_page': 1,
        'block_id': 'b', 'text_span': [0, len(text)], 'source': {'native_json_pointer': '/document/texts/0',
        'artifact_id': 'a', 'artifact_sha256': 'a' * 64, 'pdf_page': 1}, 'kind': 'texts', 'label': 'text', 'cell': None}}


def response():
    text = 'Tổng số lao động năm 2025: 1.594 người'
    return {'candidates': [{'record_type': 'measurement', 'domain': 'esg', 'pillar': 'S',
        'label': 'Tổng số lao động', 'evidence': [{'source_id': 's000000', 'quote': text}],
        'fields': {'value_raw': {'value': '1.594', 'source_id': 's000000', 'quote': '1.594'},
                   'year': {'value': 2025, 'source_id': 's000000', 'quote': 'năm 2025'},
                   'unit_raw': {'value': 'người', 'source_id': 's000000', 'quote': 'người'}}, 'notes': []}],
        'warnings': []}


def validate(value):
    return llm.validate_candidates(value, llm.read_json(llm.SCHEMA_PATH), source_catalog(),
        {'primary_source_ids': ['s000000'], 'context_source_ids': [], 'chunk_id': 'chunk1'},
        {'source_sha256': 'a' * 64, 'company_id': 'INPUT_BSR'}, 'vi')


def test_source_bound_measurement_and_unknown_boundary():
    records, rejected = validate(response())
    assert not rejected
    r = records[0]
    assert r['fields']['value_raw'] == '1.594' and r['parsed_value'] == '1594'
    assert r['fields']['year'] == 2025
    assert r['fields']['reporting_entity'] is None
    assert r['normalization']['normalized_value'] is None
    assert r['quality']['review_status'] == 'pending_human_review'
    assert r['quality']['boundary_verified'] is False and r['quality']['verdict'] is None


def test_hallucinated_year_is_cleared_not_report_year():
    data = response()
    data['candidates'][0]['fields']['year']['value'] = 2024
    records, _ = validate(data)
    assert records[0]['fields']['year'] is None
    assert 'year' in records[0]['missing_fields']
    assert records[0]['issues'][0]['code'] == 'FIELD_EVIDENCE_REJECTED'


def test_hallucinated_numeric_value_cannot_be_measurement():
    data = response()
    data['candidates'][0]['fields']['value_raw']['value'] = '1594'
    records, rejected = validate(data)
    assert not records and 'no source-bound' in rejected[0]['reason']


def test_invented_quote_and_source_are_quarantined():
    for citation in ({'source_id': 's000000', 'quote': 'không có ở nguồn'}, {'source_id': 's999999', 'quote': 'người'}):
        data = response()
        data['candidates'][0]['evidence'] = [citation]
        records, rejected = validate(data)
        assert not records and rejected


def test_extra_verdict_or_tools_fields_schema_rejected():
    data = response()
    data['candidates'][0]['verdict'] = 'Contradicted'
    with pytest.raises(ValueError, match='schema invalid'):validate(data)


def test_headings_and_standard_labels_are_not_claims():
    data = response()
    schema = llm.read_json(llm.SCHEMA_PATH)
    for text, label in [('Tổng số lao động năm 2025: 1.594 người', 'section_header'),
                        ('GRI 3-3; GRI 401, GRI 404, GRI 405', 'text')]:
        sources = source_catalog(text)
        sources['s000000']['label'] = label
        candidate = copy.deepcopy(data)
        candidate['candidates'][0].update(record_type='claim', label=text, fields={},
            evidence=[{'source_id': 's000000', 'quote': text}])
        records, rejected = llm.validate_candidates(candidate, schema, sources,
            {'primary_source_ids': ['s000000'], 'context_source_ids': [], 'chunk_id': 'c'},
            {'source_sha256': 'a' * 64}, 'vi')
        assert not records and rejected


def test_standards_mention_in_actual_narrative_is_not_blanket_excluded():
    assert llm.standards_label_only('GRI 401; GRI 404')
    assert not llm.standards_label_only('GRI 401 được tham chiếu trong chính sách lao động')


def test_standards_label_with_trailing_ocr_icon_noise_is_rejected():
    text = 'GRI 3-3: GRI 401, GRI 404, GRI 405 t)'
    data = response()
    data['candidates'][0].update(record_type='claim', label='GRI 3-3: GRI 401, GRI 404, GRI 405',
        fields={}, evidence=[{'source_id': 's000000', 'quote': text}])
    records, rejected = llm.validate_candidates(data, llm.read_json(llm.SCHEMA_PATH), source_catalog(text),
        {'primary_source_ids': ['s000000'], 'context_source_ids': [], 'chunk_id': 'c'},
        {'source_sha256': 'a' * 64}, 'vi')
    assert not records and 'Standards index' in rejected[0]['reason']


def test_generation_truncation_is_failure(monkeypatch):
    client = llm.OllamaClient(settings())
    monkeypatch.setattr(client, 'request', lambda *_: {'done': True, 'done_reason': 'length', 'message': {'content': '{}'}})
    with pytest.raises(ValueError, match='truncated'):client.generate({}, {})


def test_redirect_is_blocked():
    with pytest.raises(ValueError, match='redirects'):
        llm.NoRedirect().redirect_request(None, None, 302, 'redirect', {}, 'https://remote.invalid')


def test_long_text_no_silent_clipping_and_stable_chunk_ids():
    text = 'Dữ liệu nguồn. ' * 500
    bundle = {'source_blocks': [{'kind': 'texts', 'label': 'text', 'original_text': text,
        'source': {'native_json_pointer': '/document/texts/0', 'pdf_page': 1}, 'block_id': 'b'}]}
    sources, chunks = llm.build_chunks(bundle, 700)
    assert ''.join(s['text'] for s in sources.values()) == text
    assert [i for c in chunks for i in c['primary_source_ids']] == list(sources)
    assert (sources, chunks) == llm.build_chunks(bundle, 700)


class FakeClient:
    def __init__(self, fail=False):self.calls = 0; self.fail = fail
    def preflight(self):return {'name': 'test-local', 'digest': 'b' * 64, 'size': 1}
    def generate(self, payload, schema):
        self.calls += 1
        if self.fail:raise RuntimeError('deliberate fixture failure')
        return json.dumps({'candidates': [], 'warnings': []}), {'eval_count': 3}


def fixture_workspace(tmp_path):
    pdf = tmp_path / 'source.pdf'
    with pymupdf.open() as document:
        document.new_page()
        document.new_page()
        document.save(pdf)
    def reader(path, number):
        return {'status': 'processed', 'document': {'texts': [{'text': f'Source paragraph {number}', 'label': 'text'}]}, 'markdown': 'source'}
    return capture_pdf(pdf, tmp_path / 'source', company_id='BSR', report_type='annual_report', report_year=2025,
                       page_reader=reader, profile={'engine': 'local-llm-tests'})


def test_limit_keeps_pending_then_resume_no_duplicate_calls(tmp_path):
    work = fixture_workspace(tmp_path)
    client = FakeClient()
    path = llm.extract_local_llm(work, tmp_path / 'llm', settings(), max_chunks=1, client=client)
    data = llm.read_json(path)
    assert data['coverage']['counts'] == {'processed': 1, 'pending': 1}
    assert data['coverage']['text_pass_complete'] is False
    assert client.calls == 1
    llm.extract_local_llm(work, tmp_path / 'llm', settings(), client=client)
    assert client.calls == 2
    data = llm.read_json(path)
    assert data['coverage']['text_pass_complete'] is True
    assert data['coverage']['semantic_completeness_verified'] is False
    llm.extract_local_llm(work, tmp_path / 'llm', settings(), client=client)
    assert client.calls == 2


def test_checkpoint_tamper_blocks_resume(tmp_path):
    work = fixture_workspace(tmp_path)
    path = llm.extract_local_llm(work, tmp_path / 'llm', settings(), client=FakeClient())
    data = llm.read_json(path)
    cp = path.parent / data['coverage']['chunks'][0]['checkpoint']
    cp.write_bytes(cp.read_bytes() + b' ')
    with pytest.raises(ValueError, match='checkpoint hash/path changed'):
        llm.extract_local_llm(work, tmp_path / 'llm', settings(), client=FakeClient())


def test_failed_chunks_retry_without_discarding_plan(tmp_path):
    work = fixture_workspace(tmp_path)
    client = FakeClient(fail=True)
    path = llm.extract_local_llm(work, tmp_path / 'llm', settings(retries=1), client=client)
    data = llm.read_json(path)
    assert client.calls == 4
    assert data['coverage']['counts'] == {'failed': 2}
    assert data['records'] == []
    assert data['graph_ready'] is False
    assert all(i['code'] == 'LLM_CHUNK_FAILED' for i in data['issues'])


def test_smoke_limit_does_not_hide_previous_unselected_failure(tmp_path):
    work = fixture_workspace(tmp_path)
    path = llm.extract_local_llm(work, tmp_path / 'llm', settings(), client=FakeClient(fail=True))
    llm.extract_local_llm(work, tmp_path / 'llm', settings(), max_chunks=1, client=FakeClient())
    assert llm.read_json(path)['coverage']['counts'] == {'processed': 1, 'failed': 1}
