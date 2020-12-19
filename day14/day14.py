#!/usr/bin/env python3
import re

mask_re = re.compile(r"^mask = ([X01]{36})$")
store_re = re.compile(r"^mem\[(\d+)\] = (\d+)$")


def mask_value(value, mask):
    for i, c in enumerate(reversed(mask)):
        if c == "0":
            value &= ~(1 << i)
        elif c == "1":
            value |= (1 << i)
        elif c != "X":
            raise RuntimeError(f"Invalid mask bit: {c}")
    return value


def mask_address(addr, mask):
    floating = []
    for i, c in enumerate(reversed(mask)):
        if c == "0":
            continue
        elif c == "1":
            addr |= (1 << i)
        elif c == "X":
            floating.append(i)
        else:
            raise RuntimeError(f"Invalid mask bit: {c}")

    if not floating:
        return [addr]

    addresses = []
    for i in range(2**len(floating)):
        value = addr
        for pos, bit in enumerate(floating):
            if i & (1 << pos):
                value |= (1 << bit)
            else:
                value &= ~(1 << bit)
        addresses.append(value)

    return addresses


def execute(program, memory):
    mask = None
    for line in program:
        match = mask_re.match(line)
        if match:
            mask = match.groups()[0]
            continue
        match = store_re.match(line)
        if match:
            addr, value = match.groups()
            memory[int(addr)] = mask_value(int(value), mask)
            continue
        raise RuntimeError(f"Invalid instruction: {line}")


def execute_part2(program, memory):
    mask = None
    for line in program:
        match = mask_re.match(line)
        if match:
            mask = match.groups()[0]
            continue
        match = store_re.match(line)
        if match:
            addr, value = match.groups()
            for a in mask_address(int(addr), mask):
                memory[a] = int(value)
            continue
        raise RuntimeError(f"Invalid instruction: {line}")


if __name__ == "__main__":
    from textwrap import dedent
    example = dedent('''
    mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
    mem[8] = 11
    mem[7] = 101
    mem[8] = 0
    ''').strip().splitlines()

    memory = {}
    execute(example, memory)
    assert sum(memory.values()) == 165

    print("part 1")
    memory = {}
    with open("input.txt") as f:
        execute(f, memory)
    print(sum(memory.values()))

    example2 = dedent('''
    mask = 000000000000000000000000000000X1001X
    mem[42] = 100
    mask = 00000000000000000000000000000000X0XX
    mem[26] = 1
    ''').strip().splitlines()

    memory = {}
    execute_part2(example2, memory)
    assert sum(memory.values()) == 208

    print("part 2")
    memory = {}
    with open("input.txt") as f:
        execute_part2(f, memory)
    print(sum(memory.values()))

