"""Render selected source pages for AI inspection; no gold/approval is created."""
import json
from pathlib import Path
import subprocess
import sys
import hashlib

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.extraction.source_v2 import atomic_json


def main():
    import pymupdf
    pack = ROOT/'outputs/oil_gold_bsr_v1_20261021_r2'
    delivery = ROOT/'outputs/ESG_extract_V2'
    dest = ROOT/'tmp/ai_reference_pages_20261021'
    dest.mkdir(parents=True, exist_ok=True)
    gold = json.loads((pack/'reviewer_a_draft.json').read_text(encoding='utf-8'))
    inventory = json.loads((pack/'source_inventory.json').read_text(encoding='utf-8'))
    requested = {(u['source_sha256'], u['physical_page']) for u in gold['evaluation_units']}
    # Supplemental headcount source and report-boundary context. Not substituted
    # for any originally selected page.
    for source, info in inventory.items():
        if info['pdf_path'] == 'pdf/BSR_2025.pdf': requested.add((source, 39))
        if info['pdf_path'] == 'pdf/BSR_2023.pdf':
            requested.update((source, p) for p in (26, 32))
        if info['pdf_path'] == 'pdf/BSR_2024.pdf':
            requested.update((source, p) for p in (26, 33))
    pages = []
    for source, page in sorted(requested):
        path = delivery/inventory[source]['pdf_path']
        if hashlib.sha256(path.read_bytes()).hexdigest() != source:
            raise ValueError('PDF hash mismatch')
        prefix = dest/f'{source[:10]}_p{page:03}'
        existing = list(dest.glob(prefix.name+'-*.png'))
        if not existing:
            subprocess.run(['pdftoppm', '-f', str(page), '-l', str(page), '-scale-to', '1900',
                            '-png', str(path), str(prefix)], check=True, capture_output=True)
        with pymupdf.open(path) as pdf:
            text = pdf[page-1].get_text()
            size = list(pdf[page-1].rect)
        unit = next((u for u in gold['evaluation_units'] if u['source_sha256']==source and u['physical_page']==page), None)
        pages.append({'source_sha256': source, 'pdf_path': str(path), 'physical_page': page,
                      'image_path': str(next(dest.glob(prefix.name+'-*.png'))),
                      'pdf_rect': size, 'embedded_text': text,
                      'selected_candidate_items': unit['items'] if unit else [],
                      'role': 'selected' if unit else 'supplemental'})
    atomic_json(dest/'pages.json', pages)
    print(f'Rendered {len(pages)} source pages; no gold labels created.')


if __name__ == '__main__':
    main()
