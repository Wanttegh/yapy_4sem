import json
from datetime import datetime


def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def solve_tasks(raw_data):
    # Извлекаем список самих вакансий из поля 'data'
    vacancies = [item['data'] for item in raw_data if 'data' in item]

    # Вспомогательная функция для расчета годовой зарплаты (среднее между min и max)
    def get_annual_salary(v):
        s_min = v.get('salary_min_rub')
        s_max = v.get('salary_max_rub')
        if s_min and s_max:
            return (s_min + s_max) / 2
        return s_min or s_max or 0

    # 1. 10 самых новых вакансий
    # Сортируем по add_date (те, что null, отправляем в конец)
    newest = sorted(vacancies,
                    key=lambda x: x.get('add_date') or '',
                    reverse=True)[:10]

    # 2. 10 вакансий с максимальной годовой зарплатой
    # Приоритет отдаем salary_max_rub
    max_salary_vacs = sorted(vacancies,
                             key=lambda x: x.get('salary_max_rub') or x.get('salary_min_rub') or 0,
                             reverse=True)[:10]

    # 3. Средняя зарплата по всем вакансиям
    salaries = [get_annual_salary(v) for v in vacancies if get_annual_salary(v) > 0]
    avg_salary = sum(salaries) / len(salaries) if salaries else 0

    # 4. Все возможные типы занятости
    working_types = set()
    for v in vacancies:
        w_type = v.get('working_type')
        if w_type and w_type.get('title'):
            working_types.add(w_type['title'])

    # 5. Число вакансий для старта (без опыта) и средняя зарплата по ним
    # Обычно это "без опыта" или id, соответствующие началу карьеры
    start_vacs = [v for v in vacancies if v.get('experience_length', {}).get('title') == "нет опыта" or
                  v.get('experience_length', {}).get('id') == 3001]  # ID 3001 часто "без опыта"

    start_salaries = [get_annual_salary(v) for v in start_vacs if get_annual_salary(v) > 0]
    avg_start_salary = sum(start_salaries) / len(start_salaries) if start_salaries else 0

    # 6. Число вакансий с максимальным опытом и средняя зарплата
    # Обычно это "более 6 лет" или "6+ лет"
    max_exp_vacs = [v for v in vacancies if v.get('experience_length', {}).get('title') in ["более 6 лет", "6+ лет"] or
                    v.get('experience_length', {}).get('id') == 3004]  # ID 3004 часто "6+"

    max_exp_salaries = [get_annual_salary(v) for v in max_exp_vacs if get_annual_salary(v) > 0]
    avg_max_exp_salary = sum(max_exp_salaries) / len(max_exp_salaries) if max_exp_salaries else 0

    # Вывод результатов
    print("--- 10 САМЫХ НОВЫХ ВАКАНСИЙ ---")
    for i, v in enumerate(newest, 1):
        print(f"{i}. Дата: {v.get('add_date')} | Зарплата: {v.get('salary_formatted')}")

    print("\n--- 10 ВАКАНСИЙ С МАКСИМАЛЬНОЙ ГОДОВОЙ ЗАРПЛАТОЙ ---")
    for i, v in enumerate(max_salary_vacs, 1):
        print(f"{i}. Max RUB: {v.get('salary_max_rub')} | {v.get('salary_formatted')}")

    print(f"\nСРЕДНЯЯ ГОДОВАЯ ЗАРПЛАТА (по рынку): {avg_salary:,.2f} ₽")

    print(f"\nТИПЫ ЗАНЯТОСТИ: {', '.join(working_types)}")

    print(f"\nДЛЯ СТАРТА КАРЬЕРЫ:")
    print(f"Количество: {len(start_vacs)}")
    print(f"Средняя зарплата: {avg_start_salary:,.2f} ₽")

    print(f"\nДЛЯ МАКСИМАЛЬНОГО ОПЫТА:")
    print(f"Количество: {len(max_exp_vacs)}")
    print(f"Средняя зарплата: {avg_max_exp_salary:,.2f} ₽")


# Запуск
def main():
    data = load_data('vacs.json')
    solve_tasks(data)


if __name__ == "__main__":
    main()