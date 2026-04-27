from __future__ import annotations
import argparse
import json
from pathlib import Path
from app.logging_config import configure_logging
from app.pipeline import run_pipeline


def main():
    configure_logging()
    parser = argparse.ArgumentParser(description='Run self-correcting enterprise RAG from CLI')
    parser.add_argument('--pdf', required=True)
    parser.add_argument('--question', required=True)
    parser.add_argument('--max-retries', type=int, default=None)
    parser.add_argument('--output', default='outputs/final_result.json')
    args = parser.parse_args()

    result = run_pipeline(args.pdf, args.question, args.max_retries)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(result, indent=2))
    print('\nANSWER\n------')
    print(result['answer'])
    print('\nMETRICS\n-------')
    print(json.dumps(result['metrics'], indent=2))


if __name__ == '__main__':
    main()
