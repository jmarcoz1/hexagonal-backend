.PHONY: run test test-unit test-integration migrate migration docker-up docker-down docker-all

run:
	APP_PROFILE=local uv run uvicorn {{ cookiecutter.project_slug }}.main.boot.app:app --reload --host 0.0.0.0 --port 8000

test:
	uv run pytest --cov={{ cookiecutter.project_slug }} -v

test-unit:
	uv run pytest {{ cookiecutter.project_slug }}/tests/unit -v

test-integration:
	uv run pytest {{ cookiecutter.project_slug }}/tests/integration -v

migrate:
	uv run alembic upgrade head

migration:
	uv run alembic revision --autogenerate -m "$(msg)"

docker-up:
	docker compose up -d postgres

docker-down:
	docker compose down

docker-all:
	docker compose up -d --build
