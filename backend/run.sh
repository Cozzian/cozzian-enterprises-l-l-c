#!/usr/bin/env bash
# ===========================================================================
# Cozzian Enterprises LLC — LabSync API Server
# Starts the FastAPI backend on port 8000
# ===========================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Cozzian LabSync API ==="
echo "Installing dependencies..."
pip install -q -r requirements.txt

echo "Starting server on port 8000..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-level info