def nickname_generator(name_and_surname: str) -> str:
    words = name_and_surname.split()

    nickname = f"{words[1][:3].upper()}_{words[0][:2].lower()}{len(name_and_surname)}"

    return nickname


def main():
    name_and_surname = input("Введите ваши имя и фамилию в формате Иван Иванов: ")

    print(nickname_generator(name_and_surname))


if __name__ == "__main__":
    main()