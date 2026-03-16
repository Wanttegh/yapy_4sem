from typing import List


def find_intersection(str1: str, str2: str) -> str:
    list1 = [int(x) for x in str1.split()]
    list2 = [int(x) for x in str2.split()]
    
    intersection = list(filter(lambda x: x in list2, dict.fromkeys(list1)))
    
    return ' '.join(str(x) for x in intersection)


def main() -> None:
    str1 = '1 2 5 7 4 8 8'
    str2 = '8 5 9 0'
    
    print(f"Первая строка: {str1}")
    print(f"Вторая строка: {str2}")
    
    result = find_intersection(str1, str2)
    
    print(f"Пересечение: {result}")


if __name__ == "__main__":
    main()