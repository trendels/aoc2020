#!/usr/bin/env python3
import re

container_re = re.compile(r"^(\w+ \w+)")
contains_re = re.compile(r"(\d+) (\w+ \w+) bag")
empty_re = re.compile("no other bags.$")


def parse_rule(s):
    container = container_re.search(s).group(1)
    if empty_re.search(s):
        return container, {}
    contains = {}
    for num, color in contains_re.findall(s):
        contains[color] = int(num)
    return container, contains


def read_input(f):
    rules = {}
    for line in f:
        container, contains = parse_rule(line.strip())
        rules[container] = contains
    return rules


def find_containers_for(color, rules):
    result = set()
    queue = [color]

    while queue:
        bag = queue.pop()
        for container in rules:
            if container in result or container == bag:
                continue
            if bag in rules[container]:
                result.add(container)
                queue.append(container)

    return result


def count_total_bags(color, rules):
    total = 0
    queue = [(color, 1)]

    while queue:
        bag, multiplier = queue.pop()
        for contained, count in rules[bag].items():
            n = count * multiplier
            total += n
            queue.append((contained, n))

    return total


if __name__ == "__main__":
    from io import StringIO
    from textwrap import dedent

    f = StringIO(dedent(
    '''
    light red bags contain 1 bright white bag, 2 muted yellow bags.
    dark orange bags contain 3 bright white bags, 4 muted yellow bags.
    bright white bags contain 1 shiny gold bag.
    muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
    shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
    dark olive bags contain 3 faded blue bags, 4 dotted black bags.
    vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
    faded blue bags contain no other bags.
    dotted black bags contain no other bags.
    '''
    ).strip())

    rules = read_input(f)
    assert rules["light red"] == {"bright white": 1, "muted yellow": 2}
    assert rules["dotted black"] == {}

    assert find_containers_for("shiny gold", rules) == {
        "bright white",
        "muted yellow",
        "dark orange",
        "light red",
    }
    assert count_total_bags("shiny gold", rules) == 32

    print("part 1")
    with open("input.txt") as f:
        rules = read_input(f)
        result = find_containers_for("shiny gold", rules)
        print(len(result))

    print("part 2")
    with open("input.txt") as f:
        rules = read_input(f)
        total = count_total_bags("shiny gold", rules)
        print(total)
