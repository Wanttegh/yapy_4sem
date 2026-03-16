from typing import List, Dict


def lists_to_dicts(list1: List[int], list2: List[int]) -> tuple[Dict[int, int], Dict[int, int]]:
    dict1 = {item: index for index, item in enumerate(list1)}
    dict2 = {item: index for index, item in enumerate(list2)}

    return dict1, dict2


def find_unique_elements(dict1: Dict[int, int], dict2: Dict[int, int]) -> List[int]:
    keys1 = set(dict1.keys())
    keys2 = set(dict2.keys())

    return sorted(list(keys1.symmetric_difference(keys2)))


def find_common_elements(dict1: Dict[int, int], dict2: Dict[int, int]) -> List[int]:
    keys1 = set(dict1.keys())
    keys2 = set(dict2.keys())

    return sorted(list(keys1.intersection(keys2)))


def main():
    s1 = [1, 2, 3, 4, 5, 6, 7]
    s2 = [5, 6, 7, 8, 9]
    
    dict1, dict2 = lists_to_dicts(s1, s2)
    
    unique = find_unique_elements(dict1, dict2)
    common = find_common_elements(dict1, dict2)
    
    print(f"Уникальные элементы: {unique}")
    print(f"Общие элементы: {common}")

if __name__ == "__main__":
    main()