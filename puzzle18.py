test = False


def read_data():
    filename = f'puzzle18{"-test" if test else ""}.in'
    with open(filename, 'r') as f:
        cubes = set(tuple(int(n) for n in line.strip().split(',')) for line in f)
    return cubes


def neighbours(cube):
    diffs = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    for diff in diffs:
        yield tuple(ci + di for ci, di in zip(cube, diff))
        yield tuple(ci - di for ci, di in zip(cube, diff))


def build_graph(cubes):
    graph = {
        cube: set(neighbour for neighbour in neighbours(cube) if neighbour in cubes)
        for cube in cubes
    }
    return graph


def part_1():
    graph = build_graph(read_data())
    surface_area = sum(6 - len(neighbours) for neighbours in graph.values())
    return surface_area


def part_2():
    lava_graph = build_graph(read_data())
    air_graph = build_complement_graph(lava_graph)
    # connected components of air_graph
    # remove outer component
    # take free surfaces of air components from free surfaces of lava graph
