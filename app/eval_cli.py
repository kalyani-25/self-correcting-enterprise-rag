from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path
from app.pipeline import run_pipeline
from app.evaluator import llm_evaluate


def main():
    parser = argparse.ArgumentParser(description='Batch evaluate QA pairs')
    parser.add_argument('--pdf', required=True)
    parser.add_argument('--questions', required=True, help='JSONL with question and ground_truth')
    parser.add_argument('--output', default='outputs/eval_results.csv')
    args = parser.parse_args()

    rows = []
    for line in Path(args.questions).read_text().splitlines():
        if not line.strip():
            continue
        item = json.loads(line)
        result = run_pipeline(args.pdf, item['question'])
        eval_result = llm_evaluate(item['question'], result['answer'], item['ground_truth'])
        rows.append({
            'question': item['question'],
            'ground_truth': item['ground_truth'],
            'answer': result['answer'],
            'grade': result['grade'],
            'score': eval_result['score'],
            'eval_reason': eval_result['reason'],
            'retries': result['retries'],
            'latency_ms': result['metrics']['total_latency_ms'],
        })

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f'Saved {args.output}')


if __name__ == '__main__':
    main()
