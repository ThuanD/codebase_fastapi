.PHONY: run test lint format build up down

migrations:
	alembic revision --autogenerate -m "$(message)"

migrate:
	alembic upgrade head

run:
	uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload

test:
	pytest tests

coverage:
	pytest --cov=app --cov-report=term-missing --cov-report=html --cov-report=xml

lint:
	ruff check .

lint-fix:
	ruff check . --fix

format:
	ruff format .

format-check:
	ruff format . --check

hooks:
	pre-commit run --all-files

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down
