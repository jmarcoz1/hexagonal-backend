# Hexagonal Backend Cookiecutter Template

A [Cookiecutter](https://cookiecutter.readthedocs.io/) template for generating Python backends with hexagonal architecture (ports and adapters).

## Usage

```bash
pip install cookiecutter
cookiecutter gh:your-username/hexagonal-backend
```

Or from a local clone:

```bash
cookiecutter /path/to/hexagonal-backend
```

## Tech Stack

- **Python 3.12+** with [uv](https://docs.astral.sh/uv/) package manager
- **FastAPI** + Uvicorn
- **SQLAlchemy** + Alembic + PostgreSQL
- **dependency-injector** for dependency injection
- **pydantic-settings** + pyaml-env for configuration
- **Docker Compose** for local development (Postgres)
- **pytest** for testing

## Architecture

The generated project follows hexagonal architecture:

- `domain/` -- Pure business entities and rules (no framework dependencies)
- `application/` -- Use cases, services, and port interfaces (ABCs)
- `driving/` -- Primary adapters (REST API controllers)
- `driven/` -- Secondary adapters (database repositories, external clients)
- `boot/` -- Application bootstrap, DI containers, configuration

## Template Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `project_name` | My Hexagonal Backend | Human-readable project name |
| `project_slug` | *(derived)* | Python package name (auto-generated) |
| `project_description` | A Python backend... | Short project description |
| `author_name` | Your Name | Author name |
| `author_email` | your.email@example.com | Author email |
| `python_version` | 3.12 | Python version |
