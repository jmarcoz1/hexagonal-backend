# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Getting Started

### Prerequisites

- Python {{ cookiecutter.python_version }}+
- [uv](https://docs.astral.sh/uv/)
- Docker & Docker Compose

### Setup

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Start Postgres:
   ```bash
   make docker-up
   ```

3. Create and run migrations:
   ```bash
   make migration msg="initial"
   make migrate
   ```

4. Start the app:
   ```bash
   make run
   ```

5. Open http://localhost:8000/docs for the Swagger UI.

### Testing

```bash
make test          # all tests
make test-unit     # unit tests only
make test-integration  # integration tests only
```

## Architecture

This project follows hexagonal architecture (ports and adapters):

```
{{ cookiecutter.project_slug }}/main/
├── boot/          # App bootstrap, DI containers, configuration
├── domain/        # Pure business entities and rules
├── application/   # Use cases, services, port interfaces (ABCs)
├── driving/       # Primary adapters (REST API)
└── driven/        # Secondary adapters (database, external services)
```

### Dependency Flow

```
driving (REST) → application (services) → ports (ABCs)
                                              ↑
                                    driven (repositories) implements ports
```

The domain layer has zero external dependencies. The application layer depends only on the domain and defines port interfaces. Driven adapters implement those ports.
