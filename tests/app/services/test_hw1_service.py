import json
import logging
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest
from redis.asyncio import Redis

from app.models.job_model import JobModel
from app.services.hw1_service import HW1Service


@pytest.fixture
def mock_redis():
    redis = AsyncMock(spec=Redis)
    redis.get = AsyncMock()
    redis.set = AsyncMock()
    return redis


@pytest.fixture
def service(mock_redis):
    return HW1Service(redis=mock_redis)


@pytest.mark.asyncio
async def test_get_data_success(service, mock_redis, caplog):
    key = "test_key"
    payload = {"foo": "bar", "num": 42}
    mock_redis.get.return_value = json.dumps(payload, ensure_ascii=False)

    with caplog.at_level(logging.WARNING):
        result = await service._get_data(key)

    assert result == payload
    mock_redis.get.assert_awaited_once_with(key)


@pytest.mark.asyncio
async def test_get_data_key_not_found(service, mock_redis, caplog):
    key = "missing_key"
    mock_redis.get.return_value = None

    with caplog.at_level(logging.WARNING):
        result = await service._get_data(key)

    assert result is None
    mock_redis.get.assert_awaited_once_with(key)
    assert f"Key not found in Redis: {key}" in caplog.text


@pytest.mark.asyncio
async def test_get_data_invalid_json(service, mock_redis, caplog):
    key = "bad_key"
    mock_redis.get.return_value = "not a json"

    with caplog.at_level(logging.ERROR):
        result = await service._get_data(key)

    assert result is None
    mock_redis.get.assert_awaited_once_with(key)
    assert f"Failed to decode JSON from Redis for key: {key}" in caplog.text


@pytest.mark.asyncio
async def test_set_data(service, mock_redis):
    key = "some_key"
    payload = {"a": 1, "b": "text", "c": None}
    expected_json = json.dumps(payload, ensure_ascii=False)

    await service._set_data(key, payload)

    mock_redis.set.assert_awaited_once_with(key, expected_json)


@pytest.mark.asyncio
async def test_get_report_found(service):
    job_id = "123"
    expected_data = {
        "job_id": job_id,
        "status": "completed",
        "result": {"summary": "OK"},
    }

    with patch.object(
        service, "_get_data", new=AsyncMock(return_value=expected_data)
    ) as mock_get:
        result = await service.get_report(job_id)

    mock_get.assert_awaited_once_with(job_id)
    assert isinstance(result, JobModel)
    assert result.job_id == job_id
    assert result.status == "completed"
    assert result.result == {"summary": "OK"}


@pytest.mark.asyncio
async def test_get_report_not_found(service, caplog):
    job_id = "missing"
    expected_error_msg = f"Report not found for job_id: {job_id}"

    with patch.object(
        service, "_get_data", new=AsyncMock(return_value=None)
    ) as mock_get:
        with caplog.at_level(logging.WARNING):
            result = await service.get_report(job_id)

    mock_get.assert_awaited_once_with(job_id)
    assert isinstance(result, JobModel)
    assert result.job_id == job_id
    assert result.status == "error"
    assert result.result == {"msg": expected_error_msg}
    assert expected_error_msg in caplog.text


@pytest.mark.asyncio
async def test_create_report_success(service):
    user_id = 1
    job_id = "job123"

    with patch.object(service, "_set_data", new=AsyncMock()) as mock_set_data:
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "firstName": "John",
            "email": "john@example.com",
        }

        with patch(
            "httpx.AsyncClient.get", new=AsyncMock(return_value=mock_response)
        ) as mock_http_get:
            mock_todos = {"todos": ["task1", "task2"]}
            with patch(
                "app.services.hw1_service.get_user_todos_sync", return_value=mock_todos
            ) as mock_todos_func:
                # Выполняем метод
                await service.create_report(user_id, job_id)

    # Проверяем, что _set_data вызывалась дважды
    assert mock_set_data.call_count == 2

    # Первый вызов — с статусом running
    first_call_args = mock_set_data.call_args_list[0]
    assert first_call_args[0][0] == job_id
    job_model_running = JobModel(**first_call_args[0][1])
    assert job_model_running.status == "running"
    assert job_model_running.result == {"msg": "Report is generating..."}

    # Второй вызов — с статусом done и результатом
    second_call_args = mock_set_data.call_args_list[1]
    assert second_call_args[0][0] == job_id
    job_model_done = JobModel(**second_call_args[0][1])
    assert job_model_done.status == "done"
    assert job_model_done.result == {
        "user_id": user_id,
        "user_name": "John",
        "email": "john@example.com",
        "todos": ["task1", "task2"],
    }

    mock_http_get.assert_awaited_once_with(f"https://dummyjson.com/users/{user_id}")
    mock_todos_func.assert_called_once_with(user_id)


@pytest.mark.asyncio
async def test_create_report_http_error(service, caplog):
    user_id = 2
    job_id = "job456"

    with patch.object(service, "_set_data", new=AsyncMock()) as mock_set_data:
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.status_code = 404

        with patch(
            "httpx.AsyncClient.get", new=AsyncMock(return_value=mock_response)
        ) as mock_http_get:
            # get_user_todos_sync не должен вызываться, но замокаем на всякий случай
            with patch("app.services.hw1_service.get_user_todos_sync") as mock_todos:
                with caplog.at_level(logging.ERROR):
                    await service.create_report(user_id, job_id)

    # Проверяем, что _set_data вызывалась дважды
    assert mock_set_data.call_count == 2

    # Первый вызов — статус running
    first_call_args = mock_set_data.call_args_list[0]
    assert first_call_args[0][0] == job_id
    job_model_running = JobModel(**first_call_args[0][1])
    assert job_model_running.status == "running"

    # Второй вызов — статус error
    second_call_args = mock_set_data.call_args_list[1]
    assert second_call_args[0][0] == job_id
    job_model_error = JobModel(**second_call_args[0][1])
    assert job_model_error.status == "error"
    expected_msg = f"Failed to fetch user data for user_id: {user_id}, status_code: 404"
    assert job_model_error.result == {"msg": expected_msg}
    assert expected_msg in caplog.text

    mock_todos.assert_not_called()
    # HTTP-запрос вызван один раз
    mock_http_get.assert_awaited_once_with(f"https://dummyjson.com/users/{user_id}")


@pytest.mark.asyncio
async def test_create_report_todos_failure(service):
    user_id = 3
    job_id = "job789"

    with patch.object(service, "_set_data", new=AsyncMock()) as mock_set_data:
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "firstName": "Jane",
            "email": "jane@example.com",
        }

        with patch("httpx.AsyncClient.get", new=AsyncMock(return_value=mock_response)):
            with patch(
                "app.services.hw1_service.get_user_todos_sync",
                side_effect=Exception("DB connection error"),
            ):
                with pytest.raises(Exception, match="DB connection error"):
                    await service.create_report(user_id, job_id)

    assert mock_set_data.call_count == 1
    first_call_args = mock_set_data.call_args_list[0]
    assert first_call_args[0][0] == job_id
    job_model = JobModel(**first_call_args[0][1])
    assert job_model.status == "running"
