from typing import List


def filter_sized(words: List[str], n: int) -> List[str]:
    
    f = sorted(filter(lambda word: len(word) == n, words))
    return f


def main():

    words = ['дом', 'улица', 'гараж', 'работа', 'он', 'она']
    n = int(input("Введите n: "))

    result = filter_sized(words, n)
    print(result)


if __name__ == "__main__":
    main()