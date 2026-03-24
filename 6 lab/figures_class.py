import math
from typing import Union


class Rectangle:
    """
    Класс, представляющий прямоугольник.

    Attributes:
        a (float): Первая сторона прямоугольника.
        b (float): Вторая сторона прямоугольника.
    """

    def __init__(self, a: float, b: float) -> None:
        """
        Инициализирует объект Rectangle.

        Args:
            a: Длина первой стороны.
            b: Длина второй стороны.

        Raises:
            ValueError: Если стороны неположительные.
        """
        if a <= 0 or b <= 0:
            raise ValueError("Стороны прямоугольника должны быть положительными числами")
        self.a = a
        self.b = b

    def get_perimeter(self) -> float:
        """
        Вычисляет периметр прямоугольника.

        Returns:
            Периметр прямоугольника.
        """
        return 2 * (self.a + self.b)

    def get_square(self) -> float:
        """
        Вычисляет площадь прямоугольника.

        Returns:
            Площадь прямоугольника.
        """
        return self.a * self.b

    def __repr__(self) -> str:
        """Возвращает официальное строковое представление объекта."""
        return f"Rectangle(a={self.a}, b={self.b})"


class Circle:
    """
    Класс, представляющий круг.

    Attributes:
        r (float): Радиус круга.
    """

    def __init__(self, r: float) -> None:
        """
        Инициализирует объект Circle.

        Args:
            r: Радиус круга.

        Raises:
            ValueError: Если радиус неположительный.
        """
        if r <= 0:
            raise ValueError("Радиус круга должен быть положительным числом")
        self.r = r

    def get_perimeter(self) -> float:
        """
        Вычисляет длину окружности (периметр круга).

        Returns:
            Длина окружности.
        """
        return 2 * math.pi * self.r

    def get_square(self) -> float:
        """
        Вычисляет площадь круга.

        Returns:
            Площадь круга.
        """
        return math.pi * self.r ** 2

    def __repr__(self) -> str:
        """Возвращает официальное строковое представление объекта."""
        return f"Circle(r={self.r})"


class Rhombus:
    """
    Класс, представляющий ромб.

    Attributes:
        p (float): Первая диагональ ромба.
        q (float): Вторая диагональ ромба.
    """

    def __init__(self, p: float, q: float) -> None:
        """
        Инициализирует объект Rhombus.

        Args:
            p: Длина первой диагонали.
            q: Длина второй диагонали.

        Raises:
            ValueError: Если диагонали неположительные.
        """
        if p <= 0 or q <= 0:
            raise ValueError("Диагонали ромба должны быть положительными числами")
        self.p = p
        self.q = q

    def get_perimeter(self) -> float:
        """
        Вычисляет периметр ромба.

        Периметр ромба через диагонали: 4 * sqrt((p/2)^2 + (q/2)^2)

        Returns:
            Периметр ромба.
        """
        half_p = self.p / 2
        half_q = self.q / 2
        side = math.sqrt(half_p ** 2 + half_q ** 2)
        return 4 * side

    def get_square(self) -> float:
        """
        Вычисляет площадь ромба.

        Площадь ромба через диагонали: (p * q) / 2

        Returns:
            Площадь ромба.
        """
        return (self.p * self.q) / 2

    def __repr__(self) -> str:
        """Возвращает официальное строковое представление объекта."""
        return f"Rhombus(p={self.p}, q={self.q})"


def calculate_perimeter(figure) -> float:
    return figure.get_perimeter()


def calculate_square(figure) -> float:
    return figure.get_square()


def main() -> None:
    """
    Демонстрирует работу классов геометрических фигур.
    """
    # Создание объектов различных фигур
    rectangle = Rectangle(5, 3)
    circle = Circle(4)
    rhombus = Rhombus(6, 8)

    # Прямоугольник
    print("Прямоугольник")
    print(f"Периметр: {calculate_perimeter(rectangle):.2f}")
    print(f"Площадь: {calculate_square(rectangle):.2f}")
    print()

    # Круг
    print("Окружность")
    print(f"Длина окружности: {calculate_perimeter(circle):.2f}")
    print(f"Площадь круга: {calculate_square(circle):.2f}")
    print()

    # Ромб
    print("Ромб")
    print(f"Периметр: {calculate_perimeter(rhombus):.2f}")
    print(f"Площадь: {calculate_square(rhombus):.2f}")
    print()

    # Демонстрация полиморфизма
    print("Полиморфизм")
    figures = [
        Rectangle(4, 6),
        Circle(3.5),
        Rhombus(5, 12),
        Rectangle(2.5, 4.5),
        Circle(2),
    ]

    for i, figure in enumerate(figures, 1):
        perimeter = calculate_perimeter(figure)
        square = calculate_square(figure)
        print(f"{figure}")
        print(f"    Периметр: {perimeter:.2f}")
        print(f"    Площадь: {square:.2f}")


if __name__ == "__main__":
    main()