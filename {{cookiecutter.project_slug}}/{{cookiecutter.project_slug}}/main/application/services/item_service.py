"""Item application service -- orchestrates use cases."""

from uuid import UUID

from {{ cookiecutter.project_slug }}.main.application.ports.item_repository_port import ItemRepositoryPort
from {{ cookiecutter.project_slug }}.main.domain.exceptions import ItemNotFoundException
from {{ cookiecutter.project_slug }}.main.domain.item import Item


class ItemService:
    """Application service for Item use cases."""

    def __init__(self, item_repository: ItemRepositoryPort) -> None:
        self._repository = item_repository

    def get_all_items(self) -> list[Item]:
        return self._repository.find_all()

    def get_item(self, item_id: UUID) -> Item:
        item = self._repository.find_by_id(item_id)
        if item is None:
            raise ItemNotFoundException(str(item_id))
        return item

    def create_item(self, name: str, description: str = "") -> Item:
        item = Item(name=name, description=description)
        return self._repository.save(item)

    def delete_item(self, item_id: UUID) -> None:
        self.get_item(item_id)
        self._repository.delete(item_id)
