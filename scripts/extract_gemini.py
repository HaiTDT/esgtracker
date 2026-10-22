"""Explicit-consent Gemini PDF extraction. Configuration checks never call API."""
import argparse
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.extraction.gemini import settings, api_key, Budget, extract_pdf, read_json


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', nargs='?', type=Path)
    parser.add_argument('--company')
    parser.add_argument('--year', type=int)
    parser.add_argument('--type', choices=['financial_statements', 'ESG', 'sustainability_report', 'annual_report'])
    parser.add_argument('--model')
    parser.add_argument('--max-requests', type=int, default=10)
    parser.add_argument('--number-format', choices=['auto', 'vi', 'en'], default='auto')
    parser.add_argument('--output', type=Path, default=ROOT / 'data/processed/gemini_v1/cli')
    parser.add_argument('--allow-cloud', action='store_true', help='Consent to Google PDF upload and possible API charges')
    parser.add_argument('--check-config', action='store_true', help='No network or PDF upload')
    args = parser.parse_args(argv)
    try:
        config = settings(model=args.model)
        budget = Budget(args.max_requests)
        if args.check_config:
            try:
                api_key()
                configured = True
            except ValueError:
                configured = False
            print(json.dumps({'model': config['model'], 'api_key_configured': configured,
                              'max_requests': budget.limit, 'network_requests': 0}))
            return 0 if configured else 1
        if not args.allow_cloud:
            raise ValueError('Required: --allow-cloud. No PDF has been sent.')
        if not args.pdf or not args.pdf.is_file() or not args.company or not args.type or args.year is None or not 1900 <= args.year <= 2100:
            raise ValueError('Required: existing PDF, --company, --year 1900–2100 and --type.')
        output = extract_pdf(args.pdf, args.output, config, company_id=args.company,
            report_type='ESG' if args.type == 'sustainability_report' else args.type,
            report_year=args.year, consent=True, budget=budget, number_format=args.number_format)
        data = read_json(output)
        print(json.dumps({'output': str(output), 'records': len(data['records']), 'coverage': data['coverage']['counts'],
                          'api_requests_used': budget.used, 'pending_human_review': True}, ensure_ascii=False))
        return 0
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
