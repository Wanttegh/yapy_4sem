from __future__ import annotations
from typing import Protocol
from auth.models import Account, AuditEvent
import psycopg
import pymongo
import redis
import uuid
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from redis import asyncio as aioredis


class PostgresAccountsRepository(Protocol):
    def __init__(self, connection_string: str):
        # В реальном приложении лучше использовать пул соединений
        self.conn = psycopg.connect(connection_string)
        self._prepare_db()

    def _prepare_db(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS accounts (
                    id SERIAL PRIMARY KEY,
                    email TEXT UNIQUE NOT NULL
                )
            """)
            self.conn.commit()

    def create_account(self, email: str) -> Account:
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO accounts (email) VALUES (%s) RETURNING id, email",
                (email,)
            )
            row = cur.fetchone()
            self.conn.commit()
            return Account(id=row[0], email=row[1])

    def get_account(self, account_id: int) -> Account | None:
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, email FROM accounts WHERE id = %s", (account_id,))
            row = cur.fetchone()
            return Account(id=row[0], email=row[1]) if row else None

    def clear(self) -> None:
        with self.conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE accounts RESTART IDENTITY CASCADE")
            self.conn.commit()


class MongoAuditRepository(Protocol):
    def __init__(self, host: str, port: int, db_name: str):
        self.client = pymongo.MongoClient(host, port)
        self.db = self.client[db_name]
        self.collection = self.db["audit_events"]
    
    def log_event(self, account_id: int, event_type: str, payload: dict) -> None:
        self.collection.insert_one({
            "account_id": account_id,
            "event_type": event_type,
            "payload": payload
        })

    def list_events(self, account_id: int, limit: int = 5) -> list[AuditEvent]:
        cursor = self.collection.find({"account_id": account_id}).sort("_id", -1).limit(limit)
        return [
            AuditEvent(
                account_id=doc["account_id"],
                event_type=doc["event_type"],
                payload=doc["payload"]
            )
            for doc in cursor
        ]

    def clear(self) -> None:
        self.collection.delete_many({})


class RedisCodeRepository(Protocol):
    def __init__(self, host: str, port: int):
        self.client = redis.Redis(host=host, port=port, decode_responses=True)
    
    def _get_key(self, account_id: int) -> str:
        return f"verification_code:{account_id}"

    def set_code(self, account_id: int, code: str, ttl_seconds: int) -> None:
        self.client.setex(self._get_key(account_id), ttl_seconds, code)

    def has_code(self, account_id: int) -> bool:
        return self.client.exists(self._get_key(account_id)) > 0

    def clear(self) -> None:
        self.client.flushdb()


class AsyncPostgresAccountsRepository(Protocol):
    def __init__(self, settings):
        self.dsn = settings.pg_dsn
        self._conn = None

    async def _get_conn(self):
        if self._conn is None or self._conn.closed:
            self._conn = await psycopg.AsyncConnection.connect(self.dsn)
        return self._conn

    async def create_account(self, email: str) -> Account:
        conn = await self._get_conn()
        async with conn.cursor() as cur:
            await cur.execute(
                "INSERT INTO accounts (email) VALUES (%s) RETURNING id, email",
                (email,)
            )
            row = await cur.fetchone()
            await conn.commit()
            return Account(id=row[0], email=row[1])

    async def get_account(self, account_id: int) -> Account | None:
        conn = await self._get_conn()
        async with conn.cursor() as cur:
            await cur.execute("SELECT id, email FROM accounts WHERE id = %s", (account_id,))
            row = await cur.fetchone()
            return Account(id=row[0], email=row[1]) if row else None

    async def clear(self) -> None:
        conn = await self._get_conn()
        async with conn.cursor() as cur:
            await cur.execute("TRUNCATE TABLE accounts RESTART IDENTITY CASCADE")
            await conn.commit()


class AsyncMongoAuditRepository(Protocol):
    def __init__(self, settings):
        self.client = AsyncIOMotorClient(settings.mongo_host, settings.mongo_port)
        self.db = self.client[settings.mongo_db]
        self.collection = self.db["audit_events"]

    async def log_event(self, account_id: int, event_type: str, payload: dict) -> None:
        await self.collection.insert_one({
            "account_id": account_id,
            "event_type": event_type,
            "payload": payload
        })

    async def list_events(self, account_id: int, limit: int = 5) -> list[AuditEvent]:
        cursor = self.collection.find({"account_id": account_id}).sort("_id", -1).limit(limit)
        docs = await cursor.to_list(length=limit)
        return [
            AuditEvent(
                account_id=doc["account_id"],
                event_type=doc["event_type"],
                payload=doc["payload"]
            )
            for doc in docs
        ]

    async def clear(self) -> None:
        await self.collection.delete_many({})


class AsyncRedisCodeRepository(Protocol):
    def __init__(self, settings):
        self.redis = aioredis.Redis(
            host=settings.redis_host, 
            port=settings.redis_port, 
            decode_responses=True
        )

    def _get_key(self, account_id: int) -> str:
        return f"verification_code:{account_id}"

    async def set_code(self, account_id: int, code: str, ttl_seconds: int) -> None:
        await self.redis.setex(self._get_key(account_id), ttl_seconds, code)

    async def has_code(self, account_id: int) -> bool:
        return await self.redis.exists(self._get_key(account_id)) > 0

    async def clear(self) -> None:
        await self.redis.flushdb()