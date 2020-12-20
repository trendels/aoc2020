#!/usr/bin/env python3


def read_slice(s):
    active = set()
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            if c == "#":
                active.add((x, y, 0))
    return active


def read_slice_4d(s):
    active = set()
    for cell_3d in read_slice(s):
        x, y, z = cell_3d
        active.add((x, y, z, 0))
    return active


def get_neighbors_3d(cell):
    x, y, z = cell
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            for dz in range(-1, 2):
                if dx == dy == dz == 0:
                    continue
                yield (x+dx, y+dy, z+dz)


def get_neighbors_4d(cell):
    x, y, z, w = cell
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            for dz in range(-1, 2):
                for dw in range(-1, 2):
                    if dx == dy == dz == dw == 0:
                        continue
                    yield (x+dx, y+dy, z+dz, w+dw)


def evolve(state, get_neighbors=get_neighbors_3d):
    seen = set()
    next_state = set()
    for cell in state:
        neighbors = set(get_neighbors(cell))
        num_active = sum(n in state for n in neighbors)
        if 2 <= num_active <= 3:
            next_state.add(cell)

        for other in neighbors:
            if other not in state and other not in seen:
                num_active = sum(n in state for n in get_neighbors(other))
                if num_active == 3:
                    next_state.add(other)
            seen.add(other)

    return next_state


def evolve_state(state, turns, dim4=False):
    for _ in range(turns):
        if dim4:
            state = evolve(state, get_neighbors_4d)
        else:
            state = evolve(state)
    return state


if __name__ == "__main__":
    from textwrap import dedent
    example = dedent('''
    .#.
    ..#
    ###
    ''').strip()
    state = read_slice(example)
    assert state == {
        (1, 0, 0),
        (2, 1, 0),
        (0, 2, 0),
        (1, 2, 0),
        (2, 2, 0),
    }

    assert len(evolve_state(state, turns=6)) == 112

    print("part 1")
    with open("input.txt") as f:
        state = read_slice(f.read())
    print(len(evolve_state(state, turns=6)))

    state = read_slice_4d(example)
    assert len(evolve_state(state, turns=6, dim4=True)) == 848

    print("part 2")
    with open("input.txt") as f:
        state = read_slice_4d(f.read())
    print(len(evolve_state(state, turns=6, dim4=True)))

