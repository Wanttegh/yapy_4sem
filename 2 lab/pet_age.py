def get_age_string(years: int) -> str:
    if 11 <= years % 100 <= 19:
        return f"{years} лет"
    
    last_digit = years % 10
    if last_digit == 1:
        return f"{years} год"
    elif 2 <= last_digit <= 4:
        return f"{years} года"
    else:
        return f"{years} лет"


def main():
    name = input("Введите имя питомца: ")
    age_years = int(input("Введите возраст питомца в годах: "))
    
    print(f"{name} возрастом {age_years * 12} месяцев, или {get_age_string(age_years)} и 0 месяцев.")


if __name__ == "__main__":
    main()