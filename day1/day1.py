#!/usr/bin/env python3

def part1(numbers):
    for idx, i in enumerate(numbers):
        for j in numbers[idx+1:]:
            if i + j == 2020:
                return i, j


def part2(numbers):
    for idx, i in enumerate(numbers):
        for idx2, j in enumerate(numbers[idx+1:], start=idx):
            for k in numbers[idx2+1:]:
                if i + j + k == 2020:
                    return i, j, k


if __name__ == "__main__":
    with open("input.txt") as f:
        numbers = [int(line) for line in f]

    print("part 1")
    i, j = part1(numbers)
    print(f"{i} + {j} = {i+j}")
    print(f"{i} * {j} = {i*j}")

    print("part 2")
    i, j, k = part2(numbers)
    print(f"{i} + {j} + {k} = {i+j+k}")
    print(f"{i} * {j} * {k} = {i*j*k}")
