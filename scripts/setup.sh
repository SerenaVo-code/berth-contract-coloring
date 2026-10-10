#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
pip install -r backend/requirements.txt
(cd frontend && npm install --no-audit --no-fund)
