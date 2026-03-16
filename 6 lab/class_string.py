from typing import Union


class Str:
    """
    Сравнение объектов этого класса происходит сначала по длине строки,
    а затем лексикографически.

    Attributes:
        value (str): Внутреннее строковое значение.
    """

    def __init__(self, value: str = "") -> None:
        """
        Инициализирует объект Str.

        Args:
            value: Строковое значение. По умолчанию "".
        """
        self.value = str(value)

    def __str__(self) -> str:
        """Возвращает строковое представление объекта."""
        return self.value

    def __repr__(self) -> str:
        """Возвращает официальное строковое представление объекта."""
        return f"Str('{self.value}')"

    def __len__(self) -> int:
        """Возвращает длину строки."""
        return len(self.value)

    # Операторы сравнения
    def __eq__(self, other: object) -> bool:
        """
        Проверяет равенство с другим объектом.

        Args:
            other: Объект для сравнения.

        Returns:
            True, если объекты равны по значению, иначе False.
        """
        if not isinstance(other, (str, Str)):
            return NotImplemented
        return self.value == str(other)

    def __lt__(self, other: Union[str, 'Str']) -> bool:
        """
        Проверяет, меньше ли текущий объект другого.

        Сравнение происходит сначала по длине, затем лексикографически.

        Args:
            other: Объект для сравнения.

        Returns:
            True, если текущий объект меньше другого, иначе False.
        """
        if not isinstance(other, (str, Str)):
            return NotImplemented

        other_value = str(other)

        # Сначала сравниваем по длине
        if len(self.value) != len(other_value):
            return len(self.value) < len(other_value)

        # Если длины равны, сравниваем лексикографически
        return self.value < other_value

    def __le__(self, other: Union[str, 'Str']) -> bool:
        """
        Проверяет, меньше или равен текущий объект другому.
        """
        return self < other or self == other

    def __gt__(self, other: Union[str, 'Str']) -> bool:
        """
        Проверяет, больше ли текущий объект другого.
        """
        if not isinstance(other, (str, Str)):
            return NotImplemented

        other_value = str(other)

        # Сначала сравниваем по длине
        if len(self.value) != len(other_value):
            return len(self.value) > len(other_value)

        # Если длины равны, сравниваем лексикографически
        return self.value > other_value

    def __ge__(self, other: Union[str, 'Str']) -> bool:
        """
        Проверяет, больше или равен текущий объект другому.
        """
        return self > other or self == other

    # Операторы для работы со строками
    def __add__(self, other: Union[str, 'Str']) -> 'Str':
        """
        Конкатенирует строки.

        Args:
            other: Другая строка или Str.

        Returns:
            Новый объект Str.
        """
        return Str(self.value + str(other))

    def __mul__(self, times: int) -> 'Str':
        """
        Повторяет строку указанное количество раз.

        Args:
            times: Количество повторений.

        Returns:
            Новый объект Str.
        """
        return Str(self.value * times)

    def __getitem__(self, index: Union[int, slice]) -> 'Str':
        """
        Возвращает символ или срез строки.

        Args:
            index: Индекс или срез.

        Returns:
            Новый объект Str.
        """
        return Str(self.value[index])

    def __contains__(self, item: str) -> bool:
        """
        Проверяет, содержится ли подстрока в строке.

        Args:
            item: Искомая подстрока.

        Returns:
            True, если подстрока найдена, иначе False.
        """
        return item in self.value

    # Делаем объект итерируемым
    def __iter__(self):
        """Возвращает итератор по символам строки."""
        return iter(self.value)

    # Дополнительные методы для работы со строками
    def upper(self) -> 'Str':
        """Возвращает строку в верхнем регистре."""
        return Str(self.value.upper())

    def lower(self) -> 'Str':
        """Возвращает строку в нижнем регистре."""
        return Str(self.value.lower())

    def strip(self, chars: str = None) -> 'Str':
        """Удаляет указанные символы в начале и конце строки."""
        return Str(self.value.strip(chars))

    def split(self, sep: str = None, maxsplit: int = -1) -> list:
        """Разбивает строку на список подстрок."""
        return self.value.split(sep, maxsplit)

    def startswith(self, prefix: str) -> bool:
        """Проверяет, начинается ли строка с указанного префикса."""
        return self.value.startswith(prefix)

    def endswith(self, suffix: str) -> bool:
        """Проверяет, заканчивается ли строка указанным суффиксом."""
        return self.value.endswith(suffix)


def main() -> None:
    print(f"ac > ab ? => {Str("ac") > Str("ab")}")
    print(f"ac < a ? => {Str("ac") < Str("a")}")
    print(f"ac > a ? => {Str("ac") > Str("a")}")
    print(f"ac < aba ? => {Str("ac") < Str("aba")}")
    print(f"ac > aba ? => {Str("ac") > Str("aba")}")
    print(f"ac.upper() = {Str("ac").upper()}")


if __name__ == "__main__":
    main()