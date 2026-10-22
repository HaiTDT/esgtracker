"""Check new documentation links, source locators and published synthetic schemas."""
import argparse
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from jsonschema import Draft202012Validator


def check(root=ROOT):
    root = Path(root).resolve()
    pages = sorted((root / 'docs').glob('[0-9][0-9]-*.md')) + [root / 'docs/evidence-register.md', root / 'README.md',
            root / 'schemas/README.md', root / 'examples/README.md', root / 'DISTRIBUTION_STATUS.md']
    errors, links = [], 0
    for page in pages:
        if not page.is_file():errors.append('Missing: ' + str(page.relative_to(root)));continue
        text = page.read_text(encoding='utf-8')
        for target in re.findall(r'\]\(([^)]+)\)', text):
            if target.startswith(('http:', 'https:', 'mailto:', '#')):continue
            target = unquote(target.split('#', 1)[0].strip('<>'))
            if not target:continue
            links += 1
            if not (page.parent / target).resolve().exists():errors.append(f'{page.relative_to(root)} -> {target}')
    evidence = json.loads((root / 'docs/reference/evidence.json').read_text(encoding='utf-8'))
    for row in evidence:
        path = root / row['file']
        if not path.is_file():errors.append('Missing evidence file: ' + row['file'])
        elif row.get('symbol') and row['symbol'] not in path.read_text(encoding='utf-8-sig'):
            errors.append('Missing evidence symbol: ' + row['file'] + ':' + row['symbol'])
    for example in (root / 'examples').glob('*.json'):
        data = json.loads(example.read_text(encoding='utf-8'))
        name = data.get('schema_version')
        schema_path = {'esg-financial-candidates/2.3.0': 'contracts/financial_v2.schema.json',
                       'esg-candidates/2.1.0': 'contracts/esg_v2.schema.json',
                       'corporate-extract-1.0': 'contracts/corporate_extract_v1/schema.json',
                       'esg-upload/2.0.0': 'schemas/upload-export.inferred.schema.json'}.get(name)
        if not schema_path:errors.append('Unknown example schema: ' + example.name);continue
        validator = Draft202012Validator(json.loads((root / schema_path).read_text(encoding='utf-8')))
        errors.extend(example.name + ': ' + e.message for e in validator.iter_errors(data))
    return {'passed': not errors, 'new_documentation_files': len(pages), 'local_links_checked': links,
            'evidence_rows_checked': len(evidence), 'errors': errors,
            'limits': 'Does not fetch external URLs, run commands in prose, certify legal rights or validate live models.'}


if __name__ == '__main__':
    result = check()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result['passed'] else 1)
