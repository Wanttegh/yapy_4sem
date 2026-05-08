"""Модуль клиента для взаимодействия с сервером хешей."""

import asyncio
import aiohttp


async def fetch_algorithms(session: aiohttp.ClientSession,
                           hash_value: str) -> list:
    """
    Получает список алгоритмов для хеша с сервера.

    session: Сессия aiohttp.
    hash_value: Строка хеша.
    return: Список строк (алгоритмов).
    """
    url = f'http://127.0.0.1:8080/define/{hash_value}'
    async with session.get(url) as response:
        return await response.json()


async def solve_hash(session: aiohttp.ClientSession,
                     hash_value: str, algorithm: str) -> dict:
    """
    Отправляет запрос на решение хеша по конкретному алгоритму.

    session: Сессия aiohttp.
    hash_value: Строка хеша.
    algorithm: Название алгоритма.
    return: Словарь с результатом.
    """
    url = 'http://127.0.0.1:8080/solve'
    params = {'hash': hash_value, 'algorithm': algorithm}
    async with session.get(url, params=params) as response:
        return await response.json()


async def main():
    """Основная логика работы клиента."""
    target_hash = 'c4ca4238a0b923820dcc509a6f75849b'

    async with aiohttp.ClientSession() as session:
        print(f"Идентификация хеша: {target_hash}")
        algorithms = await fetch_algorithms(session, target_hash)

        if not algorithms:
            print("Алгоритмы не найдены.")
            return

        print(f"Найденные алгоритмы: {', '.join(algorithms)}")
        print("Запуск вычислений для каждого алгоритма...")

        # Создаем список задач для конкурентного выполнения
        tasks = [
            solve_hash(session, target_hash, alg)
            for alg in algorithms
        ]

        # Ожидаем завершения всех задач
        results = await asyncio.gather(*tasks)

        for res in results:
            print(f"Результат: {res.get('result')}")


if __name__ == '__main__':
    asyncio.run(main())