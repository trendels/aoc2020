#!/usr/bin/env python3
from collections import defaultdict, deque

def number_at_turn(target, start):
    start = list(map(int, start.split(",")))
    turn = 1
    number = None
    last_number = None
    last_spoken = defaultdict(lambda: deque([], 2))
    while turn <= target:
        if start:
            number, start = start[0], start[1:]
        elif len(last_spoken[number]) == 1:
            number = 0
        else:
            number = last_spoken[number][1] - last_spoken[number][0]
        last_spoken[number].append(turn)

        #print(f"turn {turn}: {number}")
        last_number = number
        turn += 1

    return number


if __name__ == "__main__":
    assert number_at_turn(2020, "0,3,6") == 436
    assert number_at_turn(2020, "1,3,2") == 1
    assert number_at_turn(2020, "2,1,3") == 10
    assert number_at_turn(2020, "1,2,3") == 27
    assert number_at_turn(2020, "2,3,1") == 78
    assert number_at_turn(2020, "3,2,1") == 438
    assert number_at_turn(2020, "3,1,2") == 1836

    print("part 1")
    print(number_at_turn(2020, "10,16,6,0,1,17"))

    #assert number_at_turn(30000000, "0,3,6") == 175594
    #assert number_at_turn(30000000, "1,3,2") == 2578
    #assert number_at_turn(30000000, "2,1,3") == 3544142
    #assert number_at_turn(30000000, "1,2,3") == 261214
    #assert number_at_turn(30000000, "2,3,1") == 6895259
    #assert number_at_turn(30000000, "3,2,1") == 18
    #assert number_at_turn(30000000, "3,1,2") == 362

    print("part 2")
    print(number_at_turn(30000000, "10,16,6,0,1,17"))
