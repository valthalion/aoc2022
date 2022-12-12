import networkx as nx


test = False


def read_data():
    start, end = None, None
    start_height, end_height = ord('a'), ord('z')
    filename = f'puzzle12{"-test" if test else ""}.in'
    heightmap = []
    lowest = set()
    with open(filename, 'r') as f:
        for r, line in enumerate(f):
            heightmap.append(list())
            for c, code in enumerate(line.strip()):
                if code == 'S':
                    start = (r, c)
                    height = start_height
                elif code == 'E':
                    end = (r, c)
                    height = end_height
                else:
                    height = ord(code)
                heightmap[-1].append(height)
                if height == start_height:
                    lowest.add((r, c))
    nrows, ncols = len(heightmap), len(heightmap[0])

    def neighbours(r, c):
        if r > 0:
            yield r - 1, c
        if c > 0:
            yield r, c - 1
        if c < ncols - 1:
            yield r, c + 1
        if r < nrows - 1:
            yield r + 1, c

    graph = nx.DiGraph()
    for r in range(nrows):
        for c in range(ncols):
            height = heightmap[r][c]
            graph.add_edges_from(((r, c), (r2, c2)) for r2, c2 in neighbours(r, c) if heightmap[r2][c2] <= height + 1)
    return graph, start, end, lowest


def part_1():
    graph, start, end, _lowest = read_data()
    path = nx.shortest_path(graph, start, end)
    return len(path) - 1


def part_2():
    graph, _start, end, lowest = read_data()
    all_lengths = nx.single_target_shortest_path_length(graph, end)
    return min(length for start, length in all_lengths if start in lowest)
