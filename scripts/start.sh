#!/usr/bin/env bash
# Chạy backend (8000) và frontend dev (5173) nền; log ở .logs/
cd "$(dirname "$0")/.."
mkdir -p .logs
pkill -f "uvicorn server:app" 2>/dev/null || true
pkill -f "vite --host" 2>/dev/null || true
(cd backend && nohup python -m uvicorn server:app --host 0.0.0.0 --port 8000 > ../.logs/backend.log 2>&1 &)
(cd frontend && nohup npm run dev > ../.logs/frontend.log 2>&1 &)
echo "Backend: http://localhost:8000  |  Giao diện: http://localhost:5173"
