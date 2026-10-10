.PHONY: install dev test

install:
	pip install -r backend/requirements.txt
	npm --prefix frontend install --no-audit --no-fund

# Chạy backend (8000) nền + giao diện (5173); Ctrl+C dừng cả hai
dev:
	cd backend && python -m uvicorn server:app --host 0.0.0.0 --port 8000 & \
	trap 'kill %1' EXIT; npm --prefix frontend run dev

test:
	python -m pytest tests
