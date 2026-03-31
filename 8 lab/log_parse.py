import re
from collections import Counter, defaultdict
from typing import List, Tuple


def analyze_logs(file_path: str):
    """
    Проводит анализ лог-файла nginx.

    Выводит 10 самых популярных User-Agent и 10 IP-адресов
    с пиковым потреблением трафика в сутки.
    """
    # Регулярное выражение для извлечения IP, Даты, Размера ответа и User-Agent
    # Формат: ip - - [date:time] "request" status size "referer" "user_agent"
    log_pattern = re.compile(
        r'(?P<ip>\S+)\s+\S+\s+\S+\s+\[(?P<date>\d{2}/\w{3}/\d{4}):.*?\]\s+'
        r'".*?"\s+\d{3}\s+(?P<size>\d+)\s+".*?"\s+"(?P<ua>.*?)"'
    )

    ua_counter = Counter()
    # Структура: traffic_stats[ip][date] = total_bytes
    traffic_stats = defaultdict(lambda: defaultdict(int))

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                match = log_pattern.match(line)
                if not match:
                    continue

                ip = match.group('ip')
                date = match.group('date')
                try:
                    size = int(match.group('size'))
                except ValueError:
                    size = 0
                ua = match.group('ua')

                # Считаем User-Agent
                ua_counter[ua] += 1

                # Считаем трафик для IP по конкретным суткам
                traffic_stats[ip][date] += size

    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден.")
        return

    # 1. Топ-10 User-Agent
    top_uas = ua_counter.most_common(10)

    # 2. Топ-10 IP по пиковому трафику в сутки
    # Для каждого IP находим день с максимальным трафиком
    ip_peaks = []
    for ip, dates in traffic_stats.items():
        max_daily_traffic = max(dates.values())
        ip_peaks.append((ip, max_daily_traffic))

    # Сортируем IP по значению их пикового трафика
    top_ips = sorted(ip_peaks, key=lambda x: x[1], reverse=True)[:10]

    _print_results(top_uas, top_ips)


def _print_results(top_uas: List[Tuple[str, int]], 
                   top_ips: List[Tuple[str, int]]):
    """Вспомогательный метод для вывода результатов."""
    print("--- Топ-10 User-Agent по количеству запросов ---")
    for i, (ua, count) in enumerate(top_uas, 1):
        print(f"{i}. {count} запросов | {ua}")

    print("\n--- Топ-10 IP по пиковому трафику в сутки ---")
    for i, (ip, traffic) in enumerate(top_ips, 1):
        # Переводим в MiB для читаемости (по желанию)
        traffic_mib = traffic / (1024 * 1024)
        print(f"{i}. {ip} | Пик: {traffic_mib:.2f} MiB")


if __name__ == "__main__":
    # Путь к файлу лога
    analyze_logs('C:\\Users\\howard\\Desktop\\yapy_4sem\\8 lab\\access_log.txt')