from pydantic import BaseModel, Field


class JobModel(BaseModel):
    job_id: str
    status: str
    result: dict = Field(default_factory=dict)
