"""OFFLINE controlled fixture smoke: real parsers, FAKE PDF page reader, no OCR/API."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import pymupdf
from dashboard.upload_v2 import export_result
from src.extraction.source_v2 import capture_pdf, atomic_json
from src.extraction.financial_v2 import extract_financial
from src.extraction.esg_v2 import extract_esg
from src.extraction.corporate_handoff import convert_document
from jsonschema import Draft202012Validator


def run(destination):
    destination = Path(destination).resolve()
    destination.mkdir(parents=True, exist_ok=False)
    documents, results = [], []
    for index, kind in enumerate(('financial_statements', 'ESG', 'annual_report')):
        source = destination / ('SYNTHETIC_' + kind + '_2025.pdf')
        # Internal test fixture, not a PDF report/artifact for end-user delivery.
        with pymupdf.open() as pdf:
            pdf.new_page().insert_text((40, 60), 'SYNTHETIC TEST FIXTURE ONLY - NOT A COMPANY REPORT')
            pdf.save(source)
        financial = kind == 'financial_statements'
        rows = [['Chỉ tiêu', 'Mã số', '2025', '2024'], ['Doanh thu thuần', '10', '100', '90']] if financial else [
            ['Chỉ tiêu', 'Đơn vị', '2025'], ['Tổng số lao động', 'người', '100']]
        cells = [{'text': value, 'column_header': row == 0, 'start_row_offset_idx': row, 'end_row_offset_idx': row + 1,
                  'start_col_offset_idx': col, 'end_col_offset_idx': col + 1} for row, values in enumerate(rows) for col, value in enumerate(values)]
        native = {'texts': [{'text': 'BÁO CÁO TÀI CHÍNH RIÊNG' if financial else 'Chính sách giảm phát thải và sử dụng năng lượng hiệu quả.', 'label': 'text'},
                            {'text': 'Đơn vị tính: VND' if financial else 'Phạm vi chỉ tiêu chưa xác minh.', 'label': 'text'}],
                  'tables': [{'data': {'num_rows': len(rows), 'num_cols': len(rows[0]), 'table_cells': cells}}],
                  'body': {'children': [{'$ref': '#/texts/0'}, {'$ref': '#/texts/1'}, {'$ref': '#/tables/0'}]}}
        def reader(*_, data=native):return {'status': 'processed', 'document': deepcopy(data), 'markdown': 'CONTROLLED FAKE PAGE READER - NOT OCR'}
        work = capture_pdf(source, destination / 'work', company_id='SYNTH', report_type=kind, report_year=2025,
                           page_reader=reader, profile={'engine': 'handover-synthetic-page-reader', 'version': 1})
        output_path = extract_financial(work) if financial else extract_esg(work)
        output = json.loads(output_path.read_text(encoding='utf-8'))
        if not output['validation']['valid'] or not output['records']:raise ValueError('Synthetic parser smoke failed: ' + kind)
        bundle = json.loads((work / 'canonical.json').read_text(encoding='utf-8'))
        documents.append({'document_index': index, 'filename': source.name, 'workspace': str(work), 'output_path': str(output_path),
                          'output': output, 'capture_status': 'completed', 'coverage': bundle['coverage']})
        atomic_json(destination / ('example_' + kind + '.json'), output)
        results.append({'report_type': kind, 'schema': output['schema_version'], 'records': len(output['records']), 'schema_valid': True})
    result = {'documents': documents, 'pipeline': 'source-typed-v2', 'manifest': {'document_count': 3, 'failures': []}}
    portable = export_result(result)
    Draft202012Validator(json.loads((ROOT / 'schemas/upload-export.inferred.schema.json').read_text())).validate(portable)
    atomic_json(destination / 'example_upload.json', portable)
    corporate = convert_document(documents[0])
    Draft202012Validator(json.loads((ROOT / 'contracts/corporate_extract_v1/schema.json').read_text(encoding='utf-8'))).validate(corporate)
    atomic_json(destination / 'example_corporate_financial.json', corporate)
    report = {'status': 'PASS', 'synthetic': True, 'page_reader': 'FAKE', 'real_ocr_verified': False,
              'external_api_requests': 0, 'reports': results, 'accuracy_measured': False}
    atomic_json(destination / 'smoke_report.json', report)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', type=Path, required=True, help='NEW directory; no overwrite')
    print(json.dumps(run(parser.parse_args().destination), ensure_ascii=False, indent=2))
