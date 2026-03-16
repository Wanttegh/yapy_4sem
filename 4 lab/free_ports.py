def free_ports(min_port, max_port, busy):
    """
    Находит все диапазоны свободных портов в заданном интервале.
    
    Args:
        min_port (int): Нижняя граница диапазона портов
        max_port (int): Верхняя граница диапазона портов
        busy (list): Список занятых портов
    
    Returns:
        list: Список диапазонов свободных портов в формате [[start, end], ...]
    """    
    if min_port > max_port:
        return []
    
    if not busy:
        return [[min_port, max_port]]
    
    # Сортируем занятые порты и фильтруем только те, что в нашем диапазоне
    busy_ports = sorted([p for p in busy if min_port <= p <= max_port])
    
    if not busy_ports:
        return [[min_port, max_port]]
    
    result = []
    current_start = min_port
    
    for port in busy_ports:
        if port > current_start:
            result.append([current_start, port - 1])
        current_start = port + 1
    
    # Добавляем последний диапазон, если остались порты
    if current_start <= max_port:
        result.append([current_start, max_port])
    
    return result


def print_free_ports(min_port, max_port, busy):
    """
    Выводит результат работы функции free_ports в удобочитаемом формате.
    
    Аргументы:
        min_port (int): Нижняя граница диапазона портов
        max_port (int): Верхняя граница диапазона портов
        busy (list): Список занятых портов
    """
    result = free_ports(min_port, max_port, busy)
    print(f"Диапазон: [{min_port}, {max_port}]")
    print(f"Занятые порты: {busy}")
    print(f"Свободные диапазоны: {result}\n")


def main():
    test_cases = [
        (30000, 32000, [30100, 30200]),
        (30100, 30200, [30100, 30200]),
        (30000, 32000, [100, 30100, 30200]),
        (30000, 32000, [32100]),
        (30000, 32000, []),
        (30000, 32000, [30000, 32000]),
    ]
    
    for min_p, max_p, busy_ports in test_cases:
        print_free_ports(min_p, max_p, busy_ports)


if __name__ == "__main__":
    main()