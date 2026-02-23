"""Integration tests for the Item API endpoints."""

from unittest.mock import MagicMock
from uuid import uuid4

from {{ cookiecutter.project_slug }}.main.domain.item import Item


class TestHealthEndpoints:
    def test_health(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_readiness(self, client):
        response = client.get("/ready")
        assert response.status_code == 200
        assert response.json()["status"] == "ready"


class TestItemController:
    def test_create_item(self, app, client):
        mock_repo = MagicMock()
        test_item = Item(name="Test", description="A test item")
        mock_repo.save.return_value = test_item

        with app.container.item_repository.override(mock_repo):
            response = client.post(
                "/api/v1/items",
                json={"name": "Test", "description": "A test item"},
            )

        assert response.status_code == 201
        assert response.json()["name"] == "Test"

    def test_list_items(self, app, client):
        mock_repo = MagicMock()
        mock_repo.find_all.return_value = [
            Item(name="A"),
            Item(name="B"),
        ]

        with app.container.item_repository.override(mock_repo):
            response = client.get("/api/v1/items")

        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_get_item_not_found(self, app, client):
        mock_repo = MagicMock()
        mock_repo.find_by_id.return_value = None

        with app.container.item_repository.override(mock_repo):
            response = client.get(f"/api/v1/items/{uuid4()}")

        assert response.status_code == 404

    def test_delete_item(self, app, client):
        item_id = uuid4()
        mock_repo = MagicMock()
        mock_repo.find_by_id.return_value = Item(id=item_id, name="Test")

        with app.container.item_repository.override(mock_repo):
            response = client.delete(f"/api/v1/items/{item_id}")

        assert response.status_code == 204
