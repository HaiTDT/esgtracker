"""Source-only internal review archive; no deployment, upload, secrets or datasets."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DIRECTORIES = ('src', 'dashboard', 'scripts', 'tests', 'config', 'contracts', 'docs', 'schemas', 'examples')
ROOT_FILES = ('app.py', 'README.md', '.gitignore', '.env.example', 'requirements.txt', 'pytest.ini', 'DISTRIBUTION_STATUS.md')
EXTENSIONS = {'.py', '.js', '.cjs', '.css', '.svg', '.json', '.yml', '.yaml', '.md', '.txt', '.csv', '.sql', '.ps1'}
DENY_PARTS = {'.git', '.venv', 'node_modules', '__pycache__', '.pytest_cache', '.superdesign', 'data', 'outputs', 'output', 'tmp', 'rendered', 'rendered_pdf'}
SECRET_PATTERNS = [re.compile(r'AIza[0-9A-Za-z_-]{30,}'), re.compile(r'AQ\.[0-9A-Za-z_-]{30,}'),
                   re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')]


def digest(raw):return sha256(raw).hexdigest()


def source_files(root):
    root = Path(root).resolve()
    candidates = [root / name for name in ROOT_FILES]
    for folder in DIRECTORIES:
        # No recursion across junctions, and no accidental cached dataset trees.
        pending = [root / folder]
        while pending:
            here = pending.pop()
            if not here.is_dir() or here.is_symlink() or here.is_junction():continue
            for path in sorted(here.iterdir()):
                if path.is_symlink() or path.is_junction() or path.name in DENY_PARTS:continue
                if path.is_dir():pending.append(path)
                else:candidates.append(path)
    candidates.append(root / 'database/schema.sql')
    result = []
    for path in candidates:
        if not path.is_file() or path.is_symlink() or path.is_junction():continue
        rel = path.relative_to(root)
        if path.suffix.lower() not in EXTENSIONS and path.name not in ROOT_FILES:continue
        if any(p in DENY_PARTS for p in rel.parts):continue
        if path.name.startswith('.env') and path.name != '.env.example':continue
        if re.search(r'credentials|service.account|secret.*\.json', path.name, re.I):continue
        if path.stat().st_size > 5 * 1024 * 1024:raise ValueError('Oversized source; review manually: ' + rel.as_posix())
        result.append((rel.as_posix(), path))
    return sorted(set(result))


def scan(raw, relative):
    text = raw.decode('utf-8-sig')
    if any(pattern.search(text) for pattern in SECRET_PATTERNS):
        raise ValueError('Possible secret; file withheld (value never printed): ' + relative)
    if relative == '.env.example':
        for line in text.splitlines():
            if line.strip() and not line.lstrip().startswith('#') and '=' in line and line.split('=', 1)[1].strip():
                raise ValueError('.env.example must contain only empty assignments.')


def package(root, destination, version, *, dry_run=False):
    root, destination = Path(root).resolve(), Path(destination).resolve()
    if not re.fullmatch(r'\d+\.\d+\.\d+(?:-[a-z0-9.]+)?', version):raise ValueError('Version must be semver-like, no path/URL.')
    if destination == root or destination.is_relative_to(root) or root.is_relative_to(destination):
        raise ValueError('Use a NEW dedicated destination outside the application and its ancestors.')
    git_root = next((folder for folder in (root, *root.parents) if (folder / '.git').exists()), None)
    if git_root and destination.is_relative_to(git_root):raise ValueError('Keep handover archives outside the Git repository.')
    if destination.exists():raise ValueError('Destination exists; no overwrite.')
    if not (root / 'app.py').is_file() or not (root / 'README.md').is_file():
        raise ValueError('Application entry point and README are required; no incomplete archive.')
    files = source_files(root)
    rows, contents = [], {}
    for relative, path in files:
        raw = path.read_bytes()
        scan(raw, relative)
        rows.append({'path': relative, 'sha256': digest(raw), 'bytes': len(raw)})
        contents[relative] = raw
    manifest = {'version': version, 'kind': 'INTERNAL_REVIEW_NOT_PUBLIC_RELEASE',
        'business_logic_changed_by_packager': False, 'files': rows,
        'excluded': ['.git', '.venv', 'data', 'database/*.db', 'models', 'node_modules', 'outputs', 'tmp',
                     'PDF/DOCX/XLSX/report archives', 'secret files', 'cache', 'logs', 'external root Phase1 datasets'],
        'release_blockers': ['Project license/owner distribution approval unresolved',
            'Third-party licensing, especially PyMuPDF AGPL/commercial, requires owner review',
            'Clean offline OCR/model installation and live Gemini not verified'],
        'scan': {'known_secret_patterns_found': 0, 'scope': 'Selected UTF-8 source files; heuristic, not a secret-free guarantee'},
        'reference_seed_note': 'Source config/tests may contain public-company reference excerpts; no original report files. Owner must clear rights before redistribution.'}
    if dry_run:return manifest
    destination.mkdir(parents=True, exist_ok=False)
    archive = destination / f'esg-tracker-{version}-review.zip'
    prefix = f'esg-tracker-{version}'
    with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED) as zipped:
        for relative, raw in contents.items():
            # Stable metadata/order for reproducibility on identical file bytes.
            info = zipfile.ZipInfo(prefix + '/' + relative, (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            zipped.writestr(info, raw)
        zipped.writestr(prefix + '/PACKAGE_MANIFEST.json', json.dumps(manifest, ensure_ascii=False, indent=2))
    with zipfile.ZipFile(archive) as zipped:
        for row in rows:
            raw = zipped.read(prefix + '/' + row['path'])
            if digest(raw) != row['sha256']:raise ValueError('Archive verification failed.')
            scan(raw, row['path'])
    (destination / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    (destination / 'SHA256SUMS.txt').write_text(f'{digest(archive.read_bytes())}  {archive.name}\n', encoding='ascii')
    return {'archive': str(archive), 'files': len(rows), 'sha256': digest(archive.read_bytes()),
            'verified_archive_entries': True, 'status': manifest['kind'], 'release_blockers': manifest['release_blockers']}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', type=Path, required=True)
    parser.add_argument('--version', required=True)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args(argv)
    try:result = package(ROOT, args.destination, args.version, dry_run=args.dry_run)
    except (ValueError, OSError, UnicodeError) as exc:
        print(str(exc), file=sys.stderr);return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':raise SystemExit(main())
