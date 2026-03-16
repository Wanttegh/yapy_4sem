def pass_func(age: int, passport_presence: str, invitation_presence: str) -> str:
    if (age >= 18 and passport_presence.lower() == "да") or (invitation_presence.lower() == "да"):
        print("Проходите")
    else:
        print("Вход воспрещен")


def main():
    age = int(input("Сколько вам лет? "))
    passport_presence = input("Паспорт на руках (да/нет)?" )
    invitation_presence = input("Пригласительное есть (да/нет)? ")

    pass_func(age, passport_presence, invitation_presence)


if __name__ == "__main__":
    main()