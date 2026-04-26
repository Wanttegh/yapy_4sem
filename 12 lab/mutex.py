import time
import uuid
import fakeredis  # Имитация Redis
from concurrent.futures import ThreadPoolExecutor


class RedisLock:
    def __init__(self, redis_client, lock_name, expire=10, retry_delay=0.01):
        self.redis = redis_client
        self.lock_name = f"lock:{lock_name}"
        self.expire = expire
        self.retry_delay = retry_delay
        self.token = None

    def __enter__(self):
        self.token = str(uuid.uuid4())
        while True:
            # Пытаемся захватить лок
            # nx=True: установить только если ключа нет
            # ex=expire: время жизни ключа (защита от вечного лока)
            if self.redis.set(self.lock_name, self.token, nx=True, ex=self.expire):
                return self
            # Если занято — ждем немного и пробуем снова
            time.sleep(self.retry_delay)

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Безопасное удаление через Lua-скрипт.
        # Удаляем только если значение в Redis совпадает с нашим токеном.
        script = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
        else
            return 0
        end
        """
        self.redis.eval(script, 1, self.lock_name, self.token)


# Создаем клиент FakeRedis (он живет в памяти программы)
r_client = fakeredis.FakeRedis(decode_responses=True)
mu = RedisLock(r_client, "global_counter_lock")
result = 0


def function():
    global result
    # Контекстный менеджер вызывает __enter__ (захват) и __exit__ (освобождение)
    with mu:
        r = result
        # Имитируем долгую операцию (например, запрос к БД или вычисления)
        # Без мьютекса здесь бы возник Race Condition
        time.sleep(0.1)
        result = r + 1


def main():
    global result
    print("Запуск 10 потоков...")

    with ThreadPoolExecutor(max_workers=5) as executor:
        # Запускаем функцию 10 раз в разных потоках
        futures = [executor.submit(function) for _ in range(10)]
        # Ждем завершения всех
        for f in futures:
            f.result()

    print(f"Итоговый результат: {result}")


if __name__ == "__main__":
    main()