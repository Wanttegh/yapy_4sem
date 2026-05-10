import asyncio

from auth import AsyncAccountCardService, Settings
from auth.repositories import (
    AsyncMongoAuditRepository,
    AsyncPostgresAccountsRepository,
    AsyncRedisCodeRepository,
)


async def main() -> None:
    settings = Settings.from_env()
    service = AsyncAccountCardService(
        accounts=AsyncPostgresAccountsRepository(settings),
        audit=AsyncMongoAuditRepository(settings),
        codes=AsyncRedisCodeRepository(settings),
    )

    # Начальная очистка
    await service.reset()
    
    try:
        # 1. Создаем два аккаунта параллельно
        # Используем asyncio.gather для одновременного запуска задач
        first, second = await asyncio.gather(
            service.create_account("first@example.com"),
            service.create_account("second@example.com")
        )

        # 2. Устанавливаем проверочные коды параллельно
        await asyncio.gather(
            service.set_verification_code(first.id, ttl_seconds=60),
            service.set_verification_code(second.id, ttl_seconds=60)
        )

        # 3. Собираем карточки аккаунтов параллельно
        # Каждый вызов внутри себя также делает конкурентные запросы к PG/Mongo/Redis
        first_card, second_card = await asyncio.gather(
            service.get_account_card(first.id),
            service.get_account_card(second.id)
        )
        
        # Проверки
        assert first_card.has_active_code is True
        assert second_card.has_active_code is True
        
        # Можно также проверить, что емейлы соответствуют
        assert first_card.account.email == "first@example.com"
        assert second_card.account.email == "second@example.com"
        
        print("async scenario is OK (tasks executed in parallel)")
    finally:
        # Очистка в любом случае (успех или ошибка)
        await service.reset()


if __name__ == "__main__":
    asyncio.run(main())