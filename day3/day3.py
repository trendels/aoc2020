#!/usr/bin/env python3


class Map:
    def __init__(self, pattern):
        self.pattern = pattern.splitlines()
        self.height = len(self.pattern)
        self.width = len(self.pattern[0])
        self.x = 0
        self.y = 0

    def right(self, n):
        self.x = (self.x + n) % self.width

    def down(self, n):
        self.y += n

    @property
    def value(self):
        return self.pattern[self.y][self.x]


def count_trees(pattern, right, down):
    m = Map(pattern)
    n = 0
    while m.y < m.height:
        if m.value == '#':
            n += 1
        m.right(right)
        m.down(down)
    return n


if __name__ == "__main__":
    from textwrap import dedent
    pattern = dedent(
    '''
    ..##.......
    #...#...#..
    .#....#..#.
    ..#.#...#.#
    .#...##..#.
    ..#.##.....
    .#.#.#....#
    .#........#
    #.##...#...
    #...##....#
    .#..#...#.#
    '''
    ).strip()

    assert count_trees(pattern, right=1, down=1) == 2
    assert count_trees(pattern, right=3, down=1) == 7
    assert count_trees(pattern, right=5, down=1) == 3
    assert count_trees(pattern, right=7, down=1) == 4
    assert count_trees(pattern, right=1, down=2) == 2

    with open("input.txt") as f:
        pattern = f.read()

    print("part 1")
    print(count_trees(pattern, right=3, down=1))

    print("part 2")
    result = (
          count_trees(pattern, right=1, down=1)
        * count_trees(pattern, right=3, down=1)
        * count_trees(pattern, right=5, down=1)
        * count_trees(pattern, right=7, down=1)
        * count_trees(pattern, right=1, down=2)
    )
    print(result)

