from __future__ import annotations
import secrets
import string


from auth.models import Account, AccountCard
from auth.protocols import (
    PostgresAccountsRepository,
    MongoAuditRepository,
    RedisCodeRepository,
)


class AccountCardService:
    def __init__(
        self,
        accounts: PostgresAccountsRepository,
        audit: MongoAuditRepository,
        codes: RedisCodeRepository,
    ) -> None:
        self.accounts = accounts
        self.audit = audit
        self.codes = codes

    def create_account(self, email: str) -> Account:
        # 1. Создаем аккаунт в Postgres
        account = self.accounts.create_account(email)
        # 2. Логируем событие в Mongo
        self.audit.log_event(
            account_id=account.id, 
            event_type="account_created", 
            payload={"email": email}
        )
        return account

    def set_verification_code(self, account_id: int, ttl_seconds: int = 300) -> str:
        # Генерируем случайный 6-значный код
        code = ''.join(secrets.choice(string.digits) for _ in range(6))
        
        # 1. Сохраняем в Redis с TTL
        self.codes.set_code(account_id, code, ttl_seconds)
        
        # 2. Логируем событие в Mongo
        self.audit.log_event(
            account_id=account_id,
            event_type="verification_code_set",
            payload={"ttl": ttl_seconds}
        )
        return code

    def get_account_card(self, account_id: int) -> AccountCard:
        # 1. Получаем данные аккаунта
        account = self.accounts.get_account(account_id)
        if not account:
            raise ValueError(f"Account with id {account_id} not found")

        # 2. Проверяем код в Redis
        has_active_code = self.codes.has_code(account_id)

        # 3. Достаем последние события из Mongo
        events = self.audit.list_events(account_id, limit=5)

        return AccountCard(
            account=account,
            has_active_code=has_active_code,
            events=events
        )

    def reset(self) -> None:
        # Очищаем все хранилища
        self.accounts.clear()
        self.audit.clear()
        self.codes.clear()