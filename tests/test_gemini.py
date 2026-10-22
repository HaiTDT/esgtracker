"""No live Google calls: synthetic PDFs + controlled model responses only."""
import base64
import json
from pathlib import Path
import subprocess
import sys
from urllib.error import HTTPError

import pymupdf
import pytest

from src.extraction import gemini as g
from dashboard import upload_v2 as upload

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(autouse=True)
def no_live_google(monkeypatch):
    monkeypatch.delenv('GEMINI_API_KEY', raising=False)
    monkeypatch.delenv('GOOGLE_API_KEY', raising=False)
    monkeypatch.setattr(g.GeminiClient, 'generate', lambda *_: pytest.fail('Live Gemini call prohibited in tests'))


def pdf_file(tmp_path, pages=1):
    path = tmp_path / 'BSR_2024.pdf'
    with pymupdf.open() as pdf:
        for _ in range(pages):
            pdf.new_page().insert_text((30, 30), 'Revenue 2024 1,594 VND')
        pdf.save(path)
    return path


def response(page=1, financial=False):
    record = {'record_type': 'measurement', 'domain': 'financial' if financial else 'esg',
        'pillar': 'unknown' if financial else 'S', 'label_raw': 'Revenue', 'value_raw': '1,594',
        'unit_raw': 'VND', 'year': 2024, 'measurement_date': None, 'period_start': None,
        'period_end': None, 'reporting_entity': None, 'consolidation_raw': None, 'scope_raw': None,
        'interpretation_notes': [], 'evidence': [{'physical_page': page, 'role': role, 'quote': text}
            for role, text in [('label', 'Revenue'), ('value', '1,594'), ('unit', 'VND'), ('column_header', '2024')]]}
    return {'records': [record], 'page_reviews': [{'physical_page': page, 'status': 'read', 'note': ''}],
        'metadata': {'company_name': None, 'reporting_year': {'value': '2024', 'quote': '2024', 'physical_page': page},
                     'statement_scope': {'value': 'separate', 'quote': 'Separate financial statements separate', 'physical_page': page} if financial else None},
        'warnings': []}


def envelope(data, finish='STOP'):
    return {'candidates': [{'finishReason': finish, 'content': {'parts': [{'text': json.dumps(data)}]}}],
            'modelVersion': 'gemini-test-version', 'usageMetadata': {'totalTokenCount': 12}}


class FakeClient:
    def __init__(self, financial=False, transform=None):
        self.calls, self.financial, self.transform = [], financial, transform

    def generate(self, pdf, info, schema):
        with pymupdf.open(stream=pdf, filetype='pdf') as fragment:
            assert len(fragment) == len(info['fragment_page_mapping'])
        self.calls.append(info)
        data = response(info['primary_physical_pages'][0], self.financial)
        if self.transform:data = self.transform(data)
        return envelope(data)


def extract(tmp_path, pages=1, client=None, budget=None, financial=False, **kwargs):
    source = pdf_file(tmp_path, pages)
    client = client or FakeClient(financial)
    path = g.extract_pdf(source, tmp_path / 'cache', g.settings(), company_id='BSR',
        report_type='financial_statements' if financial else 'sustainability_report', report_year=2024,
        consent=True, budget=budget, client=client, number_format='en', **kwargs)
    return path, g.read_json(path), client


def test_consent_key_and_config_guards(tmp_path, monkeypatch):
    with pytest.raises(ValueError):g.GeminiClient(g.settings())
    with pytest.raises(ValueError, match='GEMINI_API_KEY'):g.GeminiClient(g.settings(), consent=True)
    monkeypatch.setenv('GEMINI_API_KEY', 'dummy-one')
    monkeypatch.setenv('GOOGLE_API_KEY', 'dummy-two')
    with pytest.raises(ValueError):g.api_key()
    for model in ['https://evil.invalid', '../x', 'gemini-key?secret=x']:
        with pytest.raises(ValueError):g.settings(model=model)
    for n in [0, -1, True, 10.0, 1001]:
        with pytest.raises(ValueError):g.Budget(n)
    with pytest.raises(ValueError):g.extract_pdf('absent.pdf', tmp_path, g.settings(), company_id='BSR', report_type='ESG', report_year=2024)
    assert not list(tmp_path.iterdir())


@pytest.mark.parametrize('finish', ['MAX_TOKENS', 'SAFETY', 'RECITATION', None])
def test_partial_response_never_success(finish):
    with pytest.raises(ValueError):g.decode_response(envelope(response(), finish))


