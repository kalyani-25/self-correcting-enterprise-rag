from __future__ import annotations
from time import perf_counter
from uuid import uuid4
import logging
from typing import Any
from app.config import get_settings
from app.graph import build_graph
from app.metrics import metrics_store
from app.pageindex_service import PageIndexService

logger = logging.getLogger(__name__)


def run_pipeline(pdf_path: str, question: str, max_retries: int | None = None, request_id: str | None = None) -> dict[str, Any]:
    request_id = request_id or str(uuid4())
    settings = get_settings()
    start = perf_counter()

    logger.info('pipeline_started', extra={'request_id': request_id})
    service = PageIndexService()
    tree, node_map = service.build_index(pdf_path)

    graph = build_graph()
    initial_state = {
        'request_id': request_id,
        'question': question,
        'search_query': question,
        'tree': tree,
        'node_map': node_map,
        'selected_nodes': [],
        'context': '',
        'answer': '',
        'grade': 'no',
        'grader_reason': '',
        'retries': 0,
        'max_retries': max_retries if max_retries is not None else settings.max_retries,
        'metrics': {},
    }
    result = graph.invoke(initial_state)
    total_ms = round((perf_counter() - start) * 1000, 2)
    result['metrics']['total_latency_ms'] = total_ms
    result['metrics']['retries'] = result['retries']
    result['metrics']['selected_nodes'] = result['selected_nodes']

    metrics_store.add({
        'request_id': request_id,
        'question': question,
        'grade': result['grade'],
        'retries': result['retries'],
        'total_latency_ms': total_ms,
    })
    logger.info('pipeline_completed', extra={'request_id': request_id, 'latency_ms': total_ms, 'retries': result['retries']})

    return {
        'request_id': request_id,
        'question': result['question'],
        'answer': result['answer'],
        'grade': result['grade'],
        'grader_reason': result['grader_reason'],
        'selected_nodes': result['selected_nodes'],
        'retries': result['retries'],
        'metrics': result['metrics'],
    }
