"""Item repository adapter -- implements the port using SQLAlchemy."""

from contextlib import AbstractContextManager
from typing import Callable, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from {{ cookiecutter.project_slug }}.main.application.ports.item_repository_port import ItemRepositoryPort
from {{ cookiecutter.project_slug }}.main.domain.item import Item
from {{ cookiecutter.project_slug }}.main.driven.db.models import ItemModel


class ItemRepositoryAdapter(ItemRepositoryPort):
    """SQLAlchemy implementation of the ItemRepositoryPort."""

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self._session_factory = session_factory

    def find_all(self) -> list[Item]:
        with self._session_factory() as session:
            models = session.query(ItemModel).all()
            return [m.to_domain() for m in models]

    def find_by_id(self, item_id: UUID) -> Optional[Item]:
        with self._session_factory() as session:
            model = session.query(ItemModel).filter(ItemModel.id == item_id).first()
            return model.to_domain() if model else None

    def save(self, item: Item) -> Item:
        with self._session_factory() as session:
            model = ItemModel(
                id=item.id,
                name=item.name,
                description=item.description,
            )
            session.add(model)
            session.commit()
            session.refresh(model)
            return model.to_domain()

    def delete(self, item_id: UUID) -> None:
        with self._session_factory() as session:
            model = session.query(ItemModel).filter(ItemModel.id == item_id).first()
            if model:
                session.delete(model)
                session.commit()
