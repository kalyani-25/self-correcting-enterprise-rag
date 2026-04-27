PLANNER_PROMPT = """
You are a production document-retrieval planner.

Question:
{question}

Available document tree summaries:
{tree}

Pick the most relevant node IDs to inspect. Return strict JSON only:
{{
  "thinking": "brief reason",
  "node_list": ["node_001", "node_002"]
}}
"""

ANSWER_PROMPT = """
Answer the question using only the provided context.

Question:
{question}

Context:
{context}

Rules:
- Do not invent facts.
- If context is insufficient, say what is missing.
- Be concise but complete.
"""

GRADER_PROMPT = """
You are an LLM-as-Judge for retrieval QA.

Question:
{question}

Context:
{context}

Answer:
{answer}

Decide whether the answer is supported and complete. Return strict JSON only:
{{
  "grade": "yes" or "no",
  "reason": "brief reason",
  "improved_query": "better search query if grade is no, otherwise original question"
}}
"""

EVAL_PROMPT = """
Score the answer against the ground truth from 1 to 5.

Question: {question}
Ground truth: {ground_truth}
Answer: {answer}

Return strict JSON only:
{{"score": 1, "reason": "brief reason"}}
"""
