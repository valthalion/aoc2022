def read_data():
    elves = []
    elf = []
    with open('puzzle01.in', 'r') as f:
        for line in f:
            if line == '\n':
                elves.append(elf)
                elf = []
                continue
            elf.append(int(line.strip()))
        if elf:
            elves.append(elf)
    return elves


def part_1():
    elves = read_data()
    return max(sum(elf) for elf in elves)


def part_2():
    elves = read_data()
    return sum(sorted(sum(elf) for elf in elves)[-3:])
