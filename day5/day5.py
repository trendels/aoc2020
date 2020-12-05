#!/usr/bin/env python3

def decode_boarding_pass(s):
    rows = (0, 127)
    cols = (0, 7)

    for c in s:
        if c == "F":
            rows = (rows[0], rows[0] + (rows[1] - rows[0])//2)
        elif c == "B":
            rows = (rows[1] - (rows[1] - rows[0])//2, rows[1])
        elif c == "L":
            cols = (cols[0], cols[0] + (cols[1] - cols[0])//2)
        elif c == "R":
            cols = (cols[1] - (cols[1] - cols[0])//2, cols[1])
        #print(c, rows, cols)

    assert rows[0] == rows[1]
    assert cols[0] == cols[1]

    row, col = rows[0], cols[0]
    seat_id = row*8 + col
    return row, col, seat_id


if __name__ == "__main__":
    assert decode_boarding_pass("FBFBBFFRLR") == (44, 5, 357)
    assert decode_boarding_pass("BFFFBBFRRR") == (70, 7, 567)
    assert decode_boarding_pass("FFFBBBFRRR") == (14, 7, 119)
    assert decode_boarding_pass("BBFFBBFRLL") == (102, 4, 820)

    with open("input.txt") as f:
        passes = [decode_boarding_pass(line) for line in f]

    print("part 1")
    greatest_id = max(p[2] for p in passes)
    print(greatest_id)

    print("part 2")
    seat_ids = sorted(p[2] for p in passes)
    for i, seat_id in enumerate(seat_ids):
        if i > 0 and seat_ids[i+1] != seat_id+1:
            print(seat_id+1)
            break
