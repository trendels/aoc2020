#!/usr/bin/env python3


def parse_policy(policy):
    rng, char = policy.split(" ")
    lo, hi = rng.split("-")
    return char, int(lo), int(hi)


def is_valid(policy, password):
    char, lo, hi = parse_policy(policy)
    return lo <= password.count(char) <= hi


def is_valid_new(policy, password):
    char, p1, p2 = parse_policy(policy)
    ok1 = password[p1-1] == char
    ok2 = password[p2-1] == char
    return ok1 ^ ok2


if __name__ == "__main__":
    assert is_valid("1-3 a", "abcde")
    assert not is_valid("1-3 b", "cdefg")
    assert is_valid("2-9 c", "ccccccccc")

    print("part 1")
    valid = 0
    with open("input.txt") as f:
        for line in f:
            policy, password = line.split(": ")
            if is_valid(policy, password):
                valid += 1
    print(valid)

    assert is_valid_new("1-3 a", "abcde")
    assert not is_valid_new("1-3 b", "cdefg")
    assert not is_valid_new("2-9 c", "ccccccccc")

    print("part 2")
    valid_new = 0
    with open("input.txt") as f:
        for line in f:
            policy, password = line.split(": ")
            if is_valid_new(policy, password):
                valid_new += 1
    print(valid_new)
