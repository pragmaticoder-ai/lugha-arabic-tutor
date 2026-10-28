#!/usr/bin/env bash
# Run frontend + backend locally for development.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
( cd "$ROOT/backend" && python3 -m venv .venv && . .venv/bin/activate \
    && pip install -q -r requirements.txt \
    && uvicorn app.main:app --reload --port 8000 ) &
( cd "$ROOT/frontend/web-app" && npm install && npm run dev ) &
wait
