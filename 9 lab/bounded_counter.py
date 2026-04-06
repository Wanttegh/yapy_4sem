import doctest


class BoundedCounter:
    """
    Счётчик, значения которого не могут выходить за заданные границы.

    Параметры:
        min_value (int): минимальное допустимое значение (включительно).
        max_value (int): максимальное допустимое значение (включительно).
        initial_value (int, optional): начальное значение. Если не указано,
            устанавливается в min_value.

    Примеры использования (doctest):
    >>> bc = BoundedCounter(0, 10, 5)
    >>> bc.get_value()
    5
    >>> # Тест increment и границ
    >>> bc.increment(4)
    >>> bc.get_value()
    9
    >>> bc.increment(2)
    Traceback (most recent call last):
    ...
    ValueError: Increment would exceed upper bound

    >>> # Тест decrement и границ
    >>> bc.set_value(1)
    >>> bc.decrement(1)
    >>> bc.get_value()
    0
    >>> bc.decrement(1)
    Traceback (most recent call last):
    ...
    ValueError: Decrement would fall below lower bound

    >>> # Тест reset
    >>> bc.set_value(8)
    >>> bc.reset()
    >>> bc.get_value()
    5

    >>> # Тест операторов + и -
    >>> bc1 = BoundedCounter(0, 20, 10)
    >>> bc2 = BoundedCounter(0, 20, 5)
    >>> bc3 = bc1 + bc2
    >>> bc3.get_value()
    15
    >>> bc3._max == 20
    True
    >>> bc4 = bc1 - bc2
    >>> bc4.get_value()
    5
    >>> bc1 + BoundedCounter(0, 20, 15)
    Traceback (most recent call last):
    ...
    ValueError: Sum out of bounds

    >>> # Тест некорректной инициализации
    >>> BoundedCounter(10, 5)
    Traceback (most recent call last):
    ...
    ValueError: min_value must be <= max_value
    >>> BoundedCounter(0, 10, 15)
    Traceback (most recent call last):
    ...
    ValueError: initial_value out of bounds
    """

    def __init__(self, min_value: int, max_value: int, initial_value: int = 0):
        """Инициализирует счетчик с заданными границами и начальным значением."""
        if min_value > max_value:
            raise ValueError("min_value must be <= max_value")
        self._min = min_value
        self._max = max_value
        self._initial = initial_value if initial_value is not None else min_value
        if not (self._min <= self._initial <= self._max):
            raise ValueError("initial_value out of bounds")
        self._current = self._initial

    def increment(self, delta: int = 1) -> None:
        """Увеличивает текущее значение на delta."""
        new_value = self._current + delta
        if new_value > self._max:
            raise ValueError("Increment would exceed upper bound")
        self._current = new_value

    def decrement(self, delta: int = 1) -> None:
        """Уменьшает текущее значение на delta."""
        new_value = self._current - delta
        if new_value < self._min:
            raise ValueError("Decrement would fall below lower bound")
        self._current = new_value

    def set_value(self, value: int) -> None:
        """Устанавливает новое текущее значение."""
        if not (self._min <= value <= self._max):
            raise ValueError("Value out of bounds")
        self._current = value

    def reset(self) -> None:
        """Сбрасывает счётчик к начальному значению."""
        self._current = self._initial

    def get_value(self) -> int:
        """Возвращает текущее значение счётчика."""
        return self._current

    def __add__(self, other: 'BoundedCounter') -> 'BoundedCounter':
        """Создаёт новый счётчик как сумму текущих значений."""
        new_value = self._current + other._current
        if not (self._min <= new_value <= self._max):
            raise ValueError("Sum out of bounds")
        return BoundedCounter(self._min, self._max, new_value)

    def __sub__(self, other: 'BoundedCounter') -> 'BoundedCounter':
        """Создаёт новый счётчик как разность текущих значений."""
        new_value = self._current - other._current
        if not (self._min <= new_value <= self._max):
            raise ValueError("Difference out of bounds")
        return BoundedCounter(self._min, self._max, new_value)


def main():
    doctest.testmod(verbose=True)


if __name__ == "__main__":
    main()