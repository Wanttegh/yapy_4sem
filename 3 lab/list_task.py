from typing import List


def transpose_matrix(matrix: List[List[int]]) -> List[List[int]]: 
    return [[matrix[i][j] for i in range(3)] for j in range(2)]


def main():
    matrix = [
        [1, 2],
        [5, 6],
        [9, 10],
    ]

    transposed = transpose_matrix(matrix)
    for row in transposed:
        print(row)


if __name__ == "__main__":
    main()