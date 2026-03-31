import math
from typing import Protocol


class Shape(Protocol):
    """
    Протокол (интерфейс) для геометрических фигур.

    Любой класс, реализующий методы get_perimeter и get_square,
    автоматически считается соответствующим этому протоколу.
    """

    def get_perimeter(self) -> float:
        """Метод для вычисления периметра."""
        ...

    def get_square(self) -> float:
        """Метод для вычисления площади."""
        ...


class Rectangle:
    """Класс прямоугольника со сторонами a и b."""

    def __init__(self, a: float, b: float) -> None:
        """
        Инициализирует прямоугольник.

        a: Сторона А.
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
    """Класс круга с радиусом r."""

    def __init__(self, r: float) -> None:
        """
        Инициализирует круг.

        r: Радиус круга.
        """
        self.r = r

    def get_perimeter(self) -> float:
        """Возвращает длину окружности."""
        return 2 * math.pi * self.r

    def get_square(self) -> float:
        """Возвращает площадь круга."""
        return math.pi * (self.r ** 2)


class Rhombus:
    """Класс ромба с диагоналями p и q."""

    def __init__(self, p: float, q: float) -> None:
        """
        Инициализирует ромб.

        p: Первая диагональ.
        q: Вторая диагональ.
        """
        self.p = p
        self.q = q

    def get_perimeter(self) -> float:
        """
        Возвращает периметр ромба.

        Сторона вычисляется через диагонали по теореме Пифагора:
        side = sqrt((p/2)^2 + (q/2)^2).
        """
        side = math.sqrt((self.p / 2) ** 2 + (self.q / 2) ** 2)
        return 4 * side

    def get_square(self) -> float:
        """Возвращает площадь ромба."""
        return (self.p * self.q) / 2


def calculate_perimeter(figure: Shape) -> float:
    """
    Вычисляет периметр любой фигуры, соответствующей протоколу Shape.

    figure: Объект фигуры.
    :return: Значение периметра.
    """
    return figure.get_perimeter()


def calculate_square(figure: Shape) -> float:
    """
    Вычисляет площадь любой фигуры, соответствующей протоколу Shape.

    figure: Объект фигуры.
    :return: Значение площади.
    """
    return figure.get_square()


def main() -> None:
    """Основная функция для демонстрации работы программы."""
    # Создаем экземпляры фигур
    rect = Rectangle(10, 20)
    circ = Circle(5)
    rhomb = Rhombus(6, 8)

    # Список объектов, каждый из которых неявно реализует протокол Shape
    figures: list[Shape] = [rect, circ, rhomb]

    for fig in figures:
        name = fig.__class__.__name__
        perimeter = calculate_perimeter(fig)
        square = calculate_square(fig)

        print(f"Фигура: {name}")
        print(f"  Периметр: {perimeter:.4f}")
        print(f"  Площадь:  {square:.4f}")
        print("-" * 20)


if __name__ == "__main__":
    main()