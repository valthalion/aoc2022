import re
from typing import NamedTuple


class Move(NamedTuple):
    num: int
    from_stack: int
    to_stack: int


def read_data(test=False):
    cmd_re = re.compile(r'move (?P<num>\d+) from (?P<from_stack>\d+) to (?P<to_stack>\d+)')
    def parse(line):
        m = cmd_re.match(line)
        return Move(int(m.group('num')), *(int(n) - 1 for n in m.group('from_stack', 'to_stack')))

    filename = f'puzzle05{"-test" if test else ""}.in'
    num_stacks = 3 if test else 9
    stacks = {stack: list() for stack in range(num_stacks)}

    with open(filename, 'r') as f:
        while True:
            line = next(f).rstrip()
            if not line:
                break
            if line[1] == '1':
                continue
            for stack in range(num_stacks):
                col = 1 + stack * 4
                if col >= len(line):
                    break
                if (crate := line[col]) != ' ':
                    stacks[stack].append(crate)
    
        stacks = {stack: crates[::-1] for stack, crates in stacks.items()}
        moves = [parse(line.strip()) for line in f]
    return stacks, moves


def move(stacks, moves):
    for move in moves:
        for _ in range(move.num):
            stacks[move.to_stack].append(stacks[move.from_stack].pop())


def move2(stacks, moves):
    for move in moves:
        crates = stacks[move.from_stack][-move.num:]
        stacks[move.from_stack] = stacks[move.from_stack][:-move.num]
        stacks[move.to_stack].extend(crates)


def part_1():
    stacks, moves = read_data()
    move(stacks, moves)
    return ''.join(stack[-1] for stack in stacks.values())


def part_2():
    stacks, moves = read_data()
    move2(stacks, moves)
    return ''.join(stack[-1] for stack in stacks.values())
