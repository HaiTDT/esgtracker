"""Generate source/schema/dependency references without running app/OCR/API."""
import argparse
import ast
import csv
from hashlib import sha256
from importlib import metadata
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
FOLDERS = ('src', 'dashboard', 'scripts', 'tests', 'config', 'contracts')


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding='utf-8')


def run(destination):
    destination = Path(destination)
    index = []
    for folder in FOLDERS:
        for path in sorted((ROOT / folder).rglob('*')):
            if not path.is_file() or '__pycache__' in path.parts or path.suffix not in ('.py', '.yml', '.yaml', '.json', '.cjs', '.js', '.css'):
                continue
            text = path.read_text(encoding='utf-8-sig')
            item = {'path': path.relative_to(ROOT).as_posix(), 'sha256': sha256(path.read_bytes()).hexdigest(),
                    'symbols': [], 'imports': [], 'description': None}
            if path.suffix == '.py':
                tree = ast.parse(text)
                item['description'] = ast.get_docstring(tree)
                item['symbols'] = [{'name': n.name, 'line': n.lineno, 'kind': type(n).__name__}
                    for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
                item['imports'] = sorted({n.module or '' for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)} |
                    {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names})
                item['function_contracts'] = [{'name': n.name, 'line': n.lineno, 'arguments': ast.unparse(n.args),
                    'return_annotation': ast.unparse(n.returns) if n.returns else None, 'docstring': ast.get_docstring(n)}
                    for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
            index.append(item)
    app = ROOT / 'app.py'
    tree = ast.parse(app.read_text(encoding='utf-8-sig'))
    index.append({'path': 'app.py', 'sha256': sha256(app.read_bytes()).hexdigest(),
        'description': 'Production entry point; import has DB initialization side effects.',
        'symbols': [{'name': n.name, 'line': n.lineno, 'kind': type(n).__name__} for n in ast.walk(tree)
                    if isinstance(n, (ast.FunctionDef, ast.ClassDef))],
        'function_contracts': [{'name': n.name, 'line': n.lineno, 'arguments': ast.unparse(n.args),
            'return_annotation': ast.unparse(n.returns) if n.returns else None, 'docstring': ast.get_docstring(n)}
            for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))],
        'imports': sorted({n.module or '' for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)} |
            {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names})})
    write(destination / 'module-index.json', json.dumps({'scope': list(FOLDERS) + ['app.py'], 'files': index}, ensure_ascii=False, indent=2))
    profiles = ['# Hồ sơ module/symbol sinh từ source', '',
        'ĐÃ XÁC MINH: tên, chữ ký, annotation, docstring và dependency đọc từ source.',
        'Annotation/docstring không phải kiểm chứng hành vi live. Không suy kiểu trả về khi không khai báo.',
        'Luồng nghiệp vụ, cấu hình/timeout/retry, cài đặt và giới hạn xem các chương 04/06/07/17.', '']
    for item in index:
        profiles += ['## ' + item['path'], '', (item['description'] or 'Không có module docstring; xem source và inventory kiến trúc.'), '',
            '**Dependency/import:** ' + ', '.join('`' + i + '`' for i in item.get('imports', []) if i) + '.', '']
        for fn in item.get('function_contracts', []):
            profiles += ['### ' + fn['name'] + ' — dòng ' + str(fn['line']), '',
                '- Đầu vào (signature): `' + fn['arguments'].replace('`', '') + '`.',
                '- Đầu ra annotation: `' + (fn['return_annotation'] or 'chưa khai báo') + '`.',
                '- Contract ghi trong source: ' + (fn['docstring'] or 'Chưa có docstring; không tự suy từ tên hàm.'), '']
    write(destination / 'module-profiles.md', '\n'.join(profiles))
    with (destination / 'component-inventory.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(['Thành phần', 'Vai trò (module docstring nếu có)', 'File', 'Đầu vào', 'Đầu ra', 'Dependency/import', 'Xác minh'])
        for item in index:
            writer.writerow([Path(item['path']).stem, item['description'] or 'Xem hồ sơ module/pipeline; không suy từ tên', item['path'],
                             'Xem docs/07-extraction-pipelines.md', 'Xem docs/08-json-contract-and-data-dictionary.md',
                             '; '.join(item.get('imports', [])), 'ĐÃ XÁC MINH: source/hash/symbol; không có nghĩa đã chạy live'])
    lines = ['# Property inventory từ JSON Schema', '', 'Sinh bởi `scripts/handover_reference.py`; không thay schema runtime.',
        'Required theo đúng object cha; `conditional` nghĩa là allOf/if/then, không phải mọi record.',
        'Không có type/description trong schema được ghi chưa khai báo, không tự suy diễn.', '']
    def walk(node, root, pointer='', required=False, condition='trực tiếp', refs=()):
        if not isinstance(node, dict):return
        if '$ref' in node:
            ref = node['$ref']
            if ref in refs:return
            target = root
            if ref.startswith('#/'):
                for part in ref[2:].split('/'):target = target[part.replace('~1','/').replace('~0','~')]
                yield from walk(target, root, pointer, required, condition + '; ' + ref, refs + (ref,))
            return
        if pointer:
            typ = json.dumps(node.get('type', 'chưa khai báo'), ensure_ascii=False)
            rules = {k: node[k] for k in ('enum', 'const', 'pattern', 'minimum', 'maximum', 'minItems', 'maxItems') if k in node}
            desc = node.get('description', 'Chưa có description trong schema; xem dictionary nghiệp vụ.')
            yield [pointer, desc, typ, 'có' if required else 'không', condition, json.dumps(rules, ensure_ascii=False)]
        for name, child in node.get('properties', {}).items():
            yield from walk(child, root, pointer + '/' + name, name in node.get('required', []), condition, refs)
        if isinstance(node.get('items'), dict):yield from walk(node['items'], root, pointer + '/*', False, condition, refs)
        for key in ('allOf', 'anyOf', 'oneOf'):
            for child in node.get(key, []):yield from walk(child, root, pointer, required, 'conditional ' + key, refs)
        for key in ('then', 'else'):
            if key in node:yield from walk(node[key], root, pointer, required, 'conditional ' + key, refs)
    for path in sorted((ROOT / 'contracts').rglob('*schema.json')) + [ROOT / 'schemas/upload-export.inferred.schema.json']:
        schema = json.loads(path.read_text(encoding='utf-8'))
        lines += ['## ' + path.relative_to(ROOT).as_posix(), '', '| Đường dẫn | Ý nghĩa từ schema | Kiểu | Bắt buộc | Điều kiện / nguồn | Quy tắc |', '| --- | --- | --- | --- | --- | --- |']
        for row in walk(schema, schema):
            lines.append('| ' + ' | '.join(str(x).replace('|', '\\|').replace('\n', ' ') for x in row) + ' |')
        lines.append('')
    write(destination / 'schema-fields.md', '\n'.join(lines))
    dependencies = []
    for requirement in (ROOT / 'requirements.txt').read_text().splitlines() + ['python-docx', 'Pillow', 'torch', 'docling-core', 'pypdfium2']:
        name = re.split(r'[<>=!~\[]', requirement)[0].strip()
        if not name or name.startswith('#'):continue
        try:
            info = metadata.metadata(name)
            dependencies.append({'name': name, 'version': metadata.version(name),
                'license_metadata': info.get('License-Expression') or (info.get('License') or '')[:500] or 'UNKNOWN',
                'project_urls': info.get_all('Project-URL') or [],
                'scope': 'installed metadata only; not legal clearance or complete transitive SBOM'})
        except metadata.PackageNotFoundError:dependencies.append({'name': name, 'status': 'NOT_INSTALLED'})
    write(destination / 'dependencies.json', json.dumps(dependencies, ensure_ascii=False, indent=2))
    write(destination / 'dependency-constraints.txt', '# Observed Windows / Python 3.12 environment, NOT portable lockfile.\n# Only constrains packages selected by requirements; no wheel hashes or offline guarantee.\n' +
          '\n'.join(f"{d['name']}=={d['version']}" for d in dependencies if 'version' in d) + '\n')
    return {'indexed_files': len(index), 'dependencies': len(dependencies), 'destination': str(destination)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', type=Path, default=ROOT / 'docs/reference')
    print(json.dumps(run(parser.parse_args().destination), ensure_ascii=False))
