"""Opt-in source-v2 -> local Ollama candidates; never downloads models."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.extraction.local_llm import OllamaClient, extract_local_llm, load_settings, read_json


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('workspace', type=Path, nargs='?', help='Source-v2 folder containing canonical.json')
    parser.add_argument('--config', type=Path, default=ROOT / 'config/local_llm.yml')
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'data/processed/local_llm')
    parser.add_argument('--model', help='Exact installed model tag. No automatic pull.')
    parser.add_argument('--base-url', help='Loopback Ollama origin only')
    parser.add_argument('--number-format', choices=['auto', 'vi', 'en'])
    parser.add_argument('--start-page', type=int, default=1)
    parser.add_argument('--max-pages', type=int)
    parser.add_argument('--max-chunks', type=int, help='Smoke-test cap, not full report extraction')
    parser.add_argument('--check', action='store_true', help='Local runtime/model identity only; no generation')
    args = parser.parse_args(argv)
    try:
        settings = load_settings(args.config, model=args.model, base_url=args.base_url, number_format=args.number_format)
        if args.check:
            print(json.dumps({'provider': 'ollama_local', 'model': OllamaClient(settings).preflight(),
                              'mode': 'text_only', 'downloads_performed': False}, ensure_ascii=False, indent=2))
            return 0
        if args.workspace is None:
            parser.error('workspace required unless --check')
        output = extract_local_llm(args.workspace, args.output_dir, settings, start_page=args.start_page,
            max_pages=args.max_pages, max_chunks=args.max_chunks,
            progress_callback=lambda event: print(json.dumps(event, ensure_ascii=False), flush=True))
        data = read_json(output)
        print(json.dumps({'output': str(output), 'records': len(data['records']), 'issues': len(data['issues']),
                          'chunk_counts': data['coverage']['counts'],
                          'text_pass_complete': data['coverage']['text_pass_complete'],
                          'semantic_status': 'partial', 'graph_ready': False}, ensure_ascii=False, indent=2))
        # Never exit zero as a declaration of factual accuracy/full extraction.
        return 1 if data['coverage']['counts'].get('failed') else 2
    except (ValueError, OSError, RuntimeError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
