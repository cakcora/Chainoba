import numpy as np

def levenshtein_distance(string1, string2):
    """
        Calculates the distance between two strings string1 and string2 by combining Levenshtein distance and the
        memoization technique. This is an O(N*M) implementation using Dynamic Programming.
        :param string1: Blockchain user or transaction address
        :param string2: Blockchain user or transaction address

        :return: matrix: A matrix of distances between the strings following Wagner-Fischer’s algorithm.
        """
    size_x = len(string1) + 1
    size_y = len(string2) + 1
    matrix = np.zeros((size_x, size_y))

    for x in range(size_x):
        matrix[x, 0] = x
    for y in range(size_y):
        matrix[0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if string1[x - 1] == string2[y - 1]:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1],
                    matrix[x, y - 1] + 1
                )
            else:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1] + 1,
                    matrix[x, y - 1] + 1
                )
    return matrix[size_x - 1, size_y - 1]
