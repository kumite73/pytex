import logging
from typing import AsyncGenerator, Optional

from redis.asyncio import ConnectionPool, Redis
from redis.exceptions import RedisError

from app.core.config import settings

log = logging.getLogger(__name__)


class RedisHelper:
    """
    Хелпер для работы с Redis. Инициализирует клиент и предоставляет
    методы для получения клиента и закрытия соединений.
    """

    def __init__(
        self,
        url: Optional[str] = None,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        decode_responses: bool = True,
        max_connections: int = 10,
    ) -> None:
        """
        Параметры подключения к Redis.
        Если передан url, он имеет приоритет над host/port.
        """
        self.url = url
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.decode_responses = decode_responses
        self.max_connections = max_connections

        self._client: Optional[Redis] = None
        self._pool: Optional[ConnectionPool] = None

        self._initialize_client()

    def _initialize_client(self) -> None:
        """Создаёт клиент Redis (синхронно, но клиент асинхронный)."""
        try:
            if self.url:
                # Используем URL-строку для подключения
                self._pool = ConnectionPool.from_url(
                    self.url,
                    max_connections=self.max_connections,
                    decode_responses=self.decode_responses,
                )
            else:
                self._pool = ConnectionPool(
                    host=self.host,
                    port=self.port,
                    db=self.db,
                    password=self.password,
                    max_connections=self.max_connections,
                    decode_responses=self.decode_responses,
                )
            self._client = Redis(connection_pool=self._pool)
            log.info("Redis client initialized")
        except RedisError as e:
            log.error(f"Failed to initialize Redis client: {e}")
            raise

    @property
    def client(self) -> Redis:
        """Возвращает клиент Redis. Если клиент не инициализирован, выбрасывает исключение."""
        if self._client is None:
            raise RuntimeError("Redis client is not initialized")
        return self._client

    async def dispose(self) -> None:
        """Закрывает соединения с Redis."""
        if self._client is not None:
            await self._client.close()
            self._client = None
            log.info("Redis client closed")
        if self._pool is not None:
            await self._pool.disconnect()
            self._pool = None
            log.info("Redis connection pool disposed")

    async def redis_getter(self) -> AsyncGenerator[Redis, None]:
        """
        Асинхронный генератор, возвращающий клиент Redis.
        Для использования в FastAPI-зависимостях.
        """
        yield self.client


# Глобальный экземпляр хелпера, инициализируемый из настроек
redis_helper = RedisHelper(
    url=settings.redis.url,
    host=settings.redis.host,
    port=settings.redis.port,
    db=settings.redis.db,
    password=settings.redis.password,
    max_connections=settings.redis.max_connections,
    decode_responses=True,
)