def test_tool_safety_and_page_guards():
    bad = envelope(response())
    bad['candidates'][0]['content']['parts'] = [{'functionCall': {'name': 'run'}}]
    with pytest.raises(ValueError):g.decode_response(bad)
    for reviews in [[], [{'physical_page': 2, 'status': 'read', 'note': ''}]]:
        bad = response(); bad['page_reviews'] = reviews
        with pytest.raises(ValueError):g.check_batch(bad, [1], [1])
    bad = response(); bad['records'][0]['evidence'][0]['physical_page'] = 99
    with pytest.raises(ValueError):g.check_batch(bad, [1], [1])


def test_pdf_mapping_provenance_budget_and_resume(tmp_path):
    budget = g.Budget(1)
    path, data, client = extract(tmp_path, pages=3, budget=budget)
    assert len(client.calls) == 1 and budget.used == 1
    assert client.calls[0]['fragment_page_mapping'] == [
        {'fragment_page': 1, 'original_physical_page': 1}, {'fragment_page': 2, 'original_physical_page': 2}]
    assert data['coverage']['counts'] == {'processed': 1, 'pending': 2}
    r = data['records'][0]
    assert r['payload']['parsed_value'] == '1594'
    assert r['review'] == {'status': 'needs_review', 'verified_fields': []}
    assert r['boundary']['included_entities'] is None
    assert r['reported_entity'] is None and r['payload']['normalized_value'] is None
    assert r['gemini_evidence'][0]['source']['quote_check'] == 'matched_native_pdf_text'
    assert r['extraction_provenance']['is_gold'] is False
    next_client = FakeClient()
    resumed = g.extract_pdf(tmp_path / 'BSR_2024.pdf', tmp_path / 'cache', g.settings(), company_id='BSR',
        report_type='sustainability_report', report_year=2024, consent=True, client=next_client,
        budget=g.Budget(10), number_format='en')
    assert resumed == path and len(next_client.calls) == 2
    data = g.read_json(path)
    assert data['coverage']['counts'] == {'processed': 3}
    artifact = next(a for a in data['source_artifacts'] if a['kind'] == 'page_checkpoint')
    checkpoint = path.parent / artifact['path']
    checkpoint.write_bytes(checkpoint.read_bytes() + b' ')
    with pytest.raises(ValueError, match='checkpoint/PDF'):
        g.extract_pdf(tmp_path / 'BSR_2024.pdf', tmp_path / 'cache', g.settings(), company_id='BSR',
            report_type='sustainability_report', report_year=2024, consent=True, client=FakeClient(), number_format='en')


def test_dates_years_without_literal_evidence_stay_null(tmp_path):
    def transform(data):
        r = data['records'][0]
        r.update(measurement_date='2024-01-01', year=2023, reporting_entity='invented')
        r['evidence'].append({'physical_page': 1, 'role': 'date', 'quote': 'Số đầu năm'})
        return data
    _, data, _ = extract(tmp_path, client=FakeClient(transform=transform))
    r = data['records'][0]
    assert r['content_period'] is None and r['reported_entity'] is None
    assert sum(i['code'] == 'GEMINI_FIELD_UNPROVEN' for i in data['issues']) >= 3
    assert '/content_period' in r['missing_fields']


def test_explicit_dates_and_visual_unverified(tmp_path):
    def transform(data):
        r = data['records'][0]; r['measurement_date'] = '2024-12-31'
        r['evidence'].append({'physical_page': 1, 'role': 'date', 'quote': '31/12/2024'})
        return data
    _, data, _ = extract(tmp_path, client=FakeClient(transform=transform))
    r = data['records'][0]
    assert r['content_period']['as_of_date'] == '2024-12-31'
    assert r['gemini_evidence'][-1]['source']['quote_check'] == 'visual_unverified'
    assert not r['extraction_provenance']['factual_accuracy_verified']


def test_error_caps_stop_and_failures_saved(tmp_path):
    class Failure:
        def generate(self, *_):raise g.GeminiHTTPError(429)
    budget = g.Budget(5)
    _, data, _ = extract(tmp_path, pages=3, client=Failure(), budget=budget)
    assert budget.used == 1
    assert data['coverage']['counts'] == {'failed': 1, 'pending': 2}
    assert data['issues'][0]['code'] == 'GEMINI_BATCH_FAILED'


def test_request_reserved_before_api_call(tmp_path):
    class Inspect(FakeClient):
        def generate(self, *args):
            saved = list((tmp_path / 'cache').glob('**/batches/*.json'))
            assert len(saved) == 1
            assert g.read_json(saved[0])['attempts'][-1]['status'] == 'request_reserved'
            return super().generate(*args)
    extract(tmp_path, client=Inspect())


