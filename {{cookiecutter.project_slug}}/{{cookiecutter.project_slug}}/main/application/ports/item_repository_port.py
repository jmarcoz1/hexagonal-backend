"""Item repository port -- the contract that driven adapters must implement."""

from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from {{ cookiecutter.project_slug }}.main.domain.item import Item


class ItemRepositoryPort(ABC):
    """Abstract interface for Item persistence."""

    @abstractmethod
    def find_all(self) -> list[Item]:
        ...

    @abstractmethod
    def find_by_id(self, item_id: UUID) -> Optional[Item]:
        ...

    @abstractmethod
    def save(self, item: Item) -> Item:
        ...

    @abstractmethod
    def delete(self, item_id: UUID) -> None:
        ...
