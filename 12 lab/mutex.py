import time
import uuid
import redis
from concurrent.futures import ThreadPoolExecutor

class RedisLock:
    def __init__(self, redis_client, lock_name, expire=10, retry_delay=0.1):
        self.redis = redis_client
        self.lock_name = f"lock:{lock_name}"
        self.expire = expire
        self.retry_delay = retry_delay
        self.token = None

    def __enter__(self):
        # Генерируем уникальный токен для текущего захвата
        self.token = str(uuid.uuid4())
        while True:
            # Атомарная операция: установить если нет (NX) с временем жизни (EX)
            if self.redis.set(self.lock_name, self.token, nx=True, ex=self.expire):
                return self
            # Если не удалось захватить — ждем и пробуем снова
            time.sleep(self.retry_delay)

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Удаляем ключ только если токен совпадает (чтобы не удалить чужой лок)
        # Используем Lua-скрипт для атомарности "проверь и удали"
        script = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
        else
            return 0
        end
        """
        self.redis.eval(script, 1, self.lock_name, self.token)

# Инициализация клиента
# decode_responses=True преобразует байты из Redis в строки Python автоматически
r_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Инициализируем наш мьютекс
mu = RedisLock(r_client, "my_counter_lock")
result = 0

def function():
    global result
    with mu:  # Точка синхронизации
        # Читаем -> Ждем -> Пишем
        r = result
        time.sleep(0.1)  # Имитация долгой работы
        result = r + 1

def main():
    global result
    result = 0
    print("Запуск потоков...")
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(function) for _ in range(10)]
        for f in futures:
            f.result() # Ожидаем завершения всех потоков
            
    print(f"Итоговый результат: {result}") # Ожидаем 10

if __name__ == "__main__":
    try:
        main()
    except redis.exceptions.ConnectionError:
        print("Ошибка: Не удалось подключиться к Redis. Убедитесь, что сервер запущен.")