def test_cloud_upload_export_history_review_and_corporate(tmp_path, monkeypatch):
    from src.extraction.corporate_handoff import build_delivery
    from dashboard.extraction_history import load_saved_result
    from src.quality.records import native_snapshots
    source = pdf_file(tmp_path)
    original_load = upload.load_yaml
    monkeypatch.setattr(upload, 'load_yaml', lambda p: original_load(ROOT / 'config' / p.name))
    fake = FakeClient(financial=True)
    monkeypatch.setattr(g, 'GeminiClient', lambda *a, **kw: fake)
    content = 'data:application/pdf;base64,' + base64.b64encode(source.read_bytes()).decode()
    result = upload.process_upload_v2(tmp_path, [content], ['BSR_2024.pdf'], company='BSR', year=2024,
        report_type='financial_statements', engine='gemini', cloud_consent=True, number_format='en')
    assert result['manifest']['api_requests_used'] == 1
    assert result['documents'][0]['output']['provider'] == 'gemini_api'
    assert native_snapshots(result)[0]['extraction_provenance']['provider'] == 'gemini_api'
    portable = upload.export_result(result)
    assert 'gemini' in portable['pipeline']
    assert '_GEMINI_' in upload.download_filename(result)
    saved = load_saved_result(tmp_path, 'run:' + Path(result['run_directory']).name)
    assert saved['documents'][0]['output']['records'] == result['documents'][0]['output']['records']
    delivery = tmp_path / 'delivery'
    build_delivery(result, delivery)
    report = g.read_json(delivery / 'validation/report.json')
    assert report['mechanical_valid'] and report['human_review_pending']
    h = g.read_json(next((delivery / 'json').glob('*.json')))
    assert h['records'][0]['quality']['review_status'] == 'pending_human_review'
    assert h['records'][0]['value']['normalized_value'] == 1594
    check = subprocess.run([sys.executable, str(ROOT / 'scripts/audit_corporate_handoff.py'), str(delivery), '--pending-only'], capture_output=True, text=True, encoding='utf-8')
    assert check.returncode == 0, check.stdout + check.stderr
    audited = g.read_json(delivery / 'validation/extra_checks.json')
    assert audited['model_observation_quotes_checked'] == 4 and audited['native_quotes_checked'] == 0
    from scripts.quality_benchmark import predictions
    pred, _ = predictions(delivery)
    assert pred['records'] and not pred['ocr_pages']


def test_corporate_scope_unknown_blocks_but_native_survives(tmp_path):
    from src.extraction.gemini_handoff import convert
    def transform(data):data['metadata']['statement_scope'] = None; return data
    path, out, _ = extract(tmp_path, financial=True, client=FakeClient(financial=True, transform=transform))
    with pytest.raises(ValueError, match='riêng/hợp nhất'):
        convert({'output': out, 'workspace': str(path.parent), 'filename': 'BSR_2024.pdf'})
    assert path.is_file() and out['records']


def test_http_body_and_key_not_in_error_or_url(monkeypatch):
    monkeypatch.setenv('GEMINI_API_KEY', 'DUMMY-SECRET-TEST')
    # Exercise the real transport with a mocked opener, never a socket.
    client = g.GeminiClient(g.settings(), consent=True)
    def fake_open(request, **kwargs):
        assert 'DUMMY-SECRET-TEST' not in request.full_url
        assert request.get_header('X-goog-api-key') == 'DUMMY-SECRET-TEST'
        assert 'tools' not in json.loads(request.data)
        raise HTTPError(request.full_url, 403, 'blocked', {}, None)
    monkeypatch.setattr(client.opener, 'open', fake_open)
    # Fixture patched generate: restore the original method saved separately below.
    with pytest.raises(g.GeminiHTTPError) as exc:
        REAL_GENERATE(client, b'%PDF-test', {}, g.read_json(g.RESPONSE_SCHEMA))
    assert 'DUMMY-SECRET-TEST' not in str(exc.value)


REAL_GENERATE = g.GeminiClient.generate


