#!/usr/bin/env python3
from collections import defaultdict
from functools import reduce
import operator

def parse_input(f):
    rules = {}
    ticket = None
    nearby_tickets = []
    state = "rules"

    for line in f:
        line = line.strip()
        if not line:
            continue
        if line == "your ticket:":
            state = "ticket"
            continue
        if line == "nearby tickets:":
            state = "nearby_tickets"
            continue

        if state == "rules":
            name, rest = line.split(":")
            r1, r2 = [s.split("-") for s in rest.split("or")]
            range1 = range(int(r1[0]), int(r1[1])+1)
            range2 = range(int(r2[0]), int(r2[1])+1)
            rules[name] = [range1, range2]
        elif state == "ticket":
            ticket = [int(s) for s in line.split(",")]
        elif state == "nearby_tickets":
            nearby_tickets.append([int(s) for s in line.split(",")])

    return rules, ticket, nearby_tickets


def get_validity(ticket, rules):
    is_valid, error = True, 0
    for n in ticket:
        valid = any(r for r in rules.values() if n in r[0] or n in r[1])
        if not valid:
            is_valid = False
            error += n
    return is_valid, error


def get_error_rate(rules, tickets):
    validity = [get_validity(t, rules) for t in tickets]
    return sum(error for is_valid, error in validity if not is_valid)


def assign_fields(rules, tickets):
    n = len(rules)
    rule_names = set(rules)
    valid_positions = set(range(n))
    excluded_at_pos = defaultdict(set)
    excluded_for_name = defaultdict(set)
    pos_to_name = {}
    name_to_pos = {}

    for ticket in tickets:
        is_valid, _ = get_validity(ticket, rules)
        if not is_valid:
            continue
        for pos, number in enumerate(ticket):
            for name, ranges in rules.items():
                if number not in ranges[0] and number not in ranges[1]:
                    excluded_at_pos[pos].add(name)
                    excluded_for_name[name].add(pos)

    def update_excludes():
        for pos, name in pos_to_name.items():
            for other_pos in excluded_at_pos:
                if other_pos != pos:
                    excluded_at_pos[other_pos].add(name)
            for other_name in excluded_for_name:
                if other_name != name:
                    excluded_for_name[other_name].add(pos)

    assert not any(len(v) == n for k, v in excluded_at_pos.items())
    assert not any(len(v) == n for k, v in excluded_for_name.items())

    while len(pos_to_name) < n:
        for pos, names in excluded_at_pos.items():
            if pos not in pos_to_name and len(names) == n-1:
                name = (rule_names - names).pop()
                pos_to_name[pos] = name
                name_to_pos[name] = pos
                update_excludes()
        for name, positions in excluded_for_name.items():
            if name not in name_to_pos and len(positions) == n-1:
                pos = (valid_positions - positions).pop()
                pos_to_name[pos] = name
                name_to_pos[name] = pos
                update_excludes()

    return pos_to_name


if __name__ == "__main__":
    from textwrap import dedent
    example = dedent('''
    class: 1-3 or 5-7
    row: 6-11 or 33-44
    seat: 13-40 or 45-50

    your ticket:
    7,1,14

    nearby tickets:
    7,3,47
    40,4,50
    55,2,20
    38,6,12
    ''').strip().splitlines()

    rules, _, nearby_tickets = parse_input(example)
    assert get_error_rate(rules, nearby_tickets) == 71

    print("part 1")
    with open("input.txt") as f:
        rules, _, nearby_tickets = parse_input(f)
        print(get_error_rate(rules, nearby_tickets))

    example2 = dedent('''
    class: 0-1 or 4-19
    row: 0-5 or 8-19
    seat: 0-13 or 16-19

    your ticket:
    11,12,13

    nearby tickets:
    3,9,18
    15,1,5
    5,14,9
    ''').strip().splitlines()
    rules, _, nearby_tickets = parse_input(example2)
    assert assign_fields(rules, nearby_tickets) == {0: "row", 1: "class", 2: "seat"}

    print("part 2")
    with open("input.txt") as f:
        rules, ticket, nearby_tickets = parse_input(f)

    assignment = assign_fields(rules, nearby_tickets)
    departure_fields = [pos for pos, name in assignment.items() if name.startswith("departure")]
    print(reduce(operator.mul, [ticket[pos] for pos in departure_fields]))
