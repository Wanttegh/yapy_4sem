import pytest
from bounded_counter import BoundedCounter


class TestBoundedCounter:
    """
    Класс для тестирования функциональности BoundedCounter.

    Методы класса проверяют инициализацию, нормальное поведение,
    граничные случаи, обработку исключений и работу операторов.
    """

    def test_initialization(self):
        """Проверка корректности инициализации конструктора."""
        # Стандартная инициализация
        bc = BoundedCounter(0, 10, 5)
        assert bc.get_value() == 5

        # Начальное значение на границах
        assert BoundedCounter(0, 10, 0).get_value() == 0
        assert BoundedCounter(0, 10, 10).get_value() == 10

    def test_initialization_exceptions(self):
        """Проверка исключений при некорректных параметрах конструктора."""
        # Случай min_value > max_value
        with pytest.raises(ValueError, match="min_value must be <= max_value"):
            BoundedCounter(10, 5)

        # Начальное значение выше максимума
        with pytest.raises(ValueError, match="initial_value out of bounds"):
            BoundedCounter(0, 10, 15)

        # Начальное значение ниже минимума
        with pytest.raises(ValueError, match="initial_value out of bounds"):
            BoundedCounter(5, 10, 2)

    def test_normal_behavior(self):
        """Проверка инкремента, декремента, установки и сброса."""
        bc = BoundedCounter(0, 10, 5)

        bc.increment(2)
        assert bc.get_value() == 7, "Ошибка при увеличении значения"

        bc.decrement(3)
        assert bc.get_value() == 4, "Ошибка при уменьшении значения"

        bc.set_value(8)
        assert bc.get_value() == 8, "Ошибка при установке значения"

        bc.reset()
        assert bc.get_value() == 5, "Ошибка при сбросе значения"

    def test_boundary_conditions(self):
        """Проверка поведения при достижении и попытке выхода за границы."""
        bc = BoundedCounter(0, 10, 10)

        # Попытка выйти за верхнюю границу
        with pytest.raises(ValueError, match="Increment would exceed upper bound"):
            bc.increment(1)

        bc.set_value(0)
        # Попытка выйти за нижнюю границу
        with pytest.raises(ValueError, match="Decrement would fall below lower bound"):
            bc.decrement(1)

        # Установка значения вне диапазона
        with pytest.raises(ValueError, match="Value out of bounds"):
            bc.set_value(11)

    def test_operators_addition(self):
        """Проверка оператора сложения (+)."""
        bc1 = BoundedCounter(0, 20, 10)
        bc2 = BoundedCounter(0, 20, 5)

        res = bc1 + bc2

        assert isinstance(res, BoundedCounter), "Результат должен быть объектом BoundedCounter"
        assert res.get_value() == 15, "Неверная сумма текущих значений"
        assert res._min == 0 and res._max == 20, "Новый объект должен наследовать границы первого"

        # Проверка неизменяемости исходных объектов
        assert bc1.get_value() == 10
        assert bc2.get_value() == 5

        # Проверка выхода суммы за границы
        bc_large = BoundedCounter(0, 20, 15)
        with pytest.raises(ValueError, match="Sum out of bounds"):
            _ = bc1 + bc_large

    def test_operators_subtraction(self):
        """Проверка оператора вычитания (-)."""
        bc1 = BoundedCounter(0, 20, 10)
        bc2 = BoundedCounter(0, 20, 4)

        res = bc1 - bc2

        assert res.get_value() == 6
        assert bc1.get_value() == 10, "Исходный объект не должен меняться"

        # Проверка выхода разности за нижнюю границу
        bc_small = BoundedCounter(0, 20, 15)
        with pytest.raises(ValueError, match="Difference out of bounds"):
            _ = bc1 - bc_small


def main():
    """Запуск тестов через pytest."""
    pytest.main([__file__])


if __name__ == "__main__":
    main()