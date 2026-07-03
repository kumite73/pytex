from fastapi import APIRouter, Depends

from app.services.hw1_service import HW1Service

from ._depends import get_hw1_service

router: APIRouter = APIRouter(prefix="/hw1", tags=["hw1"])


@router.post(
    "/",
)
async def hw1_set(
    service: HW1Service = Depends(get_hw1_service),
):
    await service.set_hw1_data("hw1_key", {"message": "HW1 has started!"})
    return {"message": "Set HW1 data in Redis."}


@router.get(
    "/",
    description="Returns the HW1 data from Redis.",
)
async def hw1_get(
    service: HW1Service = Depends(get_hw1_service),
):
    data = await service.get_hw1_data("hw1_key")
    if not data:
        return {"message": "HW1 data not found."}
    return data
