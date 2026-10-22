"""Build a blind Oil & Gas annotation pack; check independent gold release gates."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.quality_benchmark import predictions, known_development_sources, write_new, read
from src.quality.oil_gold import load_codebook, build_pack, release_check, verify_source_delivery


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--codebook', type=Path, default=ROOT/'config/oil_gas_gold.yml')
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('build')
    p.add_argument('input', type=Path)
    p.add_argument('--destination', type=Path, required=True)
    p.add_argument('--pages', type=int, default=24)
    p.add_argument('--split', choices=['train', 'dev', 'test'], default='dev')
    p = sub.add_parser('release-check')
    p.add_argument('--final', type=Path, required=True)
    p.add_argument('--reviewer-a', type=Path, required=True)
    p.add_argument('--reviewer-b', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--source-delivery', type=Path, required=True, help='Manifest delivery containing unchanged original PDFs')
    args = parser.parse_args()
    try:
        book = load_codebook(args.codebook)
        if args.command == 'build':
            if args.destination.exists():
                raise ValueError('Choose a NEW destination; existing annotations must not be overwritten.')
            data, _ = predictions(args.input)
            draft, tasks, plan = build_pack(data, book, pages=args.pages, split=args.split,
                                           development_sources=known_development_sources())
            draft['codebook_sha256'] = sha256(args.codebook.read_bytes()).hexdigest()
            inventory = verify_source_delivery(args.input, [draft]) if args.input.is_dir() else {
                'status': 'unverified_paths', 'reason': 'Prediction JSON only. Verify original PDFs using --source-delivery at release-check.'}
            args.destination.mkdir(parents=True)
            for name in ('reviewer_a_draft.json', 'reviewer_b_draft.json', 'adjudication_draft.json'):
                write_new(args.destination/name, draft)
            write_new(args.destination/'assisted_candidates_NOT_GOLD.json', tasks)
            write_new(args.destination/'coverage_plan.json', plan)
            write_new(args.destination/'codebook.json', book)
            write_new(args.destination/'predictions.json', data)
            write_new(args.destination/'source_inventory.json', inventory)
            print(f"DRAFT_NOT_GOLD sources={plan['selected_sources']} pages={plan['selected_pages']} candidates={plan['candidate_items']}")
        else:
            final, a, b = (read(p) for p in (args.final, args.reviewer_a, args.reviewer_b))
            digest = lambda p: sha256(p.read_bytes()).hexdigest()
            if any(g.get('codebook_sha256') != digest(args.codebook) for g in (final, a, b)):
                raise ValueError('Codebook version/hash mismatch; re-review annotations after codebook changes.')
            report = release_check(final, a, b, book, a_sha256=digest(args.reviewer_a),
                                   b_sha256=digest(args.reviewer_b), development_sources=known_development_sources())
            inventory = verify_source_delivery(args.source_delivery, [final, a, b])
            report.update(final_sha256=digest(args.final), codebook_sha256=digest(args.codebook),
                          reviewer_a_sha256=digest(args.reviewer_a), reviewer_b_sha256=digest(args.reviewer_b),
                          verified_source_count=len(inventory))
            write_new(args.output, report)
            print(json.dumps(report, ensure_ascii=False))
        return 0
    except (ValueError, KeyError, OSError, TypeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
