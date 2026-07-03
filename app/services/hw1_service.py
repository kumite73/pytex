import asyncio
import json
import logging

import httpx
from redis.asyncio import Redis

from app.models.job_model import JobModel
from app.services.legacy_client import get_user_todos_sync

log = logging.getLogger(__name__)


class HW1Service:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def create_report(self, user_id: int, job_id: str) -> None:
        job = JobModel(
            job_id=job_id,
            status="running",
            result={"msg": "Report is generating..."},
        )
        _, user = await asyncio.gather(
            self._set_data(job_id, job.model_dump()),
            httpx.AsyncClient().get(f"https://dummyjson.com/users/{user_id}"),
        )
        if user.status_code != 200:
            error_msg = f"Failed to fetch user data for user_id: {user_id}, status_code: {user.status_code}"
            log.error(error_msg)
            await self._set_data(
                job_id,
                JobModel(
                    job_id=job_id, status="error", result={"msg": error_msg}
                ).model_dump(),
            )
            return
        user_data = user.json()
        result = {
            "user_id": user_id,
            "user_name": user_data["firstName"],
            "email": user_data["email"],
        }
        todos = await asyncio.to_thread(get_user_todos_sync, user_id)
        result.update(todos)
        job.status = "done"
        job.result = result
        await self._set_data(job_id, job.model_dump())

    async def get_report(self, job_id: str) -> JobModel:
        data = await self._get_data(job_id)
        if not data:
            error_msg = f"Report not found for job_id: {job_id}"
            log.warning(error_msg)
            return JobModel(job_id=job_id, status="error", result={"msg": error_msg})
        return JobModel(**data)

    async def _get_data(self, key: str) -> dict | None:
        result = await self.redis.get(key)
        if not result:
            log.warning(f"Key not found in Redis: {key}")
            return None
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            log.error(f"Failed to decode JSON from Redis for key: {key}")
            return None

    async def _set_data(self, key: str, payload: dict) -> None:
        json_str = json.dumps(payload, ensure_ascii=False)
        await self.redis.set(key, json_str)
