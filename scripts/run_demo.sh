#!/usr/bin/env bash
set -euo pipefail
streamlit run app/demo.py --server.port 8501 --server.address 0.0.0.0
