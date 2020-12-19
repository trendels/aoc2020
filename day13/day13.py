#!/usr/bin/env python3
from math import gcd


def delay(timestamp, busline):
    return busline - timestamp % busline


def lcm(a, b):
    return a * b // gcd(a, b)


def get_interval_and_offset(a, offset_a, b, offset_b):
    interval = lcm(a, b)
    for x in range(offset_a, offset_a + interval, a):
        #print(f"testing {x} for ({a}, {offset_a}), ({b}, {offset_b})")
        if (x + offset_b) % b == 0:
            return interval, x


def get_earliest_timestamp(schedule):
    offsets = [(int(l), d) for d, l in enumerate(schedule.split(",")) if l != "x"]
    interval, offset = offsets[0]
    for (next_interval, next_offset) in offsets[1:]:
        interval, offset = get_interval_and_offset(
            interval, offset, next_interval, next_offset,
        )
    return offset


if __name__ == "__main__":
    timestamp = 939
    buslines = [7, 13, 59, 31, 19]
    best = sorted([(l, delay(timestamp, l)) for l in buslines], key=lambda x: x[1])[0]
    assert best == (59, 5)

    with open("input.txt") as f:
        timestamp = int(f.readline())
        schedule = f.readline().strip()
        buslines = [int(s) for s in schedule.split(",") if s != "x"]

    print("part 1")
    best = sorted([(l, delay(timestamp, l)) for l in buslines], key=lambda x: x[1])[0]
    print(best[0] * best[1])

    assert get_earliest_timestamp("7,13,x,x,59,x,31,19") == 1068781
    assert get_earliest_timestamp("17,x,13,19") == 3417
    assert get_earliest_timestamp("67,7,59,61") == 754018
    assert get_earliest_timestamp("67,x,7,59,61") == 779210
    assert get_earliest_timestamp("67,7,x,59,61") == 1261476
    assert get_earliest_timestamp("1789,37,47,1889") == 1202161486

    print("part 2")
    print(get_earliest_timestamp(schedule))
