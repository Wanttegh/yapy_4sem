class Counter:
    """
    Класс, реализующий положительный целочисленный счетчик.

    Счетчик работает в заданном диапазоне [min_value, max_value].
    По умолчанию нижняя граница равна 0.
    """
    def __init__(self, start_value=0, max_boundary=100):
        """
        Инициализирует счетчик.

        start_value: Начальное значение.
        max_boundary: Верхняя граница диапазона.
        """
        self._min_value = 0
        self._max_value = max_boundary
        self._initial_value = start_value

        if not (self._min_value <= start_value <= self._max_value):
            raise ValueError(f"Стартовое значение должно быть в "
                             f"диапазоне [{self._min_value}, {self._max_value}]")
        
        self._current_value = start_value

    def set_value(self, value):
        """
        Устанавливает произвольное значение счетчика в пределах диапазона.

        value: Новое значение.
        """
        if self._min_value <= value <= self._max_value:
            self._current_value = value
        else:
            raise ValueError(f"Значение {value} вне диапазона "
                             f"[{self._min_value}, {self._max_value}]")

    def increment(self, step=1):
        """
        Увеличивает текущее значение счетчика на заданный шаг.

        step: Шаг увеличения (по умолчанию 1).
        """
        new_value = self._current_value + step
        if new_value <= self._max_value:
            self._current_value = new_value
        else:
            raise ValueError("Превышена верхняя граница счетчика")

    def decrement(self, step=1):
        """
        Уменьшает текущее значение счетчика на заданный шаг.

        step: Шаг уменьшения (по умолчанию 1).
        """
        new_value = self._current_value - step
        if new_value >= self._min_value:
            self._current_value = new_value
        else:
            raise ValueError("Превышена нижняя граница счетчика")

    def get_value(self):
        """Возвращает текущее значение счетчика."""
        return self._current_value

    def reset(self):
        """Сбрасывает текущее значение к начальному значению."""
        self._current_value = self._initial_value

    def __add__(self, other):
        """
        Складывает два экземпляра Counter.

        Результатом является новый Counter, чье значение и верхняя граница
        являются суммами соответствующих значений слагаемых.
        """
        if not isinstance(other, Counter):
            return NotImplemented
        
        new_start = self._current_value + other._current_value
        new_max = self._max_value + other._max_value
        return Counter(start_value=new_start, max_boundary=new_max)

    def __str__(self):
        """Строковое представление объекта."""
        return (f"Counter(current={self._current_value}, "
                f"range=[{self._min_value}, {self._max_value}])")


def main():
    """Основная функция для демонстрации работы класса Counter."""
    print("--- Инициализация счетчика ---")
    # Создание экземпляра со значениями по умолчанию (0 и 100)
    # Но для теста цикла в рамках вывода ограничим диапазон 10
    c1 = Counter(start_value=0, max_boundary=10)
    print(f"Начальные параметры: {c1}")

    print("\n--- Проверка цикла (от 0 до максимума) ---")
    try:
        while True:
            print(f"Текущее значение: {c1.get_value()}")
            c1.increment()
    except ValueError as e:
        print(f"Цикл завершен. Сообщение: {e}")

    print("\n--- Тестирование методов ---")
    
    # Метод сброса
    c1.reset()
    print(f"После reset(): {c1.get_value()}")

    # Установка произвольного значения
    c1.set_value(5)
    print(f"После set_value(5): {c1.get_value()}")

    # Уменьшение
    c1.decrement(2)
    print(f"После decrement(2): {c1.get_value()}")

    # Проверка ошибки диапазона
    print("Попытка установить значение 100 при максимуме 10:")
    try:
        c1.set_value(100)
    except ValueError as e:
        print(f"Ошибка поймана: {e}")

    print("\n--- Сложение двух счетчиков ---")
    cnt1 = Counter(3, 20)
    cnt2 = Counter(7, 30)
    cnt_sum = cnt1 + cnt2
    print(f"Счетчик 1: {cnt1}")
    print(f"Счетчик 2: {cnt2}")
    print(f"Результат сложения: {cnt_sum}")


if __name__ == "__main__":
    main()