import datetime
from typing import Tuple


def dmy(date: datetime.datetime) -> Tuple[int, int, int]:
    if not isinstance(date, datetime.datetime):
        raise TypeError("Аргумент должен быть объектом datetime.datetime")
    
    get_day = lambda dt: dt.day
    get_month = lambda dt: dt.month
    get_year = lambda dt: dt.year
    
    d, m, y = get_day(date), get_month(date), get_year(date)
    return d, m, y


def main() -> None:
    try:
        current_date = datetime.datetime.now()
        print(f"Текущая дата и время: {current_date}")
        
        day, month, year = dmy(current_date)
        
        print(f"День: {day}")
        print(f"Месяц: {month}")
        print(f"Год: {year}")
        
        print("\nПопытка передать аргумент неверного типа: не дата")
        dmy("не дата")
        
    except TypeError as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()