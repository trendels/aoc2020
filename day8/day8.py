#!/usr/bin/env python3

class Machine:
    def __init__(self, program):
        self.ip = 0
        self.acc = 0
        self.program = program
        self.seen = set()
        self.stopped = False

    def run(self):
        while self.ip < len(self.program):
            self.seen.add(self.ip)
            self.process_instruction()
            if self.ip in self.seen:
                # about to enter infinite loop
                return
        self.stopped = True

    def process_instruction(self):
        line = self.program[self.ip]
        op, arg = line.split()
        arg = int(arg)

        if op == "acc":
            self.acc += arg
            self.ip += 1
        elif op == "jmp":
            self.ip += arg
        elif op == "nop":
            self.ip += 1
        else:
            raise RuntimeError(f"invald instruction: {op} {arg}")


if __name__ == "__main__":
    from textwrap import dedent
    program = dedent(
    '''
    nop +0
    acc +1
    jmp +4
    acc +3
    jmp -3
    acc -99
    acc +1
    jmp -4
    acc +6
    '''
    ).strip().splitlines()

    m = Machine(program)
    m.run()
    assert not m.stopped
    assert m.acc == 5

    with open("input.txt") as f:
        program = f.read().splitlines()

    print("part 1")
    m = Machine(program)
    m.run()
    assert not m.stopped
    print(m.acc)

    print("part 2")
    for i, line in enumerate(program):
        if line.startswith("jmp"):
            line = line.replace("jmp", "nop")
        elif line.startswith("nop"):
            line = line.replace("jmp", "nop")
        else:
            continue
        new_program = program[:i] + [line] + program[i+1:]
        m = Machine(new_program)
        m.run()
        if m.stopped:
            print(m.acc)
            break
