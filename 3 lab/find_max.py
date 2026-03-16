from typing import List


def get_top(nums: List[int], k: int) -> List[int]:
    top = []
    
    if k <= 0 or not nums:
        return top
    
    sorted_nums = sorted(nums, reverse=True)
    top = sorted_nums[:k]

    return top


def main():
    test_cases = [
        ([1, 2, 3, 2, 5, 7, 1], 2),
        ([1, 2, 3, 3, 3, 3, 3], 1),
        ([1, 1], 1),
        ([5, 5, 5, 5], 2),
        ([], 3),
        ([1, 2, 3], 0)
    ]
    
    for nums, k in test_cases:
        result = get_top(nums, k)
        print(f"nums = {nums}, k = {k} -> result = {result}")


if __name__ == "__main__":
    main()

# O(nlogn), n = len(nums)