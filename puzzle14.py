test = False


def parse_line(line):
    endpoints = (
        tuple(int(x) for x in pair.split(','))
        for pair in line.split(' -> ')
    )
    startx, starty = next(endpoints)
    for endx, endy in endpoints:
        if startx == endx:
            delta = 1 if endy > starty else -1
            yield from ((startx, y) for y in range(starty, endy, delta))
        else:
            delta = 1 if endx > startx else -1
            yield from ((x, starty) for x in range(startx, endx, delta))
        startx, starty = endx, endy
    yield endx, endy


def read_data():
    filename = f'puzzle14{"-test" if test else ""}.in'
    with open(filename, 'r') as f:
        for line in f:
            yield from parse_line(line.strip())


def drop_sand(rocks, bottom):
    posx, posy = 500, 0
    while posy < bottom:
        for candidate in ((posx, posy + 1), (posx - 1, posy + 1), (posx + 1, posy + 1)):
            if candidate not in rocks:
                posx, posy = candidate
                break
        else:
            break
    return posx, posy


def count_drops(total_block):
    rocks = set(read_data())
    bottom = max(y for _x, y in rocks) + 1 # cannot cross the bottom
    stop_condition = 0 if total_block else bottom

    n = 0
    while True:
        x, y = drop_sand(rocks, bottom)
        if y == stop_condition:
            break
        else:
            rocks.add((x, y))
            n += 1
    if total_block:
        n += 1  # count the one that blocks the source
    return n


def part_1():
    return count_drops(total_block=False)


def part_2():
    return count_drops(total_block=True)
