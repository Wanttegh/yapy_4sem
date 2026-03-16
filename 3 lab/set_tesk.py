from typing import Set, Tuple


def analyze_sets(set1: Set[int], set2: Set[int]) -> Tuple[Set[int], Set[int]]:
    unique_elements = set1.symmetric_difference(set2)

    common_elements = set1.intersection(set2)
    
    return unique_elements, common_elements


def print_set_analysis(set1: Set[int], set2: Set[int]) -> None:
    unique, common = analyze_sets(set1, set2)

    print(f"Уникальные элементы: {unique}")
    
    print(f"Общие элементы: {common}")


def main():
    s1 = {1, 2, 3, 4, 5, 6, 7}
    s2 = {5, 6, 7, 8, 9}

    print_set_analysis(s1, s2)


if __name__ == "__main__":
    main()