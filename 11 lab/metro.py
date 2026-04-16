import requests


def get_country_mapping():
    """
    Получает дерево регионов и создает словарь: {id_региона: название_страны}
    """
    response = requests.get("https://api.hh.ru/areas")
    response.raise_for_status()
    areas = response.json()

    id_to_country = {}

    for country in areas:
        country_name = country['name']

        # Рекурсивная функция для обхода дерева регионов
        def map_ids(node, name):
            id_to_country[node['id']] = name
            for sub_area in node.get('areas', []):
                map_ids(sub_area, name)

        map_ids(country, country_name)

    return id_to_country


def count_metro_stations():
    """
    Получает данные о метро и суммирует станции по странам
    """
    # 1. Получаем маппинг ID -> Страна
    try:
        country_map = get_country_mapping()
    except Exception as e:
        return f"Ошибка при получении данных о регионах: {e}"

    # 2. Получаем данные о метро
    try:
        response = requests.get("https://api.hh.ru/metro")
        response.raise_for_status()
        metro_data = response.json()
    except Exception as e:
        return f"Ошибка при получении данных о метро: {e}"

    stats = {}

    # 3. Анализируем данные метро
    for city in metro_data:
        city_id = city['id']
        country_name = country_map.get(city_id, "Неизвестно")

        # Считаем станции во всех линиях города
        station_count = 0
        for line in city.get('lines', []):
            station_count += len(line.get('stations', []))

        # Группируем по странам
        if country_name in stats:
            stats[country_name] += station_count
        else:
            stats[country_name] = station_count

    return stats


def main():
    print("Загрузка данных и расчет станций метро...\n")
    results = count_metro_stations()

    if isinstance(results, dict):
        # Сортировка результатов по количеству станций (от большего к меньшему)
        sorted_results = sorted(results.items(), key=lambda item: item[1], reverse=True)

        print(f"{'Страна':<20} | {'Количество станций':<10}")
        print("-" * 40)
        for country, count in sorted_results:
            print(f"{country:<20} | {count:<10}")
    else:
        print(results)


if __name__ == "__main__":
    main()