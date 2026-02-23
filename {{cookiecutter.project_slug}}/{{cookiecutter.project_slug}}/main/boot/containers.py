"""Dependency injection container using dependency-injector."""

from dependency_injector import containers, providers

from {{ cookiecutter.project_slug }}.main.application.services.item_service import ItemService
from {{ cookiecutter.project_slug }}.main.driven.db.database import Database
from {{ cookiecutter.project_slug }}.main.driven.db.item_repository import ItemRepositoryAdapter


class Container(containers.DeclarativeContainer):
    """Application DI container."""

    wiring_config = containers.WiringConfiguration(
        modules=[
            "{{ cookiecutter.project_slug }}.main.driving.api_rest.item_controller",
            "{{ cookiecutter.project_slug }}.main.driving.api_rest.health_controller",
        ]
    )

    config = providers.Configuration()

    db = providers.Singleton(
        Database,
        db_url=config.database.url,
        pool_size=config.database.pool_size,
        max_overflow=config.database.max_overflow,
        echo=config.database.echo,
    )

    item_repository = providers.Factory(
        ItemRepositoryAdapter,
        session_factory=db.provided.session,
    )

    item_service = providers.Factory(
        ItemService,
        item_repository=item_repository,
    )
