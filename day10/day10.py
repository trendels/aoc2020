#!/usr/bin/env python3
from collections import Counter
from math import factorial


def get_differences(adapters):
    levels = [0] + sorted(adapters) + [max(adapters) + 3]
    differences = []
    for i in range(1, len(levels)):
        differences.append(levels[i] - levels[i-1])
    return differences


def count_differences(adapters):
    differences = Counter(get_differences(adapters))
    return dict(differences)


def get_combinations(adapters):
    total = 1
    ones, l = True, 0
    for d in get_differences(adapters):
        if d == 1:
            ones, l = True, l+1
        else:
            if ones and l > 1:
                # number of possibilities to take 2 from l (combinations)
                p = factorial(l)//(factorial(l-2)*2)
                total *= p+1
            ones, l = False, 0
    return total


if __name__ == "__main__":
    example1 = '''
    16
    10
    15
    5
    1
    11
    7
    19
    6
    12
    4
    '''.split()

    adapters = list(map(int, example1))
    assert count_differences(adapters) == {1: 7, 3: 5}
    assert get_combinations(adapters) == 8

    example2 = '''
    28
    33
    18
    42
    31
    14
    46
    20
    48
    47
    24
    23
    49
    45
    19
    38
    39
    11
    1
    32
    25
    35
    8
    17
    7
    9
    4
    2
    34
    10
    3
    '''.split()

    adapters = list(map(int, example2))
    assert count_differences(adapters) == {1: 22, 3: 10}
    assert get_combinations(adapters) == 19208

    with open("input.txt") as f:
        adapters = list(map(int, f))

    print("part 1")
    d = count_differences(adapters)
    print(d[1] * d[3])

    print("part 2")
    print(get_combinations(adapters))
