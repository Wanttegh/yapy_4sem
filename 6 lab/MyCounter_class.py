from collections import Counter
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union


class MyCounter(Counter):
    """
    Расширенная версия класса Counter с методом least_common.

    Класс наследует все возможности Counter и добавляет метод
    для получения самых редких элементов.

    """

    def least_common(self, n: Optional[int] = None) -> List[Tuple[Any, int]]:
        """
        Возвращает n самых редких элементов.

        Элементы сортируются от самых редких к самым частым.
        При одинаковой частоте порядок не гарантируется.

        Args:
            n: Количество возвращаемых элементов.
               Если None, возвращаются все элементы.

        Returns:
            Список кортежей (элемент, частота) в порядке возрастания частоты.

        """
        # Получаем все элементы с их частотами
        items = list(self.items())

        # Сортируем по частоте (по возрастанию)
        # При одинаковой частоте сортируем по элементу для детерминированности
        sorted_items = sorted(items, key=lambda x: (x[1], x[0]))

        # Если n не указано, возвращаем все элементы
        if n is None:
            return sorted_items

        # Иначе возвращаем первые n элементов
        return sorted_items[:n]

    def __repr__(self) -> str:
        """Возвращает строковое представление объекта."""
        return f"MyCounter({dict(self)})"


def main() -> None:
    # Пример 1: Подсчёт символов в строке
    text = "abracadabra"
    counter = MyCounter(text)

    print(f"1. Подсчёт символов в строке '{text}':")
    print(f"   {counter}")
    print()

    # Пример 2: least_common (новый метод)
    print("2. Самые редкие символы (least_common):")
    print(f"   Все: {counter.least_common()}")
    print(f"   Топ-3: {counter.least_common(3)}")
    print(f"   Топ-2: {counter.least_common(2)}")
    print()

    # Пример 3: Работа с пустым счётчиком
    empty_counter = MyCounter()
    print("3. Пустой счётчик:")
    print(f"   least_common: {empty_counter.least_common()}")
    print(f"   most_common: {empty_counter.most_common()}")
    print()


if __name__ == "__main__":
    main()