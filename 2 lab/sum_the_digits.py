def sum_of_digits(number: int) -> int:
    result = 0

    while number > 0:
        result += number % 10
        number = number // 10

    return result


def main():
    number = int(input())
    
    print(sum_of_digits(number))


if __name__ == "__main__":
    main()