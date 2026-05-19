from __future__ import annotations
from auth.config import Settings
from auth.models import AuditEvent
from auth.protocols import AuditRepositoryProtocol, AsyncAuditRepositoryProtocol


class MongoAuditRepository(AuditRepositoryProtocol):
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def log_event(self, account_id: int, event_type: str, payload: dict) -> None:
        super().log_event(account_id, event_type, payload)

    def list_events(self, account_id: int, limit: int = 5) -> list[AuditEvent]:
        return super().list_events(account_id, limit)

    def clear(self) -> None:
        super().clear()


class AsyncMongoAuditRepository(AsyncAuditRepositoryProtocol):
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def log_event(self, account_id: int, event_type: str, payload: dict) -> None:
        await super().log_event(account_id, event_type, payload)

    async def list_events(self, account_id: int, limit: int = 5) -> list[AuditEvent]:
        return await super().list_events(account_id, limit)

    async def clear(self) -> None:
        await super().clear()