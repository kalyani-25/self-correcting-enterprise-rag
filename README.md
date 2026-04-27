# Self-Correcting Enterprise RAG System

A production-oriented system for answering questions from long documents using a structured retrieval pipeline and iterative refinement.

---

## Overview

This project implements a reliable question-answering system for large documents such as technical reports, architecture documents, and financial filings.

Instead of relying on a single retrieval step, the system follows a multi-stage pipeline that retrieves relevant sections, generates an answer, evaluates the result, and retries when necessary.

---

## System Workflow

User → UI / API → Processing Pipeline  
→ Retrieve relevant sections  
→ Generate answer  
→ Evaluate result  
→ Retry if needed  
→ Return final response  

---

## Features

- Long-document question answering  
- Structured retrieval pipeline  
- Retry mechanism for incomplete answers  
- Latency and retry tracking  
- CLI for testing  
- Streamlit UI for demo  
- FastAPI backend  
- Docker support  

---

## Project Structure


app/
├── cli.py
├── pipeline.py
├── graph.py
├── llm.py
├── api.py
├── demo.py

data/
outputs/
scripts/
tests/


---

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Environment
OPENAI_API_KEY=your_key
USE_MOCK_LLM=true
USE_MOCK_PAGEINDEX=true
Run CLI
python -m app.cli \
  --pdf "data/sample.pdf" \
  --question "What is this document about?"
Run UI
PYTHONPATH=. streamlit run app/demo.py

http://localhost:8501

Run API
uvicorn app.api:app --reload

http://localhost:8000/docs

Example Output

Answer generated from document
Retries: 0
Latency: ~12 ms
Selected Sections: ["overview", "architecture"]

Docker
docker-compose up --build
Purpose

This project demonstrates building a reliable long-document QA system with:

structured retrieval
iterative refinement
basic observability

---

