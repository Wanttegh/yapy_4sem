"""Скрипт для демонстрации работы BoundedCounter и профилирования."""

from bounded_counter import BoundedCounter


def heavy_computation():
    """Выполняет ресурсоемкие операции со счетчиками."""
    # Создаем много объектов и выполняем операции в цикле
    main_counter = BoundedCounter(0, 1000000, 0)

    for i in range(100000):
        # Инкремент
        main_counter.increment(1)

        # Создание временных объектов через операторы
        temp_counter = BoundedCounter(0, 1000000, i % 10)
        main_counter = main_counter + temp_counter

        # Сброс каждые 1000 итераций, чтобы не выйти за границы
        if main_counter.get_value() > 900000:
            main_counter.reset()


def main():
    """Точка входа в скрипт."""
    print("Starting computation...")
    heavy_computation()
    print("Finished.")


if __name__ == "__main__":
    main()