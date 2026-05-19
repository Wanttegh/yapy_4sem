from __future__ import annotations
import psycopg
import asyncpg
from auth.config import Settings

class PostgresAccountsRepository:
    def __init__(self, settings: Settings) -> None:
        self.dsn = settings.postgres_dsn

    def create_account(self, email: str):
        with psycopg.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO accounts (email) VALUES (%s) RETURNING id, email", (email,)
                )
                res = cur.fetchone()
                # Исправлено: проверка на None
                if res is None:
                    return None
                return {"id": res[0], "email": res[1]}

    def get_account(self, account_id: int):
        with psycopg.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, email FROM accounts WHERE id = %s", (account_id,))
                res = cur.fetchone()
                if res is None:
                    return None
                return {"id": res[0], "email": res[1]}

    def clear(self) -> None:
        with psycopg.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute("TRUNCATE TABLE accounts RESTART IDENTITY CASCADE")


class AsyncPostgresAccountsRepository:
    def __init__(self, settings: Settings) -> None:
        self.dsn = settings.postgres_dsn

    async def create_account(self, email: str):
        conn = await asyncpg.connect(self.dsn)
        try:
            row = await conn.fetchrow(
                "INSERT INTO accounts (email) VALUES ($1) RETURNING id, email", email
            )
            return dict(row) if row else None
        finally:
            await conn.close()

    async def get_account(self, account_id: int):
        conn = await asyncpg.connect(self.dsn)
        try:
            row = await conn.fetchrow("SELECT id, email FROM accounts WHERE id = $1", account_id)
            return dict(row) if row else None
        finally:
            await conn.close()

    async def clear(self) -> None:
        conn = await asyncpg.connect(self.dsn)
        try:
            await conn.execute("TRUNCATE TABLE accounts RESTART IDENTITY CASCADE")
        finally:
            await conn.close()