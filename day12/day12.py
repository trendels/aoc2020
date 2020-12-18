#!/usr/bin/env python3

DIRECTIONS = "NESW"


def turn(direction, degrees):
    cur = DIRECTIONS.index(direction)
    new = cur + degrees//90
    return DIRECTIONS[new % 4]


def move(ship, instruction):
    x, y, direction = ship
    action, value = instruction[0], int(instruction[1:])
    if action == "N":
        return x, y + value, direction
    if action == "S":
        return x, y - value, direction
    if action == "E":
        return x + value, y, direction
    if action == "W":
        return x - value, y, direction
    if action == "L":
        return x, y, turn(direction, -value)
    if action == "R":
        return x, y, turn(direction, value)
    if action == "F":
        if direction == "N":
            return x, y + value, direction
        if direction == "E":
            return x + value, y, direction
        if direction == "S":
            return x, y - value, direction
        if direction == "W":
            return x - value, y, direction

    raise RuntimeError(f"Invalid instruction: {instruction}")


def rotate(waypoint, ship, degrees):
    x, y, _ = ship
    dx, dy = waypoint
    steps = abs(degrees//90)
    for _ in range(steps):
        if degrees > 0:
            dx, dy = dy, -dx
        else:
            dx, dy = -dy, dx
    return dx, dy


def move_part2(ship, waypoint, instruction):
    dx, dy = waypoint
    action, value = instruction[0], int(instruction[1:])
    if action == "N":
        return ship, (dx, dy + value)
    if action == "S":
        return ship, (dx, dy - value)
    if action == "E":
        return ship, (dx + value, dy)
    if action == "W":
        return ship, (dx - value, dy)
    if action == "L":
        return ship, rotate(waypoint, ship, -value)
    if action == "R":
        return ship, rotate(waypoint, ship, value)
    if action == "F":
        x, y, direction = ship
        return (x + value*dx, y + value*dy, direction), waypoint

    raise RuntimeError(f"Invalid instruction: {instruction}")



if __name__ == "__main__":
    example = """
    F10
    N3
    F7
    R90
    F11
    """.split()

    ship = (0, 0, "E")
    for instruction in example:
        ship = move(ship, instruction)
    assert ship == (17, -8, "S")

    print("part 1")
    ship = (0, 0, "E")
    with open("input.txt") as f:
        for instruction in f:
            ship = move(ship, instruction)
    x, y, _ = ship
    print(abs(x) + abs(y))

    ship = (0, 0, "E")
    waypoint = (10, 1)
    for instruction in example:
        ship, waypoint = move_part2(ship, waypoint, instruction)
    assert ship == (214, -72, "E")
    assert waypoint == (4, -10)

    print("part 2")
    ship = (0, 0, "E")
    waypoint = (10, 1)
    with open("input.txt") as f:
        for instruction in f:
            ship, waypoint = move_part2(ship, waypoint, instruction)
    x, y, _ = ship
    print(abs(x) + abs(y))
