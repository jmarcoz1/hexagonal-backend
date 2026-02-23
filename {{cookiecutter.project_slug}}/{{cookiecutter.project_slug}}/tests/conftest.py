"""Shared test fixtures."""

import pytest
from fastapi.testclient import TestClient

from {{ cookiecutter.project_slug }}.main.boot.app import create_app


@pytest.fixture
def app():
    """Create application for testing."""
    return create_app()


@pytest.fixture
def client(app):
    """Create test HTTP client."""
    return TestClient(app)
