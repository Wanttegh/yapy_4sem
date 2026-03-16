def calculate_sum(numbers):
    total = 0
    for number in numbers:
        total += number
    return total


def main():
    numbers = [1, 10, 100, 1000]
    
    result = calculate_sum(numbers)
    
    print(result)


if __name__ == "__main__":
    main()