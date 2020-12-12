#!/usr/bin/env python3
import itertools


def check_number(window, n):
    for x, y in itertools.combinations(window, 2):
        if x != y and x + y == n:
            return True
    return False


def check_stream(stream, window_size=25):
    preamble = itertools.islice(stream, window_size)
    pos = 0
    window = list(preamble)
    for n in stream:
        yield n, check_number(window, n)
        window = window[1:] + [n]


def find_weakness(stream, n, window_size=25):
    window = []
    while True:
        if len(window) >= 2 and sum(window) == n:
            return min(window), max(window)
        if sum(window) < n:
            window.append(next(stream))
            continue
        if sum(window) > n:
            window = window[1:]
            continue

    return None, None


if __name__ == "__main__":
    example = '''
        35
        20
        15
        25
        47
        40
        62
        55
        65
        95
        102
        117
        150
        182
        127
        219
        299
        277
        309
        576
    '''.split()

    stream = map(int, example)
    result = next((n for n, valid in check_stream(stream, 5) if not valid), None)
    assert result == 127

    stream = map(int, example)
    assert find_weakness(stream, 127, window_size=5) == (15, 47)

    print("part 1")
    with open("input.txt") as f:
        stream = map(int, f)
        result = next((n for n, valid in check_stream(stream) if not valid), None)
        print(result)

    print("part 2")
    with open("input.txt") as f:
        stream = map(int, f)
        lo, hi = find_weakness(stream, result)
        print(lo + hi)
