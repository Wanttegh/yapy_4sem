from functools import wraps


def unexcept(default_value):
    """
    Декоратор для перехвата исключений в декорируемой функции.
    
    Args:
        default_value: Значение, которое будет возвращено при возникновении любого исключения
    
    Returns:
        Декоратор, оборачивающий функцию
    """
    def wrapper(func):
        """
        Внутренний декоратор, который оборачивает функцию.
        
        Args:
            func: Декорируемая функция
        
        Returns:
            Обертка функции с обработкой исключений
        """
        @wraps(func)
        def wrapped(*args, **kwargs):
            """
            Обертка, выполняющая функцию и перехватывающая исключения.
            
            Returns:
                Результат функции или default_value при исключении
            """
            try:
                return func(*args, **kwargs)
            except Exception:
                return default_value
        return wrapped
    return wrapper


@unexcept(default_value="Ошибка: деление на ноль!")
def div(a, b):
    """Деление двух чисел."""
    return a / b


@unexcept(default_value="Ошибка типов: один или несколько аргументов не являются объектами числовых типов!")
def plus(a, b):
    """Сложение двух чисел."""
    return a + b


def main():
    print("div")
    print(f"div(10, 2) = {div(10, 2)}")        # 5.0
    print(f"div(10, 0) = {div(10, 0)}\n")        # -1 (деление на ноль)

    print("plus")
    print(f"plus(5, 3) = {plus(5, 3)}")        # 8
    print(f"plus('5', 3) = {plus('5', 3)}")    # 1000 (ошибка типов)


if __name__ == '__main__':
    main()