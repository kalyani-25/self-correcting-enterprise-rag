from pydantic import BaseModel, Field
from typing import Any


class AskRequest(BaseModel):
    pdf_path: str = Field(..., description='Local PDF path, e.g. data/nvidia-10k.pdf')
    question: str
    max_retries: int | None = None


class AskResponse(BaseModel):
    request_id: str
    question: str
    answer: str
    grade: str
    grader_reason: str
    selected_nodes: list[str]
    retries: int
    metrics: dict[str, Any]


class MetricsResponse(BaseModel):
    total_requests: int
    successful_requests: int
    failed_requests: int
    avg_latency_ms: float
    avg_retries: float
    last_requests: list[dict[str, Any]]
