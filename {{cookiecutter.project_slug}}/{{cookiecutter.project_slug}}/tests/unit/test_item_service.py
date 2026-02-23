"""Unit tests for ItemService."""

from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from {{ cookiecutter.project_slug }}.main.application.services.item_service import ItemService
from {{ cookiecutter.project_slug }}.main.domain.exceptions import ItemNotFoundException
from {{ cookiecutter.project_slug }}.main.domain.item import Item


@pytest.fixture
def mock_repository():
    return MagicMock()


@pytest.fixture
def service(mock_repository):
    return ItemService(item_repository=mock_repository)


class TestItemService:
    def test_create_item(self, service, mock_repository):
        mock_repository.save.return_value = Item(name="Test", description="Desc")

        result = service.create_item(name="Test", description="Desc")

        assert result.name == "Test"
        assert result.description == "Desc"
        mock_repository.save.assert_called_once()

    def test_get_all_items(self, service, mock_repository):
        mock_repository.find_all.return_value = [
            Item(name="A"),
            Item(name="B"),
        ]

        result = service.get_all_items()

        assert len(result) == 2
        assert result[0].name == "A"
        assert result[1].name == "B"

    def test_get_item(self, service, mock_repository):
        item_id = uuid4()
        mock_repository.find_by_id.return_value = Item(id=item_id, name="Test")

        result = service.get_item(item_id)

        assert result.id == item_id
        assert result.name == "Test"

    def test_get_item_not_found(self, service, mock_repository):
        mock_repository.find_by_id.return_value = None

        with pytest.raises(ItemNotFoundException):
            service.get_item(uuid4())

    def test_delete_item(self, service, mock_repository):
        item_id = uuid4()
        mock_repository.find_by_id.return_value = Item(id=item_id, name="Test")

        service.delete_item(item_id)

        mock_repository.delete.assert_called_once_with(item_id)

    def test_delete_item_not_found(self, service, mock_repository):
        mock_repository.find_by_id.return_value = None

        with pytest.raises(ItemNotFoundException):
            service.delete_item(uuid4())
