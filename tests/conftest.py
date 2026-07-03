import pytest
from fastapi.testclient import TestClient

from app import main_app


@pytest.fixture
def client(mock_session, monkeypatch):
    # async def override_redis_getter():
    #     yield mock_redis
    # main_app.dependency_overrides[redis_helper.redis_getter] = override_redis_getter

    yield TestClient(main_app)

    main_app.dependency_overrides.clear()
