import asyncio
import aiohttp


class Composer:
    """Класс для агрегации данных, полученных от сервиса."""

    def __init__(self):
        """Инициализация аккумулятора результата."""
        self.result = 0
        self._lock = asyncio.Lock()

    async def add(self, data: dict):
        """
        Добавляет значение из словаря к общему результату.

        :param data: Словарь, содержащий ключ 'data'.
        """
        async with self._lock:
            self.result += data.get('data', 0)


async def fetch(
    session: aiohttp.ClientSession,
    url: str,
    param: int,
    composer: Composer,
    semaphore: asyncio.Semaphore
):
    """
    Выполняет асинхронный GET-запрос и передает данные в Composer.

    :param session: Сессия aiohttp для выполнения запросов.
    :param url: Базовый URL сервиса.
    :param param: Параметр запроса.
    :param composer: Экземпляр класса Composer для сбора данных.
    :param semaphore: Семафор для ограничения количества одновременных запросов.
    """
    async with semaphore:
        try:
            async with session.get(f'{url}/{param}') as response:
                if response.status == 200:
                    data = await response.json()
                    await composer.add(data)
                else:
                    # Можно добавить логирование ошибок сервера
                    pass
        except Exception as e:
            # Обработка сетевых ошибок
            print(f"Ошибка при запросе {param}: {e}")


async def collector(params: range) -> int:
    """
    Основная асинхронная функция для сбора данных по списку параметров.

    :param params: Список или диапазон параметров для запросов.
    :return: Итоговая сумма собранных данных.
    """
    url = 'http://localhost:8003'
    composer = Composer()
    # Ограничиваем количество одновременных соединений (например, 500),
    # чтобы не исчерпать ресурсы системы и не уронить сервер.
    semaphore = asyncio.Semaphore(500)

    # Используем ClientSession для повторного использования соединений (TCP Keep-Alive)
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch(session, url, i, composer, semaphore)
            for i in params
        ]
        # Запускаем все задачи конкурентно
        await asyncio.gather(*tasks)

    return composer.result


def main():
    # Входные параметры
    request_params = range(100_000)

    # Запуск асинхронного цикла
    final_result = asyncio.run(collector(request_params))
    print(f"Итоговый результат: {final_result}")


if __name__ == '__main__':
    main()