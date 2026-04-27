# Self-Correcting Enterprise RAG System

A production-oriented system for answering questions from long documents using a structured retrieval pipeline and iterative refinement.

---

## Overview

This project implements a reliable question-answering system for large documents such as technical reports, architecture documents, and financial filings.

Instead of relying on a single retrieval step, the system follows a multi-stage pipeline that retrieves relevant sections, generates an answer, evaluates the result, and retries when necessary.

---

## Architecture

![Self-Correcting RAG Architecture](images/Self-correcting%20RAG%20architecture%20diagram.png)

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

- Long-document QA  
- Structured retrieval  
- Retry mechanism  
- Latency tracking  
- CLI + UI + API  
- Docker support  

---

## Setup

python -m venv venv  
source venv/bin/activate  
pip install -r requirements.txt  

---

## Run

python -m app.cli --pdf "data/sample.pdf" --question "What is this document about?"

---

## UI

PYTHONPATH=. streamlit run app/demo.py  
http://localhost:8501  

---

## API

uvicorn app.api:app --reload  
http://localhost:8000/docs  

---

## Summary

A clean implementation of a long-document QA system with structured retrieval and iterative refinement.
