test = False


delta = {
    'U': 1j,
    'D': -1j,
    'R': 1,
    'L': -1
}


def read_data():
    filename = f'puzzle09{"-test" if test else ""}.in'
    cmds = []
    with open(filename, 'r') as f:
        for line in f:
            direction, steps = line.strip().split()
            cmds.append((direction, int(steps)))
    return cmds


def follow(head, tail):
    diff = head - tail

    if abs(diff.real) > 1:
        real_step = 1 if diff.real > 0 else -1
        if diff.imag == 0:
            return real_step
        else:
            return real_step + (1j if diff.imag > 0 else -1j)

    if abs(diff.imag) > 1:
        imag_step = 1j if diff.imag > 0 else -1j
        if diff.real == 0:
            return imag_step
        else:
            return (1 if diff.real > 0 else -1) + imag_step

    return 0


def move(start, cmds):
    rope = start
    for direction, steps in cmds:
        for _ in range(steps):
            rope[0] += delta[direction]
            for pos in range(1, len(rope)):
                rope[pos] += follow(rope[pos - 1], rope[pos])
            yield


def visit_tail(rope):
    visited = set()
    for _ in move(rope, read_data()):
        visited.add(rope[-1])
    return visited


def part_1():
    return len(visit_tail(rope=[0] * 2))


def part_2():
    return len(visit_tail(rope=[0] * 10))
