from typing import ClassVar

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.logging_config import LOGGING_CONFIG


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    socket: str = ""
    workers: int = 1


class LoggingConfig(BaseModel):
    environment: str = "development"
    log_config: ClassVar[dict] = LOGGING_CONFIG


class RedisConfig(BaseSettings):
    url: str | None = None
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: str | None = None
    max_connections: int = 10


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        extra="ignore",
    )
    run: RunConfig = RunConfig()
    logging: LoggingConfig = LoggingConfig()
    redis: RedisConfig = RedisConfig()


settings = Settings()
