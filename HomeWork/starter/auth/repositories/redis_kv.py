from __future__ import annotations
from typing import cast
import redis
import redis.asyncio as async_redis
from auth.config import Settings

class RedisCodeRepository:
    def __init__(self, settings: Settings) -> None:
        # Исправлено: используем redis_dsn
        self.client = redis.from_url(settings.redis_dsn)

    def set_code(self, account_id: int, code: str, ttl_seconds: int) -> None:
        self.client.setex(f"code:{account_id}", ttl_seconds, code)

    def has_code(self, account_id: int) -> bool:
        # Исправлено: явное приведение к bool для типизации
        return bool(self.client.exists(f"code:{account_id}"))

    def clear(self) -> None:
        self.client.flushdb()


class AsyncRedisCodeRepository:
    def __init__(self, settings: Settings) -> None:
        self.client = async_redis.from_url(settings.redis_dsn)

    async def set_code(self, account_id: int, code: str, ttl_seconds: int) -> None:
        await self.client.setex(f"code:{account_id}", ttl_seconds, code)

    async def has_code(self, account_id: int) -> bool:
        # Исправлено: await результата перед сравнением
        res = await self.client.exists(f"code:{account_id}")
        return int(res) > 0

    async def clear(self) -> None:
        await self.client.flushdb()