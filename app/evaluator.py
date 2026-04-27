from __future__ import annotations
from app.llm import LLMClient
from app.prompts import EVAL_PROMPT
from app.utils import safe_json_loads


def llm_evaluate(question: str, answer: str, ground_truth: str) -> dict:
    llm = LLMClient()
    prompt = EVAL_PROMPT.format(question=question, answer=answer, ground_truth=ground_truth)
    parsed = safe_json_loads(llm.invoke(prompt), fallback={'score': 0, 'reason': 'Invalid evaluator response'})
    return {'score': int(parsed.get('score', 0)), 'reason': parsed.get('reason', '')}
