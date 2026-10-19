"""Private persistent page reader; never writes a source capture checkpoint."""
import json
from pathlib import Path
import sys
import time
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import pymupdf
from src.extraction.source_v2 import atomic_json, _docling_page, _ocr_docling_page
from src.extraction.docling_backend import create_converter


def main():
    settings_path = Path(sys.argv[1])
    folder = settings_path.parent
    settings = json.loads(settings_path.read_text(encoding='utf-8'))
    native_auto = settings.get('mode', 'native_auto') == 'native_auto'
    options = {'backend': 'native_text'} if native_auto else dict(settings['ocr'])
    options['document_timeout_seconds'] = settings['page_timeout']
    converter = create_converter(options)
    atomic_json(folder / 'ready.json', {'ready': True})
    seq = None
    while True:
        try:
            request = json.loads((folder / 'request.json').read_text(encoding='utf-8'))
        except (OSError, ValueError):
            time.sleep(.1)
            continue
        if request['seq'] == seq:
            time.sleep(.1)
            continue
        seq = request['seq']
        try:
            path, number = request['pdf'], request['page']
            text = ''
            if native_auto:
                with pymupdf.open(path) as pdf:
                    text = pdf[number - 1].get_text()
            if native_auto and len(text.strip()) >= 40 and text.count('\ufffd') <= max(1, len(text) // 100):
                # Process a one-page native proxy, not the whole multi-page
                # resource tree. Original PDF bytes are never modified. This
                # also avoids mixed page-size provenance clamping in Docling.
                with tempfile.TemporaryDirectory(prefix='esg_native_page_') as temporary:
                    proxy = Path(temporary) / 'page.pdf'
                    with pymupdf.open(path) as source, pymupdf.open() as single:
                        single.insert_pdf(source, from_page=number-1, to_page=number-1)
                        single.save(proxy, garbage=4, deflate=True)
                    result = _docling_page(proxy, 1, converter)
                result['read_method'] = 'isolated_docling_single_native_page'
                result['original_pdf_page'] = number
            elif settings['ocr']['backend'] == 'tesseract_pdf':
                result = _ocr_docling_page(path, number, converter, settings['ocr'])
                result['read_method'] = 'isolated_tesseract_pdf_then_docling'
            elif native_auto:
                raise ValueError('Native text insufficient; configured Tesseract OCR unavailable.')
            else:
                result = _docling_page(path, number, converter)
                result['read_method'] = 'isolated_configured_docling_ocr'
            atomic_json(folder / 'reply.json', {'seq': seq, 'result': result})
        except Exception as exc:
            atomic_json(folder / 'reply.json', {'seq': seq, 'error': f'{type(exc).__name__}: {exc}'})


if __name__ == '__main__':
    main()
