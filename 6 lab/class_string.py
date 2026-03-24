from typing import Union


class Str(str):
    """
    Сравнение объектов этого класса происходит сначала по длине строки,
    а затем лексикографически.
    """

    def __lt__(self, other: Union[str, 'Str']) -> bool:
        """
        Проверяет, меньше ли текущий объект другого.

        Сравнение происходит сначала по длине, затем лексикографически.

        Args:
            other: Объект для сравнения.

        Returns:
            True, если текущий объект меньше другого, иначе False.
        """
        if not isinstance(other, (str, Str)):
            return NotImplemented

        other_value = str(other)

        # Сначала сравниваем по длине
        if len(self) != len(other_value):
            return len(self) < len(other_value)

        # Если длины равны, сравниваем лексикографически
        return super().__lt__(other_value)

    def __le__(self, other: Union[str, 'Str']) -> bool:
        """
        Проверяет, меньше или равен текущий объект другому.
        """
        if not isinstance(other, (str, Str)):
            return NotImplemented
            
        other_value = str(other)
        
        # Сначала сравниваем по длине
        if len(self) != len(other_value):
            return len(self) < len(other_value)
        
        # Если длины равны, сравниваем лексикографически
        return super().__le__(other_value)

    def __gt__(self, other: Union[str, 'Str']) -> bool:
        """
        Проверяет, больше ли текущий объект другого.
        """
        if not isinstance(other, (str, Str)):
            return NotImplemented

        other_value = str(other)

        # Сначала сравниваем по длине
        if len(self) != len(other_value):
            return len(self) > len(other_value)

        # Если длины равны, сравниваем лексикографически
        return super().__gt__(other_value)

    def __ge__(self, other: Union[str, 'Str']) -> bool:
        """
        Проверяет, больше или равен текущий объект другому.
        """
        if not isinstance(other, (str, Str)):
            return NotImplemented
            
        other_value = str(other)
        
        # Сначала сравниваем по длине
        if len(self) != len(other_value):
            return len(self) > len(other_value)
        
        # Если длины равны, сравниваем лексикографически
        return super().__ge__(other_value)


def main() -> None:
    print(f"ac > ab ? => {Str("ac") > Str("ab")}")
    print(f"ac < a ? => {Str("ac") < Str("a")}")
    print(f"ac > a ? => {Str("ac") > Str("a")}")
    print(f"ac < aba ? => {Str("ac") < Str("aba")}")
    print(f"ac > aba ? => {Str("ac") > Str("aba")}")
    print(f"ac.upper() = {Str("ac").upper()}")


if __name__ == "__main__":
    main()