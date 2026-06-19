.PHONY: help setup install dev test lint format clean docker-up docker-down migrate deploy

help:
	@echo "Enterprise Knowledge Assistant - Makefile"
	@echo ""
	@echo "Available commands:"
	@echo "  make setup          - Create virtual environment"
	@echo "  make install        - Install dependencies"
	@echo "  make dev            - Run development server"
	@echo "  make test           - Run tests"
	@echo "  make lint           - Lint code"
	@echo "  make format         - Format code"
	@echo "  make clean          - Clean up cache files"
	@echo "  make docker-up      - Start Docker services"
	@echo "  make docker-down    - Stop Docker services"
	@echo "  make migrate        - Run migrations"
	@echo "  make deploy         - Deploy to Railway"

setup:
	python3.10 -m venv venv
	@echo "Virtual environment created. Run: source venv/bin/activate"

install:
	pip install -r requirements.txt

dev:
	python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

test:
	python test_auth.py

lint:
	ruff check .

format:
	black .

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .pytest_cache .coverage htmlcov dist build *.egg-info

docker-up:
	docker-compose up -d
	sleep 10
	@echo "Database running. Run: alembic upgrade head"

docker-down:
	docker-compose down

migrate:
	alembic upgrade head

deploy:
	railway up

logs:
	railway logs -f

status:
	railway status

variables:
	railway variable list
