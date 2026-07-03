from unittest.mock import AsyncMock

from pytest import fixture

from app import main_app
from app.handlers._depends import get_hw1_service
from app.models.job_model import JobModel
from app.services.hw1_service import HW1Service


@fixture
def job_model_fixture():
    return JobModel(
        job_id="job_id_123",
        status="done",
        result={"msg": "Report is generating..."},
    )


def test_hw1_post_success(client, mocker):
    job_id = "job_id_123"
    result_fixture = JobModel(
        job_id=job_id,
        status="started",
        result={"msg": "Report generation started"},
    )
    mocker.patch("uuid.uuid4", return_value=job_id)
    mock_create_task = mocker.patch("app.handlers.hw1_handlers.asyncio.create_task")
    mock_service = AsyncMock(spec=HW1Service)
    mock_service.create_report.return_value = None
    main_app.dependency_overrides[get_hw1_service] = lambda: mock_service

    response = client.post("/hw1/reports/1")
    assert response.status_code == 200
    assert response.json() == result_fixture.model_dump()
    mock_service.create_report.assert_called_once_with(1, job_id)
    mock_create_task.assert_called_once()


def test_hw1_get_success(client, job_model_fixture):
    job_id = "job_id_123"
    mock_service = AsyncMock(spec=HW1Service)
    mock_service.get_report.return_value = job_model_fixture
    main_app.dependency_overrides[get_hw1_service] = lambda: mock_service

    response = client.get(f"/hw1/reports/jobs/{job_id}")
    assert response.status_code == 200
    assert response.json() == job_model_fixture.model_dump()

    mock_service.get_report.assert_called_once_with(job_id)

    main_app.dependency_overrides.clear()
