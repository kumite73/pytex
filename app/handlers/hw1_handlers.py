import asyncio
import uuid

from fastapi import APIRouter, Depends

from app.models.job_model import JobModel
from app.services.hw1_service import HW1Service

from ._depends import get_hw1_service

router: APIRouter = APIRouter(prefix="/hw1", tags=["hw1"])


@router.post(
    "/reports/{user_id}",
    response_model=JobModel,
)
async def post_hw1_report(
    user_id: int,
    service: HW1Service = Depends(get_hw1_service),
):
    job_id = str(uuid.uuid4())
    asyncio.create_task(service.create_report(user_id, job_id))
    return JobModel(
        job_id=job_id, status="started", result={"msg": "Report generation started"}
    )


@router.get(
    "/reports/jobs/{job_id}",
    response_model=JobModel,
)
async def get_hw1_report(
    job_id: str,
    service: HW1Service = Depends(get_hw1_service),
):
    return await service.get_report(job_id)
