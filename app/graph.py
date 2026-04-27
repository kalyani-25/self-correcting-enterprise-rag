from __future__ import annotations
from typing import Any, TypedDict
import json
from langgraph.graph import StateGraph, END
from app.config import get_settings
from app.llm import LLMClient
from app.metrics import timer
from app.prompts import PLANNER_PROMPT, ANSWER_PROMPT, GRADER_PROMPT
from app.utils import safe_json_loads, strip_text_for_planning


class RagState(TypedDict):
    request_id: str
    question: str
    search_query: str
    tree: list[dict[str, Any]]
    node_map: dict[str, dict[str, Any]]
    selected_nodes: list[str]
    context: str
    answer: str
    grade: str
    grader_reason: str
    retries: int
    max_retries: int
    metrics: dict[str, Any]


def build_graph():
    llm = LLMClient()
    settings = get_settings()

    def planner(state: RagState) -> RagState:
        with timer(state['metrics'], 'planner'):
            planning_tree = strip_text_for_planning(state['tree'])
            prompt = PLANNER_PROMPT.format(
                question=state['search_query'],
                tree=json.dumps(planning_tree, indent=2),
            )
            parsed = safe_json_loads(llm.invoke(prompt), fallback={'node_list': []})
            nodes = [str(x) for x in parsed.get('node_list', [])]
            state['selected_nodes'] = nodes[:5] or ['node_002']
        return state

    def retriever(state: RagState) -> RagState:
        with timer(state['metrics'], 'retriever'):
            chunks: list[str] = []
            for node_id in state['selected_nodes']:
                node = state['node_map'].get(node_id)
                if not node:
                    continue
                chunks.append(
                    f"Node: {node_id}\nTitle: {node.get('title','')}\nPage: {node.get('page', 'unknown')}\nSummary: {node.get('summary','')}\nText: {node.get('text','')}"
                )
                for child in node.get('children', []) or []:
                    chunks.append(
                        f"Child Node: {child.get('id')}\nTitle: {child.get('title','')}\nPage: {child.get('page','unknown')}\nSummary: {child.get('summary','')}\nText: {child.get('text','')}"
                    )
            state['context'] = '\n\n---\n\n'.join(chunks)[:12000]
        return state

    def answer(state: RagState) -> RagState:
        with timer(state['metrics'], 'answer'):
            prompt = ANSWER_PROMPT.format(question=state['question'], context=state['context'])
            state['answer'] = llm.invoke(prompt)
        return state

    def grader(state: RagState) -> RagState:
        with timer(state['metrics'], 'grader'):
            prompt = GRADER_PROMPT.format(
                question=state['question'], context=state['context'], answer=state['answer']
            )
            parsed = safe_json_loads(llm.invoke(prompt), fallback={'grade': 'no', 'reason': 'Invalid grader JSON', 'improved_query': state['question']})
            state['grade'] = str(parsed.get('grade', 'no')).lower()
            state['grader_reason'] = str(parsed.get('reason', ''))
            if state['grade'] != 'yes':
                state['search_query'] = str(parsed.get('improved_query') or state['question'])
                state['retries'] += 1
        return state

    def route(state: RagState) -> str:
        max_retries = state.get('max_retries') or settings.max_retries
        if state['grade'] == 'yes' or state['retries'] >= max_retries:
            return 'end'
        return 'retry'

    graph = StateGraph(RagState)
    graph.add_node('planner', planner)
    graph.add_node('retriever', retriever)
    graph.add_node('answer', answer)
    graph.add_node('grader', grader)
    graph.set_entry_point('planner')
    graph.add_edge('planner', 'retriever')
    graph.add_edge('retriever', 'answer')
    graph.add_edge('answer', 'grader')
    graph.add_conditional_edges('grader', route, {'retry': 'planner', 'end': END})
    return graph.compile()
