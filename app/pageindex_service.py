from __future__ import annotations
import logging
import time
from pathlib import Path
from typing import Any
from app.config import get_settings
from app.utils import flatten_tree

logger = logging.getLogger(__name__)


class PageIndexService:
    """Production wrapper around PageIndex with a mock fallback for demos/tests.

    Live mode expects the external `pageindex` package and PAGEINDEX_API_KEY.
    Mock mode creates a deterministic tree from the local PDF filename so the
    rest of the production pipeline can be tested without vendor lock-in.
    """

    def __init__(self):
        self.settings = get_settings()
        self.mock = self.settings.use_mock_pageindex or not self.settings.pageindex_api_key
        self.client = None
        if not self.mock:
            try:
                from pageindex import PageIndexClient  # type: ignore
                self.client = PageIndexClient(api_key=self.settings.pageindex_api_key)
            except Exception as exc:
                logger.warning('Falling back to mock PageIndex mode: %s', exc)
                self.mock = True

    def build_index(self, pdf_path: str) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
        path = Path(pdf_path)
        if not path.exists():
            raise FileNotFoundError(f'PDF not found: {pdf_path}')
        if self.mock:
            tree = self._mock_tree(path)
        else:
            doc_id = self.client.submit_document(str(path))['doc_id']
            self._wait_until_ready(doc_id)
            raw = self.client.get_tree(doc_id, node_summary=True)
            tree = raw.get('result', raw)
        node_map = flatten_tree(tree)
        return tree, node_map

    def _wait_until_ready(self, doc_id: str, timeout_sec: int = 900) -> None:
        start = time.perf_counter()
        while not self.client.is_retrieval_ready(doc_id):
            if time.perf_counter() - start > timeout_sec:
                raise TimeoutError('PageIndex processing timed out')
            time.sleep(8)

    def _mock_tree(self, path: Path) -> list[dict[str, Any]]:
        name = path.name
        return [
            {
                'id': 'node_001',
                'title': f'{name} - Business Overview',
                'summary': 'Business model, product segments, revenue drivers, customers, and market overview.',
                'page': 1,
                'text': 'This section summarizes the company business, products, customers, demand drivers, revenue mix, and market environment.',
                'children': [
                    {'id': 'node_001a', 'title': 'Revenue and Customers', 'summary': 'Revenue concentration and major customer discussion.', 'page': 8, 'text': 'Revenue can be concentrated among large customers and demand can vary by product cycle.', 'children': []},
                ],
            },
            {
                'id': 'node_002',
                'title': f'{name} - Risk Factors',
                'summary': 'Supply chain, export controls, geopolitical, customer concentration, cybersecurity, and manufacturing risks.',
                'page': 25,
                'text': 'Risk factors include supply chain disruptions, dependency on manufacturing partners, export controls, geopolitical restrictions, customer concentration, cybersecurity threats, and changes in demand.',
                'children': [
                    {'id': 'node_002a', 'title': 'Supply Chain Risks', 'summary': 'Manufacturing constraints, suppliers, logistics, and availability risks.', 'page': 28, 'text': 'Supply chain risks include limited manufacturing capacity, component shortages, supplier dependency, shipping delays, and inability to meet customer demand.', 'children': []},
                    {'id': 'node_002b', 'title': 'Export Control Risks', 'summary': 'Government restrictions impacting product sales and customers.', 'page': 32, 'text': 'Export controls and trade restrictions can limit sales to certain countries and customers, reduce revenue, and require product redesigns or licensing.', 'children': []},
                ],
            },
            {
                'id': 'node_003',
                'title': f'{name} - Financial Statements',
                'summary': 'Income statement, balance sheet, cash flows, and notes.',
                'page': 70,
                'text': 'Financial statements include revenue, operating income, net income, assets, liabilities, cash flow, and accounting notes.',
                'children': [],
            },
        ]
