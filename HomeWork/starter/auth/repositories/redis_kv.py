from __future__ import annotations
from auth.config import Settings
from auth.protocols import CodeRepositoryProtocol, AsyncCodeRepositoryProtocol


class RedisCodeRepository(CodeRepositoryProtocol):
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def set_code(self, account_id: int, code: str, ttl_seconds: int) -> None:
        super().set_code(account_id, code, ttl_seconds)

    def has_code(self, account_id: int) -> bool:
        return super().has_code(account_id)

    def clear(self) -> None:
        super().clear()


class AsyncRedisCodeRepository(AsyncCodeRepositoryProtocol):
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def set_code(self, account_id: int, code: str, ttl_seconds: int) -> None:
        await super().set_code(account_id, code, ttl_seconds)

    async def has_code(self, account_id: int) -> bool:
        return await super().has_code(account_id)

    async def clear(self) -> None:
        await super().clear()