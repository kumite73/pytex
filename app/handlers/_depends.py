from app.core import redis_helper
from app.services.hw1_service import HW1Service


async def get_hw1_service() -> HW1Service:
    return HW1Service(redis_helper.client)
