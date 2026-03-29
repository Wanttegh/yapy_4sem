import math
from typing import Union


class Rectangle:
    """Класс, представляющий прямоугольник."""

    def __init__(self, a: float, b: float) -> None:
        """
        Инициализирует прямоугольник со сторонами a и b.

        a: Сторона A.
        b: Сторона B.
        """
        self.a = a
        self.b = b

    def get_perimeter(self) -> float:
        """Возвращает периметр прямоугольника."""
        return 2 * (self.a + self.b)

    def get_square(self) -> float:
        """Возвращает площадь прямоугольника."""
        return self.a * self.b


class Circle:
    """Класс, представляющий круг."""

    def __init__(self, r: float) -> None:
        """
        Инициализирует круг радиусом r.

        r: Радиус круга.
        """
        self.r = r

    def get_perimeter(self) -> float:
        """Возвращает длину окружности (периметр)."""
        return 2 * math.pi * self.r

    def get_square(self) -> float:
        """Возвращает площадь круга."""
        return math.pi * (self.r ** 2)


class Rhombus:
    """Класс, представляющий ромб."""

    def __init__(self, p: float, q: float) -> None:
        """
        Инициализирует ромб его диагоналями p и q.

        p: Первая диагональ.
        q: Вторая диагональ.
        """
        self.p = p
        self.q = q

    def get_perimeter(self) -> float:
        """
        Возвращает периметр ромба.

        Сторона ромба вычисляется через диагонали по теореме Пифагора.
        """
        side = math.sqrt((self.p / 2) ** 2 + (self.q / 2) ** 2)
        return 4 * side

    def get_square(self) -> float:
        """Возвращает площадь ромба через его диагонали."""
        return (self.p * self.q) / 2


# Создаем тип-псевдоним для аннотации функций
Figure = Union[Rectangle, Circle, Rhombus]


def calculate_perimeter(figure: Figure) -> float:
    """
    Вычисляет и возвращает периметр переданной фигуры.

    figure: Экземпляр фигуры (Rectangle, Circle или Rhombus).
    :return: Значение периметра.
    """
    return figure.get_perimeter()


def calculate_square(figure: Figure) -> float:
    """
    Вычисляет и возвращает площадь переданной фигуры.

    figure: Экземпляр фигуры (Rectangle, Circle или Rhombus).
    :return: Значение площади.
    """
    return figure.get_square()


def main() -> None:
    """Основная функция для демонстрации работы классов фигур."""
    rect = Rectangle(10, 20)
    circ = Circle(5)
    rhomb = Rhombus(6, 8)

    figures: list[Figure] = [rect, circ, rhomb]

    for fig in figures:
        print(f"Фигура: {fig.__class__.__name__}")
        print(f"  Периметр: {calculate_perimeter(fig):.2f}")
        print(f"  Площадь:  {calculate_square(fig):.2f}")
        print("-" * 20)


if __name__ == "__main__":
    main()