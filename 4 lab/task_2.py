import string
import re


def is_panogram(text):
    """
    Проверяет, является ли строка панограммой (содержит все буквы алфавита).
    
    Панограмма - это предложение, которое содержит каждую букву алфавита хотя бы один раз.
    
    Args:
        text: Строка для проверки
    
    Returns:
        True, если строка - панограмма, иначе False
    """
    # Использую re для удаления всех символов, кроме букв
    text = text.lower()
    text = re.sub(r'[^a-z]', '', text)
    
    # Получаю уникальные буквы с помощью множества
    unique_letters = set(text)
    
    # Сравниваю с алфавитом
    return len(unique_letters) == len(string.ascii_lowercase)


# Демонстрация работы
def main():
    """Тестирует функцию на различных примерах."""
    test_strings = [
        "The quick brown fox jumps over the lazy dog",
        "Pack my box with five dozen liquor jugs",
        "Hello world",
        "abcdefghijklmnopqrstuvwxyz",
        "ABC DEF GHI JKL MNO PQR STU VWX YZ",
        "",
    ]
    
    for text in test_strings:
        result = is_panogram(text)
        print(f"'{text}' -> {result}")


if __name__ == "__main__":
    main()