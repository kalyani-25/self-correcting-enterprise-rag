# Self-Correcting Enterprise RAG

A production-engineer-level long-document QA system that combines **PageIndex-style hierarchical retrieval** with a **LangGraph deterministic planner → retriever → answer → grader retry loop**.

This project is designed for AI/ML, SDE, MLOps, and agentic AI roles. It demonstrates not just RAG, but production thinking: API design, metrics, evaluation, logging, Docker, CI, and demo UX.

---

## Why this project matters

Typical RAG systems chunk a document and run similarity search. That often fails on 100+ page enterprise documents because document structure, table of contents, section hierarchy, and long-range dependencies are lost.

This system instead uses hierarchical document reasoning and a self-correction loop:

```text
PDF → PageIndex Tree → Planner → Retriever → Answer Generator → Grader → Retry if incomplete
```

---

## Core features

- Hierarchical document indexing through PageIndex or mock PageIndex mode
- LangGraph state machine for deterministic agent execution
- LLM-as-Judge grading and retry loop
- FastAPI backend with `/ask`, `/health`, and `/metrics`
- Streamlit demo UI for recruiter-friendly demos
- Structured JSON logging with request IDs
- Latency and retry metrics
- Batch evaluation pipeline
- Docker and Docker Compose support
- GitHub Actions CI
- Unit and API tests

---

## Architecture

```text
                       ┌────────────────────┐
                       │ 100+ page PDF       │
                       └─────────┬──────────┘
                                 │
                                 ▼
                       ┌────────────────────┐
                       │ PageIndex Service   │
                       │ hierarchical tree   │
                       └─────────┬──────────┘
                                 │
                                 ▼
┌──────────┐   ┌───────────┐   ┌────────────┐   ┌──────────┐
│ Planner  │ → │ Retriever │ → │ Answer LLM │ → │ Grader   │
└────┬─────┘   └───────────┘   └────────────┘   └────┬─────┘
     ▲                                                │
     └──────────── retry with improved query ─────────┘
```

---

## Quick start

### 1. Create environment

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
```

Update `.env`:

```env
OPENAI_API_KEY=your_openai_key_here
USE_MOCK_PAGEINDEX=true
```

Mock mode lets the app run without a PageIndex key. For live PageIndex mode, set:

```env
PAGEINDEX_API_KEY=your_pageindex_key_here
USE_MOCK_PAGEINDEX=false
```

### 3. Add a PDF

Place any 100+ page PDF into `data/`, for example:

```text
data/nvidia-10k.pdf
```

### 4. Run from CLI

```bash
python -m app.cli \
  --pdf data/nvidia-10k.pdf \
  --question "What are the main supply chain and export control risks?"
```

### 5. Run API

```bash
./scripts/run_api.sh
```

Then call:

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"pdf_path":"data/nvidia-10k.pdf","question":"What are the main supply chain risks?"}'
```

Metrics:

```bash
curl http://localhost:8000/metrics
```

### 6. Run Streamlit demo

```bash
./scripts/run_demo.sh
```

Open:

```text
http://localhost:8501
```

---

## Docker

```bash
docker compose up --build
```

API:

```text
http://localhost:8000
```

Demo:

```text
http://localhost:8501
```

---

## Evaluation

Create a JSONL file with questions and ground truth answers:

```json
{"question":"What are the main supply chain risks?","ground_truth":"supplier dependency and manufacturing capacity"}
```

Run:

```bash
python -m app.eval_cli \
  --pdf data/nvidia-10k.pdf \
  --questions data/eval_questions.jsonl \
  --output outputs/eval_results.csv
```

---

## Production engineering highlights

| Area | Implementation |
|---|---|
| Agent orchestration | LangGraph state machine |
| Retrieval | PageIndex hierarchical document tree |
| Reliability | Grade-and-retry loop |
| Observability | Latency, retries, request IDs, metrics endpoint |
| Backend | FastAPI async wrapper |
| Demo | Streamlit UI |
| Deployment | Docker + Docker Compose |
| Quality | Tests + GitHub Actions |

---

## Resume bullet

Built a production-ready self-correcting enterprise RAG system using PageIndex and LangGraph, implementing deterministic planner–retriever–grader workflows with retry logic; deployed FastAPI and Streamlit interfaces with structured logging, evaluation, latency tracking, and Docker-based deployment for long-document QA over 100+ page financial filings.

---

## Interview pitch

“I built a self-correcting enterprise document AI system. Instead of simply chunking and embedding a PDF, the system builds a hierarchical document tree, uses LangGraph to plan which section to inspect, retrieves the relevant branch, generates an answer, and then uses an LLM-as-Judge to verify whether the answer is complete. If not, it rewrites the query and retries. I also wrapped it with FastAPI, Streamlit, Docker, metrics, logging, and a batch evaluation pipeline to make it production-ready.”

---

## Suggested LinkedIn post

**Beyond Vector RAG: Building a Self-Correcting Enterprise Document Agent**

Most RAG demos work on small text chunks, but enterprise documents are messy: 100+ page PDFs, nested sections, tables, risk factors, financial notes, and cross-references.

I built a production-ready long-document QA system using:

- PageIndex-style hierarchical retrieval
- LangGraph deterministic planner → retriever → grader loops
- LLM-as-Judge self-correction
- FastAPI backend
- Streamlit demo UI
- Docker deployment
- latency, retry, and evaluation metrics

The key idea: if the agent retrieves the wrong section, it does not blindly answer. It grades itself, rewrites the retrieval query, and retries.

This is the shift from “RAG demo” to auditable AI engineering.
