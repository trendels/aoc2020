#!/usr/bin/env python3


class Board:
    def __init__(self, layout, max_adjacent=4, line_of_sight=False):
        self.layout = layout
        self.width = len(layout[0])
        self.height = len(layout)
        self.max_adjacent = max_adjacent
        self.line_of_sight = line_of_sight

    def __str__(self):
        return "\n".join(["".join(row) for row in self.layout])

    def __eq__(self, other):
        return self.layout == other.layout

    @classmethod
    def from_string(cls, s, **kw):
        return cls([list(l) for l in s.splitlines()], **kw)

    def copy(self):
        return type(self)(
            [row[:] for row in self.layout],
            max_adjacent=self.max_adjacent,
            line_of_sight=self.line_of_sight,
        )

    def get_neighbours(self, x, y):
        occupied = 0
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if (i, j) == (x, y):
                    continue
                if 0 <= i < self.width and 0 <= j < self.height:
                    if self.layout[j][i] == "#":
                        occupied += 1
        return occupied

    def get_neighbours_line_of_sight(self, x, y):
        occupied = 0
        for direction in (
                (0, -1), (1, -1), (1, 0), (1, 1),
                (0, 1), (-1, 1), (-1, 0), (-1, -1),
            ):
            i, j = x, y
            while True:
                i, j = i + direction[0], j + direction[1]
                if 0 <= i < self.width and 0 <= j < self.height:
                    value = self.layout[j][i]
                    if value == "#":
                        occupied += 1
                        break
                    elif value == "L":
                        break
                else:
                    break
        return occupied

    def evolve(self):
        new = self.copy()
        if self.line_of_sight:
            get_neighbours = self.get_neighbours_line_of_sight
        else:
            get_neighbours = self.get_neighbours
        for x in range(self.width):
            for y in range(self.height):
                value = self.layout[y][x]
                if value == ".":
                    continue
                occupied = get_neighbours(x, y)
                if value == "L":
                    if occupied == 0:
                        new.layout[y][x] = "#"
                elif value == "#":
                    if occupied >= self.max_adjacent:
                        new.layout[y][x] = "L"
        return new

    @property
    def num_occupied(self):
        return str(self).count("#")


def evolve_board(board, print_=False):
    i = 0
    while True:
        if print_:
            print(f"round {i}:\n{board}\n")
        new_board = board.evolve()
        if new_board == board:
            break
        board = new_board
        i += 1
    return board


if __name__ == "__main__":
    from textwrap import dedent
    example = dedent(
    '''
    L.LL.LL.LL
    LLLLLLL.LL
    L.L.L..L..
    LLLL.LL.LL
    L.LL.LL.LL
    L.LLLLL.LL
    ..L.L.....
    LLLLLLLLLL
    L.LLLLLL.L
    L.LLLLL.LL
    '''
    ).strip()

    board = Board.from_string(example)
    board = evolve_board(board)
    assert board.num_occupied == 37

    print("part 1")
    with open("input.txt") as f:
        layout = f.read()
    board = Board.from_string(layout)
    board = evolve_board(board)
    print(board.num_occupied)

    board = Board.from_string(example, max_adjacent=5, line_of_sight=True)
    board = evolve_board(board)
    assert board.num_occupied == 26

    print("part 2")
    with open("input.txt") as f:
        layout = f.read()
    board = Board.from_string(layout, max_adjacent=5, line_of_sight=True)
    board = evolve_board(board)
    print(board.num_occupied)
