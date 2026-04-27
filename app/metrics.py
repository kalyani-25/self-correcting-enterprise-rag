from __future__ import annotations
import threading
from collections import deque
from statistics import mean
from typing import Any
from contextlib import contextmanager
from time import perf_counter


class MetricsStore:
    def __init__(self, max_items: int = 100):
        self._lock = threading.Lock()
        self._items: deque[dict[str, Any]] = deque(maxlen=max_items)

    def add(self, item: dict[str, Any]) -> None:
        with self._lock:
            self._items.append(item)

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            items = list(self._items)
        total = len(items)
        successes = sum(1 for x in items if x.get('grade') == 'yes')
        failures = total - successes
        latencies = [x.get('total_latency_ms', 0) for x in items]
        retries = [x.get('retries', 0) for x in items]
        return {
            'total_requests': total,
            'successful_requests': successes,
            'failed_requests': failures,
            'avg_latency_ms': round(mean(latencies), 2) if latencies else 0.0,
            'avg_retries': round(mean(retries), 2) if retries else 0.0,
            'last_requests': items[-10:],
        }


metrics_store = MetricsStore()


@contextmanager
def timer(metrics: dict[str, Any], name: str):
    start = perf_counter()
    yield
    metrics[f'{name}_latency_ms'] = round((perf_counter() - start) * 1000, 2)
