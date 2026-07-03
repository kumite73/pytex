import json
import logging
from typing import Any

from redis.asyncio import Redis

log = logging.getLogger(__name__)


class HW1Service:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_hw1_data(self, key: str) -> Any | None:
        result = await self.redis.get(key)
        if not result:
            log.warning(f"Key not found in Redis: {key}")
            return None
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            log.error(f"Failed to decode JSON from Redis for key: {key}")
            return None

    async def set_hw1_data(self, key: str, payload: Any) -> None:
        json_str = json.dumps(payload, ensure_ascii=False)
        await self.redis.set(key, json_str)
