import importlib.util
import json
from pathlib import Path
import zipfile

import pytest

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_handover_local_links_evidence_examples():
    report = load('check_handover').check()
    assert report['passed'], report['errors']


def test_three_type_offline_smoke_and_no_overwrite(tmp_path):
    script = load('handover_smoke')
    result = script.run(tmp_path / 'smoke')
    assert result['status'] == 'PASS' and result['external_api_requests'] == 0
    assert not result['real_ocr_verified'] and not result['accuracy_measured']
    assert {r['report_type'] for r in result['reports']} == {'financial_statements', 'ESG', 'annual_report'}
    assert all(r['records'] > 0 and r['schema_valid'] for r in result['reports'])
    with pytest.raises(FileExistsError):script.run(tmp_path / 'smoke')


def fixture_source(tmp_path):
    root = tmp_path / 'repo'
    root.mkdir()
    (root / 'README.md').write_text('# Synthetic package test', encoding='utf-8')
    (root / 'app.py').write_text('# Synthetic entry point', encoding='utf-8')
    (root / '.env.example').write_text('GEMINI_API_KEY=\n', encoding='utf-8')
    for path, data in [('src/a.py', 'answer = 1'), ('docs/reference/component-inventory.csv', 'component,role\n'), ('data/client.json', 'PRIVATE DATA'),
                       ('docs/client.pdf', 'REPORT'), ('database/esg_tracker.db', 'DATABASE'),
                       ('src/__pycache__/a.pyc', 'CACHE'), ('config/credentials.json', 'CREDENTIALS')]:
        target = root / path;target.parent.mkdir(parents=True, exist_ok=True);target.write_text(data, encoding='utf-8')
    return root


def test_packaging_allowlist_hash_manifest_and_reproducibility(tmp_path):
    script = load('package_handover')
    root = fixture_source(tmp_path)
    first = script.package(root, tmp_path / 'out1', '0.1.0-test.1')
    second = script.package(root, tmp_path / 'out2', '0.1.0-test.1')
    assert first['sha256'] == second['sha256']
    with zipfile.ZipFile(first['archive']) as zipped:
        names = zipped.namelist()
        assert any(n.endswith('/src/a.py') for n in names)
        assert any(n.endswith('/app.py') for n in names)
        assert any(n.endswith('/component-inventory.csv') for n in names)
        assert not any(n.endswith(('.pdf', '.db', '.pyc')) or '/data/' in n or 'credentials.json' in n for n in names)
        manifest = json.loads(zipped.read(next(n for n in names if n.endswith('PACKAGE_MANIFEST.json'))))
        assert manifest['kind'] == 'INTERNAL_REVIEW_NOT_PUBLIC_RELEASE'
        assert manifest['release_blockers']


def test_packaging_secret_error_does_not_echo_value(tmp_path):
    script = load('package_handover')
    root = fixture_source(tmp_path)
    secret = 'AIza' + 'X' * 35
    (root / 'src/a.py').write_text('value = ' + repr(secret))
    with pytest.raises(ValueError) as exc:script.package(root, tmp_path / 'out', '0.1.0-test')
    assert secret not in str(exc.value)
    assert not (tmp_path / 'out').exists()


@pytest.mark.parametrize('version', ['../x', 'https://x', '1/2/3', ''])
def test_packaging_bad_versions_rejected(tmp_path, version):
    script = load('package_handover')
    with pytest.raises(ValueError):script.package(fixture_source(tmp_path), tmp_path / 'out', version)


def test_packaging_destinations_empty_env_and_dry_run(tmp_path):
    script = load('package_handover')
    root = fixture_source(tmp_path)
    with pytest.raises(ValueError):script.package(root, root / 'dist', '0.1.0')
    with pytest.raises(ValueError):script.package(root, tmp_path, '0.1.0')
    script.package(root, tmp_path / 'exists', '0.1.0')
    with pytest.raises(ValueError):script.package(root, tmp_path / 'exists', '0.1.0')
    assert script.package(root, tmp_path / 'dry', '0.1.0', dry_run=True)['scan']['known_secret_patterns_found'] == 0
    assert not (tmp_path / 'dry').exists()
    (root / '.env.example').write_text('GEMINI_API_KEY=DO_NOT_USE\n')
    with pytest.raises(ValueError):script.package(root, tmp_path / 'secret', '0.1.0')


def test_packager_does_not_traverse_junction_classified_directory(tmp_path, monkeypatch):
    script = load('package_handover')
    root = fixture_source(tmp_path)
    linked = root / 'src/linked';linked.mkdir()
    (linked / 'not_for_package.py').write_text('value = 1')
    original = Path.is_junction
    monkeypatch.setattr(Path, 'is_junction', lambda p: p == linked or original(p))
    result = script.package(root, tmp_path / 'out', '0.1.0-test')
    with zipfile.ZipFile(result['archive']) as zipped:
        assert not any('/linked/' in name for name in zipped.namelist())


def test_packager_rejects_missing_entrypoint(tmp_path):
    script = load('package_handover')
    root = tmp_path / 'empty';root.mkdir()
    with pytest.raises(ValueError, match='entry point'):script.package(root, tmp_path / 'out', '0.1.0')
