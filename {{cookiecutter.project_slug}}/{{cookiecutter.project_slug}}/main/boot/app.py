"""FastAPI application factory."""

from fastapi import FastAPI

from {{ cookiecutter.project_slug }}.main.boot.config import load_config
from {{ cookiecutter.project_slug }}.main.boot.containers import Container
from {{ cookiecutter.project_slug }}.main.driving.api_rest import health_controller, item_controller


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = load_config()

    container = Container()
    container.config.from_dict({
        "database": {
            "url": settings.database.url,
            "pool_size": settings.database.pool_size,
            "max_overflow": settings.database.max_overflow,
            "echo": settings.database.echo,
        }
    })

    application = FastAPI(
        title=settings.app.name,
        version=settings.app.version,
        description="{{ cookiecutter.project_description }}",
    )

    application.container = container

    application.include_router(health_controller.router, tags=["Health"])
    application.include_router(item_controller.router, prefix="/api/v1", tags=["Items"])

    return application


app = create_app()
