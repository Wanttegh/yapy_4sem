from typing import List
from collections import Counter


def get_top(nums: List[int], k: int) -> List[int]:
    top = []
    
    if k <= 0 or not nums:
        return []
    
    frequency = Counter(nums)
    
    top = [item for item, _ in frequency.most_common(k)]
    
    return top


def main():
    test_cases = [
        ([1, 2, 3, 2, 5, 7, 1], 2),
        ([1, 2, 3, 3, 3, 3, 3], 1),
        ([1, 1], 1),
        ([], 2),
        ([1, 2, 3], 0),
        ([4, 4, 4, 4, 2, 2, 3, 3, 3], 3),
    ]
    
    for i, (nums, k) in enumerate(test_cases, 1):
        result = get_top(nums, k)
        
        result_sorted = sorted(result)
        
        print(f"nums = {nums}, k = {k} -> result = {result_sorted}")


if __name__ == "__main__":
    main()

# O(nlogn), n = len(nums)