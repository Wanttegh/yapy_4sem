from __future__ import annotations
import pymongo
from motor.motor_asyncio import AsyncIOMotorClient
from auth.config import Settings

class MongoAuditRepository:
    def __init__(self, settings: Settings) -> None:
        # Исправлено: используем mongo_dsn (проверьте имя в вашем Settings)
        self.client = pymongo.MongoClient(settings.mongo_dsn)
        self.db = self.client.get_database("audit_db")
        self.collection = self.db.get_collection("events")

    def log_event(self, account_id: int, event_type: str, payload: dict) -> None:
        self.collection.insert_one({
            "account_id": account_id,
            "event_type": event_type,
            "payload": payload
        })

    def list_events(self, account_id: int, limit: int = 5):
        cursor = self.collection.find({"account_id": account_id}).sort("_id", -1).limit(limit)
        return [{"event_type": e["event_type"], "payload": e["payload"]} for e in cursor]

    def clear(self) -> None:
        self.collection.delete_many({})


class AsyncMongoAuditRepository:
    def __init__(self, settings: Settings) -> None:
        self.client = AsyncIOMotorClient(settings.mongo_dsn)
        self.db = self.client.get_database("audit_db")
        self.collection = self.db.get_collection("events")

    async def log_event(self, account_id: int, event_type: str, payload: dict) -> None:
        await self.collection.insert_one({
            "account_id": account_id,
            "event_type": event_type,
            "payload": payload
        })

    async def list_events(self, account_id: int, limit: int = 5):
        cursor = self.collection.find({"account_id": account_id}).sort("_id", -1).limit(limit)
        events = await cursor.to_list(length=limit)
        return [{"event_type": e["event_type"], "payload": e["payload"]} for e in events]

    async def clear(self) -> None:
        await self.collection.delete_many({})