def test_ui_consent_controls_and_request_settings(monkeypatch, tmp_path):
    from dash import Dash
    from dashboard import upload_analysis as ui
    app = Dash(__name__)
    app.layout = ui.upload_panel()
    ui.register_upload_callbacks(app, tmp_path)
    def callback(fragment):
        return next(v['callback'].__wrapped__ for k, v in app.callback_map.items() if fragment in k)
    start = callback('analysis-job.data')
    args = (1, ['dummy'], ['BSR_2024.pdf'], 'BSR', 2024, 'financial_statements', 'en')
    assert 'error' in start(*args, 'gemini', [], 'gemini-3.8-flash', 10)
    assert 'GEMINI_API_KEY' in start(*args, 'gemini', ['cloud'], 'gemini-3.8-flash', 10)['error']
    assert 'error' in start(*args, 'unknown')
    monkeypatch.setenv('GEMINI_API_KEY', 'DUMMY-SECRET')
    seen = []
    def fake_worker(*a, **kw):
        seen.append(kw)
        return {'status': 'failed', 'error': 'controlled fake'}
    class ImmediateThread:
        def __init__(self, target, **kw):self.target = target
        def start(self):self.target()
    monkeypatch.setattr(ui, 'run_isolated_upload', fake_worker)
    monkeypatch.setattr(ui.threading, 'Thread', ImmediateThread)
    job = start(*args, 'gemini', ['cloud'], 'gemini-3.8-flash', 3)
    try:
        assert seen == [{'engine': 'gemini', 'cloud_consent': True, 'gemini_model': 'gemini-3.8-flash', 'max_api_requests': 3}]
        assert 'DUMMY-SECRET' not in json.dumps(job)
        assert callback('analysis-gemini-settings.hidden')('docling') == (True, [])
        with app.server.test_client() as client:
            layout = client.get('/_dash-layout')
            assert layout.status_code == 200 and b'analysis-gemini-consent' in layout.data
    finally:ui.JOBS.pop(job['id'], None)


def test_worker_job_does_not_persist_key(tmp_path, monkeypatch):
    import uuid
    from dashboard.extraction_worker import run_isolated_upload, job_folder
    monkeypatch.setenv('GEMINI_API_KEY', 'DUMMY-DO-NOT-PERSIST')
    job = uuid.uuid4().hex
    run_isolated_upload(tmp_path, job, [], [], engine='gemini', cloud_consent=True,
        max_api_requests=2, worker_script=ROOT / 'tests/fixtures/isolated_worker_stub.py')
    request = (job_folder(tmp_path, job) / 'request.json').read_text(encoding='utf-8')
    assert 'DUMMY-DO-NOT-PERSIST' not in request
    assert json.loads(request)['engine'] == 'gemini'
    assert json.loads(request)['max_api_requests'] == 2


def test_history_immutable_when_cache_resumed(tmp_path, monkeypatch):
    source = pdf_file(tmp_path, pages=2)
    original_load = upload.load_yaml
    monkeypatch.setattr(upload, 'load_yaml', lambda p: original_load(ROOT / 'config' / p.name))
    fake = FakeClient()
    monkeypatch.setattr(g, 'GeminiClient', lambda *a, **kw: fake)
    content = 'data:application/pdf;base64,' + base64.b64encode(source.read_bytes()).decode()
    kwargs = dict(company='BSR', year=2024, report_type='ESG', engine='gemini', cloud_consent=True, number_format='en')
    first = upload.process_upload_v2(tmp_path, [content], [source.name], max_api_requests=1, **kwargs)
    first_path = Path(first['documents'][0]['output_path'])
    before = first_path.read_bytes()
    second = upload.process_upload_v2(tmp_path, [content], [source.name], max_api_requests=2, **kwargs)
    assert first['documents'][0]['workspace'] != second['documents'][0]['workspace']
    assert first_path.read_bytes() == before
    assert first['documents'][0]['coverage']['counts']['pending'] == 1
    assert second['documents'][0]['coverage']['counts'] == {'processed': 2}
    assert len(fake.calls) == 2
    assert upload.export_result(first) and upload.export_result(second)


def test_context_only_and_unreadable_do_not_create_records(tmp_path):
    def transform(data):
        data['page_reviews'][0]['status'] = 'unreadable'
        return data
    _, data, _ = extract(tmp_path, client=FakeClient(transform=transform))
    assert not data['records'] and data['coverage']['counts'] == {'failed': 1}
    assert any(i['code'] == 'GEMINI_PAGE_UNREADABLE' for i in data['issues'])


def test_cli_check_config_never_calls_api(monkeypatch, capsys):
    from scripts.extract_gemini import main
    assert main(['--check-config']) == 1
    assert json.loads(capsys.readouterr().out)['network_requests'] == 0
    monkeypatch.setenv('GEMINI_API_KEY', 'DUMMY-CONFIG')
    assert main(['--check-config']) == 0
    assert 'DUMMY-CONFIG' not in capsys.readouterr().out
    assert main([]) == 2


def test_stray_scope_word_does_not_establish_statement_scope(tmp_path):
    def transform(data):
        data['metadata']['statement_scope'] = {'value': 'riêng', 'quote': 'tính riêng cho lao động', 'physical_page': 1}
        return data
    _, data, _ = extract(tmp_path, financial=True, client=FakeClient(financial=True, transform=transform))
    assert data['metadata']['statement_scope']['value'] is None
