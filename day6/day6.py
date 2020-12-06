#!/usr/bin/env python3
import operator
from functools import reduce


def read_input(f):
    result = []
    for line in f:
        line = line.strip()
        if line:
            answers = set(line)
            result.append(answers)
        else:
            yield result
            result = []
    if result:
        yield result


def count_all_answers(group):
    return len(reduce(operator.or_, group))


def count_common_answers(group):
    return len(reduce(operator.and_, group))


if __name__ == "__main__":
    from io import StringIO
    from textwrap import dedent

    f = StringIO(dedent(
    '''
    abc

    a
    b
    c

    ab
    ac

    a
    a
    a
    a

    b
    '''
    ).strip())
    assert sum(map(count_all_answers, read_input(f))) == 11

    print("part 1")
    with open("input.txt") as f:
        count = sum(map(count_all_answers, read_input(f)))
        print(count)

    f = StringIO(dedent(
    '''
    abc

    a
    b
    c

    ab
    ac

    a
    a
    a
    a

    b
    '''
    ).strip())
    assert sum(map(count_common_answers, read_input(f))) == 6

    print("part 2")
    with open("input.txt") as f:
        count = sum(map(count_common_answers, read_input(f)))
        print(count)
