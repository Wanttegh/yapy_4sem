from __future__ import annotations
import time
from typing import Protocol
from auth.models import Account, AuditEvent


class AccountsRepositoryProtocol(Protocol):
    _storage: dict[int, Account] = {}
    _id_counter: int = 1

    def create_account(self, email: str) -> Account:
        account = Account(id=self.__class__._id_counter, email=email)
        self.__class__._storage[account.id] = account
        self.__class__._id_counter += 1
        return account

    def get_account(self, account_id: int) -> Account | None:
        return self.__class__._storage.get(account_id)

    def clear(self) -> None:
        self.__class__._storage.clear()
        self.__class__._id_counter = 1


class AuditRepositoryProtocol(Protocol):
    _events: dict[int, list[AuditEvent]] = {}

    def log_event(self, account_id: int, event_type: str, payload: dict) -> None:
        if account_id not in self.__class__._events:
            self.__class__._events[account_id] = []
        event = AuditEvent(account_id=account_id, event_type=event_type, payload=payload)
        self.__class__._events[account_id].append(event)

    def list_events(self, account_id: int, limit: int = 5) -> list[AuditEvent]:
        all_events = self.__class__._events.get(account_id, [])
        return all_events[-limit:][::-1]

    def clear(self) -> None:
        self.__class__._events.clear()


class CodeRepositoryProtocol(Protocol):
    _codes: dict[int, tuple[str, float]] = {}

    def set_code(self, account_id: int, code: str, ttl_seconds: int) -> None:
        expiry = time.time() + ttl_seconds
        self.__class__._codes[account_id] = (code, expiry)

    def has_code(self, account_id: int) -> bool:
        if account_id not in self.__class__._codes:
            return False
        code, expiry = self.__class__._codes[account_id]
        if time.time() > expiry:
            del self.__class__._codes[account_id]
            return False
        return True

    def clear(self) -> None:
        self.__class__._codes.clear()


class AsyncAccountsRepositoryProtocol(Protocol):
    _storage: dict[int, Account] = {}
    _id_counter: int = 1

    async def create_account(self, email: str) -> Account:
        account = Account(id=self.__class__._id_counter, email=email)
        self.__class__._storage[account.id] = account
        self.__class__._id_counter += 1
        return account

    async def get_account(self, account_id: int) -> Account | None:
        return self.__class__._storage.get(account_id)

    async def clear(self) -> None:
        self.__class__._storage.clear()
        self.__class__._id_counter = 1


class AsyncAuditRepositoryProtocol(Protocol):
    _events: dict[int, list[AuditEvent]] = {}

    async def log_event(self, account_id: int, event_type: str, payload: dict) -> None:
        if account_id not in self.__class__._events:
            self.__class__._events[account_id] = []
        event = AuditEvent(account_id=account_id, event_type=event_type, payload=payload)
        self.__class__._events[account_id].append(event)

    async def list_events(self, account_id: int, limit: int = 5) -> list[AuditEvent]:
        all_events = self.__class__._events.get(account_id, [])
        return all_events[-limit:][::-1]

    async def clear(self) -> None:
        self.__class__._events.clear()


class AsyncCodeRepositoryProtocol(Protocol):
    _codes: dict[int, tuple[str, float]] = {}

    async def set_code(self, account_id: int, code: str, ttl_seconds: int) -> None:
        expiry = time.time() + ttl_seconds
        self.__class__._codes[account_id] = (code, expiry)

    async def has_code(self, account_id: int) -> bool:
        if account_id not in self.__class__._codes:
            return False
        _, expiry = self.__class__._codes[account_id]
        if time.time() > expiry:
            del self.__class__._codes[account_id]
            return False
        return True

    async def clear(self) -> None:
        self.__class__._codes.clear()