from __future__ import annotations
import asyncio
import secrets
import string


from auth.models import Account, AccountCard
from auth.protocols import (
    AsyncPostgresAccountsRepository,
    AsyncMongoAuditRepository,
    AsyncRedisCodeRepository,
)


class AsyncAccountCardService:
    def __init__(
        self,
        accounts: AsyncPostgresAccountsRepository,
        audit: AsyncMongoAuditRepository,
        codes: AsyncRedisCodeRepository,
    ) -> None:
        self.accounts = accounts
        self.audit = audit
        self.codes = codes

    async def create_account(self, email: str) -> Account:
        account = await self.accounts.create_account(email)
        await self.audit.log_event(
            account_id=account.id,
            event_type="account_created",
            payload={"email": email}
        )
        return account

    async def set_verification_code(self, account_id: int, ttl_seconds: int = 300) -> str:
        code = ''.join(secrets.choice(string.digits) for _ in range(6))
        
        # Выполняем параллельно сохранение кода и запись лога
        await asyncio.gather(
            self.codes.set_code(account_id, code, ttl_seconds),
            self.audit.log_event(
                account_id=account_id,
                event_type="verification_code_set",
                payload={"ttl": ttl_seconds}
            )
        )
        return code

    async def get_account_card(self, account_id: int) -> AccountCard:
        # Сначала получаем аккаунт, так как если его нет, остальное не имеет смысла
        account = await self.accounts.get_account(account_id)
        if not account:
            raise ValueError(f"Account {account_id} not found")

        # Получаем данные из Redis и Mongo параллельно
        has_code_task = self.codes.has_code(account_id)
        events_task = self.audit.list_events(account_id, limit=5)

        has_active_code, events = await asyncio.gather(has_code_task, events_task)

        return AccountCard(
            account=account,
            has_active_code=has_active_code,
            events=events
        )

    async def reset(self) -> None:
        await asyncio.gather(
            self.accounts.clear(),
            self.audit.clear(),
            self.codes.clear()
        )