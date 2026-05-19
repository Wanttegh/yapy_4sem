from __future__ import annotations
from auth.config import Settings
from auth.models import Account
from auth.protocols import AccountsRepositoryProtocol, AsyncAccountsRepositoryProtocol


class PostgresAccountsRepository(AccountsRepositoryProtocol):
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def create_account(self, email: str) -> Account:
        return super().create_account(email)

    def get_account(self, account_id: int) -> Account | None:
        return super().get_account(account_id)

    def clear(self) -> None:
        super().clear()


class AsyncPostgresAccountsRepository(AsyncAccountsRepositoryProtocol):
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def create_account(self, email: str) -> Account:
        return await super().create_account(email)

    async def get_account(self, account_id: int) -> Account | None:
        return await super().get_account(account_id)

    async def clear(self) -> None:
        await super().clear()