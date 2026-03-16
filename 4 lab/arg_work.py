def calculate(op, base, *numbers):
    result = base
    for num in numbers:
        match op:
            case '+':
                result += num
            case '-':
                result -= num
            case '*':
                result *= num
            case '/':
                result /= num
    return result

def main():
    print(f"('-', 6, 2, 1) -> {calculate('-', 6, 2, 1)}")      # -> 3
    print(f"('-', 6, 2, 1, 2) -> {calculate('-', 6, 2, 1, 2)}")   # -> 1
    print(f"('-', 6, 10) -> {calculate('-', 6, 10)}")        # -> -4

if __name__ == '__main__':
    main()