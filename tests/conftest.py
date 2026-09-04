"""Shared pytest fixtures for the math API test suite."""

import pytest

from app import create_app


@pytest.fixture
def client():
    """Build a test client from a fresh app instance via create_app()."""
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client
