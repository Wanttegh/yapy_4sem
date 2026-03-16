from datetime import datetime
from time import sleep


def time_now(message, *, dt=None):
    """
    Выводит сообщение с временем в консоль.
    
    Args:
        message: Сообщение для вывода
        dt: Время для отображения (по умолчанию текущее)
    """
    if dt is None:
        dt = datetime.now()
    print(message, dt)


def main():
    print("Первый вызов:")
    time_now("Сейчас:")

    sleep(2)

    print("Второй вызов (через 2 секунды):")
    time_now("Сейчас:")  # Теперь время будет разным


if __name__ == '__main__':
    main()