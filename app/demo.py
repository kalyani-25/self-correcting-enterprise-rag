from __future__ import annotations
import json
import tempfile
from pathlib import Path
import streamlit as st
import pandas as pd
from app.pipeline import run_pipeline
from app.metrics import metrics_store

st.set_page_config(page_title='Self-Correcting Enterprise RAG', layout='wide')
st.title('Self-Correcting Enterprise RAG')
st.caption('PageIndex-style hierarchical retrieval + LangGraph planner/retriever/grader retry loop')

with st.sidebar:
    st.header('Configuration')
    max_retries = st.slider('Max retries', 0, 5, 2)
    st.info('Set USE_MOCK_PAGEINDEX=true for local demos without a PageIndex key.')

uploaded = st.file_uploader('Upload a PDF', type=['pdf'])
question = st.text_input('Ask a question', 'What are the main supply chain and export control risks?')

if st.button('Run self-correcting retrieval', type='primary'):
    if not uploaded:
        st.error('Please upload a PDF first.')
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            tmp.write(uploaded.read())
            pdf_path = tmp.name
        with st.spinner('Running LangGraph workflow...'):
            result = run_pipeline(pdf_path, question, max_retries=max_retries)
        st.subheader('Answer')
        st.write(result['answer'])
        c1, c2, c3 = st.columns(3)
        c1.metric('Grade', result['grade'])
        c2.metric('Retries', result['retries'])
        c3.metric('Latency', f"{result['metrics'].get('total_latency_ms', 0)} ms")
        st.subheader('Selected Nodes')
        st.code(json.dumps(result['selected_nodes'], indent=2))
        st.subheader('Latency Breakdown')
        metric_items = {k: v for k, v in result['metrics'].items() if k.endswith('_latency_ms')}
        if metric_items:
            df = pd.DataFrame([{'stage': k.replace('_latency_ms',''), 'latency_ms': v} for k, v in metric_items.items()])
            st.bar_chart(df, x='stage', y='latency_ms')
        with st.expander('Full JSON result'):
            st.json(result)

st.divider()
st.subheader('Service Metrics Snapshot')
st.json(metrics_store.snapshot())
