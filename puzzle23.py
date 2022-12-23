from collections import defaultdict, deque


test = False


def read_data():
    filename = f'puzzle23{"-test" if test else ""}.in'
    with open(filename, 'r') as f:
        elves = {complex(c, r) for r, row in enumerate(f) for c, item in enumerate(row) if item == '#'}
    return elves


def rectangle(elves):
    left = min(elf.real for elf in elves)
    right = max(elf.real for elf in elves)
    top = max(elf.imag for elf in elves)
    bottom = min(elf.imag for elf in elves)
    return (right - left + 1) * (top - bottom + 1) - len(elves)


def neighbours(elf):
    yield from ((elf + r + i*1j) for r in range(-1, 2) for i in range(-1, 2) if r or i)


def move_neighbours(move, elf):
    ref = elf + move
    yield ref
    delta = move * 1j
    yield ref + delta
    yield ref - delta


def make_proposal(elf, elves, moves):
    if sum(1 for r in range(-1, 2) for i in range(-1, 2) if elf + r + i*1j in elves) == 1:
        return None

    for move in moves:
        if not any(pos in elves for pos in move_neighbours(move, elf)):
            return elf + move

    return None


def spread(elves, rounds=None):
    iterations = 1
    moves = deque([-1j, 1j, -1, 1])

    while True:
        proposals = defaultdict(list)

        for elf in elves:
            proposal = make_proposal(elf, elves, moves)
            if proposal is not None:
                proposals[proposal].append(elf)

        if not proposals:
            break

        for target, moving_elves in proposals.items():
            if len(moving_elves) == 1:
                elves.remove(moving_elves[0])
                elves.add(target)

        moves.rotate(-1)
        if rounds is not None:
            if iterations == rounds:
                break
        iterations += 1
    return elves, iterations


def part_1():
    elves, _ = spread(read_data(), rounds=10)
    return rectangle(elves)


def part_2():
    elves, iterations = spread(read_data())
    return iterations
