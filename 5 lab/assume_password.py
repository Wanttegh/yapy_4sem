import string
from typing import Tuple, List


def check_password(password: str, min_length: int) -> Tuple[bool, List[str]]:
    comments = []
    
    # Проверка длины
    if len(password) < min_length:
        comments.append(f"длина {len(password)} символов из {min_length}")
    
    # Набор специальных символов
    special_chars = "!@#$%^&*()-+"
    
    # Проверка наличия разных категорий символов
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in special_chars for c in password)
    
    # Добавление замечаний
    if not has_upper:
        comments.append("Нет хотя бы одной заглавной буквы")
    if not has_lower:
        comments.append("Нет хотя бы одной прописной буквы")
    if not has_digit:
        comments.append("Нет хотя бы одной цифры")
    if not has_special:
        comments.append("Нет хотя бы одного специального символа")
    
    # Пароль надежный, если нет замечаний
    is_strong = len(comments) == 0
    
    return is_strong, comments


def test_check_password() -> None:
    # Тест 1: Пароль с цифрами, без заглавных и спецсимволов
    result, comments = check_password('123456789i', 5)
    assert result == False, "Пароль должен быть ненадежным"
    assert sorted(comments) == sorted(['Нет хотя бы одной заглавной буквы', 'Нет хотя бы одного специального символа']), f"Ожидались замечания ['Нет хотя бы одной заглавной буквы', 'Нет хотя бы одного специального символа'], получено {comments}"
    print("Тест 1 пройден: '123456789i', N=5")
    
    # Тест 2: Пустой пароль
    result, comments = check_password('', 5)
    assert result == False, "Пустой пароль должен быть ненадежным"
    expected_comments = ['Нет хотя бы одной заглавной буквы', 'Нет хотя бы одного специального символа', 'Нет хотя бы одной прописной буквы', 'Нет хотя бы одной цифры', 'длина 0 символов из 5']
    assert sorted(comments) == sorted(expected_comments), f"Ожидались замечания {expected_comments}, получено {comments}"
    print("Тест 2 пройден: '', N=5")
    
    # Тест 3: Пароль недостаточной длины
    result, comments = check_password('Qwerty!', 9)
    assert result == False, "Пароль должен быть ненадежным из-за длины"
    assert 'длина 7 символов из 9' in comments, "Должно быть замечание о длине"
    print("Тест 3 пройден: 'Qwerty!', N=9")
    
    # Тест 4: Надежный пароль
    result, comments = check_password('MammaMia9*', 9)
    assert result == True, "Пароль должен быть надежным"
    assert comments == [], "У надежного пароля не должно быть замечаний"
    print("Тест 4 пройден: 'MammaMia9*', N=9")
    
    # Тест 5: Надежный пароль со скобками
    result, comments = check_password('(Abracadabrissimus5)', 9)
    assert result == True, "Пароль должен быть надежным"
    assert comments == [], "У надежного пароля не должно быть замечаний"
    print("Тест 5 пройден: '(Abracadabrissimus5)', N=9")
    
    print("\nВсе тесты успешно пройдены!")


def main():    
    password = input("Введите пароль для проверки: ")
    min_length = int(input("Введите минимальную длину пароля: "))
    
    is_strong, comments = check_password(password, min_length)
    
    if is_strong:
        print("\nПароль надежный!")
    else:
        print("\nПароль ненадежный!")
        print("Замечания:")
        for comment in comments:
            print(f"  - {comment}")


if __name__ == "__main__":
    main()
    test_check_password()