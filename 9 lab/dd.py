import pytest
from bounded_counter import BoundedCounter


def test_initialization():
    """Проверка корректной инициализации счетчика."""
    # Обычная инициализация
    bc = BoundedCounter(0, 10, 5)
    assert bc.get_value() == 5

    # Инициализация без начального значения (должно быть min_value)
    bc_default = BoundedCounter(1, 10)
    assert bc_default.get_value() == 1

    # Инициализация на границах
    bc_min = BoundedCounter(0, 10, 0)
    assert bc_min.get_value() == 0
    bc_max = BoundedCounter(0, 10, 10)
    assert bc_max.get_value() == 10


def test_initialization_errors():
    """Проверка обработки исключений при создании объекта."""
    # min > max
    with pytest.raises(ValueError, match="min_value must be <= max_value"):
        BoundedCounter(10, 5)

    # initial_value > max
    with pytest.raises(ValueError, match="initial_value out of bounds"):
        BoundedCounter(0, 10, 11)

    # initial_value < min
    with pytest.raises(ValueError, match="initial_value out of bounds"):
        BoundedCounter(5, 10, 4)


def test_normal_behavior():
    """Проверка инкремента, декремента, установки и сброса."""
    bc = BoundedCounter(0, 10, 5)

    bc.increment(2)
    assert bc.get_value() == 7

    bc.decrement(3)
    assert bc.get_value() == 4

    bc.set_value(9)
    assert bc.get_value() == 9

    bc.reset()
    assert bc.get_value() == 5


def test_boundary_conditions():
    """Проверка поведения на границах допустимого диапазона."""
    bc = BoundedCounter(0, 10, 5)

    # Достижение верхней границы
    bc.set_value(10)
    with pytest.raises(ValueError, match="Increment would exceed upper bound"):
        bc.increment(1)

    # Достижение нижней границы
    bc.set_value(0)
    with pytest.raises(ValueError, match="Decrement would fall below lower bound"):
        bc.decrement(1)

    # Попытка установки значения за границами
    with pytest.raises(ValueError, match="Value out of bounds"):
        bc.set_value(11)


def test_operators():
    """Проверка работы магических методов __add__ и __sub__."""
    bc1 = BoundedCounter(0, 100, 30)
    bc2 = BoundedCounter(0, 50, 20)

    # Проверка сложения
    res_add = bc1 + bc2
    assert isinstance(res_add, BoundedCounter)
    assert res_add.get_value() == 50
    assert res_add._min == 0
    assert res_add._max == 100

    # Проверка вычитания
    res_sub = bc1 - bc2
    assert res_sub.get_value() == 10

    # Проверка неизменяемости исходных объектов
    assert bc1.get_value() == 30
    assert bc2.get_value() == 20

    # Выход за границы при сложении
    bc_large = BoundedCounter(0, 100, 80)
    with pytest.raises(ValueError, match="Sum out of bounds"):
        _ = bc1 + bc_large

    # Выход за границы при вычитании
    with pytest.raises(ValueError, match="Difference out of bounds"):
        _ = bc2 - bc1


def main():
    """Запуск pytest для данного модуля."""
    pytest.main([__file__])


if __name__ == "__main__":
    main()