from __future__ import annotations
import secrets
from auth.protocols import (
    AccountsRepositoryProtocol,
    AuditRepositoryProtocol,
    CodeRepositoryProtocol,
)

class AccountCardService:
    def __init__(
        self,
        accounts: AccountsRepositoryProtocol,
        audit: AuditRepositoryProtocol,
        codes: CodeRepositoryProtocol,
    ) -> None:
        self.accounts = accounts
        self.audit = audit
        self.codes = codes

    def create_account(self, email: str):
        account = self.accounts.create_account(email)
        # Так как account это объект класса Account, используем доступ через точку
        self.audit.log_event(account.id, "account_created", {"email": email})
        return account

    def set_verification_code(self, account_id: int, ttl_seconds: int = 300):
        code = secrets.token_hex(4).upper()
        self.codes.set_code(account_id, code, ttl_seconds)
        self.audit.log_event(account_id, "verification_code_set", {"ttl": ttl_seconds})
        return code

    def get_account_card(self, account_id: int):
        account = self.accounts.get_account(account_id)
        if not account:
            return None
        
        return {
            "account": account,
            "has_active_code": self.codes.has_code(account_id),
            "last_events": self.audit.list_events(account_id)
        }

    def reset(self) -> None:
        self.accounts.clear()
        self.audit.clear()
        self.codes.clear()