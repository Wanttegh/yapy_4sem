import random 


def guess_number(number: int, attempts: int) -> str:
    for attempt in range(attempts):
        user_input = input(f"Попытка {attempt + 1}: Введите число: ")
        guess = int(user_input)

        if guess == number:
            print("Поздравляю!")
            return
        else:
            if attempt == 4:
                print(f"Попытки кончились. Было загадано: {number}")
                return
            else:
                if number < guess:
                    print("Меньше")
                else:
                    print("Больше")


def main():
    number = random.randint(1, 100)
    attempts = 5

    guess_number(number, attempts)


if __name__ == "__main__":
    main()