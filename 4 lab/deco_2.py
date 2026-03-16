from functools import wraps
import time


def n_dec(n):
    """
    Декоратор для определения времени работы функции при некотором количестве повторений

    Args:
        n: количество раз выполнения функции

    Returns:
        Декоратор, оборачивающий функцию
    """
    def wrapper(func):
        """
        Декоратор, оборачивающий функцию

        Args:
            func: декорируемая функция

        Returns:
            Обертка функции с вычисленным временем выполнения
        """
        @wraps(func)
        def wrapped(*args, **kwargs):
            """
            Обертка, выполняющая функцию подсчитывающая время работы функции

            Args:
                принимает все аргументы декорируемой функции

            Returns:
                результат работы исходной функции и время работы
            """
            start_time = time.time()
            result = 0
            for i in range (n):
                result += func(*args, **kwargs)
            end_time = time.time()

            execution_time = end_time - start_time
            print(f"Функция {func.__name__} выполнена за {execution_time:.6f} секунд, результат:")
            return result
        return wrapped
    return wrapper


@n_dec(n = 12339561)
def plus(a, b):
    return a + b


def main():
    print(plus(1325, 666))


if __name__ == '__main__':
    main()