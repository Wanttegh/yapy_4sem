from functools import reduce
from typing import List


# Решение без reduce и анонимных функций
def word_maker(letters: List[str]) -> str:
    """Convert list of lowercase letters to uppercase joined string."""
    word = ''.join(letter.upper() for letter in letters)
    return word


def main():

    input_word = input("Введите слово из строчных букв: ")

    letters = list(input_word)

    result_reduce = reduce(lambda acc, x: acc + x.upper(), letters, '')
    print(f"Результат с reduce: {result_reduce}")

    result_function = word_maker(letters)
    print(f"Результат через функцию: {result_function}")


if __name__ == "__main__":
    main()