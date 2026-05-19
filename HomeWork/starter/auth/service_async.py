from __future__ import annotations
import secrets
import asyncio
from auth.protocols import (
    AsyncAccountsRepositoryProtocol,
    AsyncAuditRepositoryProtocol,
    AsyncCodeRepositoryProtocol,
)

class AsyncAccountCardService:
    def __init__(
        self,
        accounts: AsyncAccountsRepositoryProtocol,
        audit: AsyncAuditRepositoryProtocol,
        codes: AsyncCodeRepositoryProtocol,
    ) -> None:
        self.accounts = accounts
        self.audit = audit
        self.codes = codes

    async def create_account(self, email: str):
        account = await self.accounts.create_account(email)
        # Обращаемся к id напрямую через точку
        await self.audit.log_event(account.id, "account_created", {"email": email})
        return account

    async def set_verification_code(self, account_id: int, ttl_seconds: int = 300):
        code = secrets.token_hex(4).upper()
        await self.codes.set_code(account_id, code, ttl_seconds)
        await self.audit.log_event(account_id, "verification_code_set", {"ttl": ttl_seconds})
        return code

    async def get_account_card(self, account_id: int):
        # asyncio.gather возвращает кортеж с результатами
        account, has_code, events = await asyncio.gather(
            self.accounts.get_account(account_id),
            self.codes.has_code(account_id),
            self.audit.list_events(account_id)
        )
        
        if not account:
            return None

        return {
            "account": account,
            "has_active_code": has_code,
            "last_events": events
        }

    async def reset(self) -> None:
        await asyncio.gather(
            self.accounts.clear(),
            self.audit.clear(),
            self.codes.clear()
        )