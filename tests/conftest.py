import pytest
from fastapi.testclient import TestClient

from app import main_app


@pytest.fixture
def client():
    yield TestClient(main_app)

    main_app.dependency_overrides.clear()
