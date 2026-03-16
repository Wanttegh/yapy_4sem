from typing import List


def get_filtered(recom_ids: List[int], seen_ids: List[int]) -> List[int]:
    filtered = []

    seen_set_ids = set(seen_ids)

    for id in recom_ids:
        if id not in seen_set_ids:
            filtered.append(id)

    return filtered


def main():
    recom_ids = [1, 2, 3]
    seen_ids = [1, 4, 5]

    result = get_filtered(recom_ids, seen_ids)

    print(f"Filtered IDs: {result}")

if __name__ == "__main__":
    main()


# Алгоритмическая сложность - O(n), где n - длина списка recom_ids, m - длина списка seen_ids