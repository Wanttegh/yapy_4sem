from __future__ import annotations
from typing import Protocol
from auth.models import Account, AuditEvent
import psycopg
import pymongo
import redis
import uuid


class AccountsRepositoryProtocol(Protocol):
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


class AuditRepositoryProtocol(Protocol):
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


class CodeRepositoryProtocol(Protocol):
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


class AsyncAccountsRepositoryProtocol(Protocol):
    async def create_account(self, email: str) -> Account:
        ...

    async def get_account(self, account_id: int) -> Account | None:
        ...

    async def clear(self) -> None:
        ...


class AsyncAuditRepositoryProtocol(Protocol):
    async def log_event(self, account_id: int, event_type: str, payload: dict) -> None:
        ...

    async def list_events(self, account_id: int, limit: int = 5) -> list[AuditEvent]:
        ...

    async def clear(self) -> None:
        ...


class AsyncCodeRepositoryProtocol(Protocol):
    async def set_code(self, account_id: int, code: str, ttl_seconds: int) -> None:
        ...

    async def has_code(self, account_id: int) -> bool:
        ...

    async def clear(self) -> None:
        ...
