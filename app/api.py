from __future__ import annotations
from uuid import uuid4
import asyncio
from fastapi import FastAPI, Header, HTTPException
from app.logging_config import configure_logging
from app.metrics import metrics_store
from app.models import AskRequest, AskResponse, MetricsResponse
from app.pipeline import run_pipeline

configure_logging()
app = FastAPI(
    title='Self-Correcting Enterprise RAG',
    description='Production-ready PageIndex + LangGraph long-document QA system',
    version='1.0.0',
)


@app.get('/health')
def health():
    return {'status': 'ok'}


@app.post('/ask', response_model=AskResponse)
async def ask(payload: AskRequest, x_request_id: str | None = Header(default=None)):
    request_id = x_request_id or str(uuid4())
    try:
        result = await asyncio.to_thread(
            run_pipeline,
            payload.pdf_path,
            payload.question,
            payload.max_retries,
            request_id,
        )
        return result
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get('/metrics', response_model=MetricsResponse)
def metrics():
    return metrics_store.snapshot()
