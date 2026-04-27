from __future__ import annotations
import json
import re
from typing import Any


def safe_json_loads(text: str, fallback: dict[str, Any] | None = None) -> dict[str, Any]:
    fallback = fallback or {}
    try:
        return json.loads(text)
    except Exception:
        match = re.search(r'\{.*\}', text, flags=re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                return fallback
        return fallback


def flatten_tree(tree: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    node_map: dict[str, dict[str, Any]] = {}

    def visit(node: dict[str, Any]):
        node_id = str(node.get('id') or node.get('node_id') or f"node_{len(node_map)+1:03d}")
        node['id'] = node_id
        node_map[node_id] = node
        for child in node.get('children', []) or []:
            visit(child)

    for root in tree:
        visit(root)
    return node_map


def strip_text_for_planning(tree: list[dict[str, Any]], limit: int = 80) -> list[dict[str, Any]]:
    def clone(node: dict[str, Any]) -> dict[str, Any]:
        return {
            'id': node.get('id'),
            'title': node.get('title', ''),
            'summary': node.get('summary', '')[:500],
            'page': node.get('page', node.get('page_index', 'unknown')),
            'children': [clone(c) for c in (node.get('children', []) or [])[:8]],
        }
    return [clone(n) for n in tree[:limit]]
