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


def  build_complement_graph(exclusion_graph):
    graph = {}
    xlow, xhigh = min(x for x, _, _ in exclusion_graph), max(x for x, _, _ in exclusion_graph)
    ylow, yhigh = min(y for _, y, _ in exclusion_graph), max(y for _, y, _ in exclusion_graph)
    zlow, zhigh = min(z for _, _, z in exclusion_graph), max(z for _, _, z in exclusion_graph)
    for x in range(xlow - 1, xhigh + 2):
        for y in range(ylow - 1, yhigh + 2):
            for z in range(zlow - 1, zhigh + 2):
                cube = (x, y, z)
                if cube in exclusion_graph:
                    continue
                graph[cube] = set(
                    neighbour for neighbour in neighbours(cube) if neighbour not in exclusion_graph
                )
    return graph


def connected_components(graph, exculsion_graph):
    xlow = min(x for x, _, _ in graph)
    ylow = min(y for _, y, _ in graph)
    zlow = min(z for _, _, z in graph)
    nodes = set(graph)
    outer_point = (xlow, ylow, zlow)
    nodes.remove(outer_point)
    queue = {outer_point}
    while queue:  # remove outer component (reachable by air)
        node = queue.pop()
        node_neighbours = graph[node] & nodes
        queue |= node_neighbours
        nodes -= node_neighbours
    while nodes:
        component = set()
        queue = {nodes.pop()}
        while queue:
            node = queue.pop()
            component.add(node)
            node_neighbours = graph[node] & nodes
            queue |= node_neighbours
            nodes -= node_neighbours
        yield {cube: neighbours for cube, neighbours in graph.items() if cube in component}


def free_surface_area(graph):
    return sum(6 - len(neighbours) for neighbours in graph.values())


def part_1():
    graph = build_graph(read_data())
    surface_area = free_surface_area(graph)
    return surface_area


def part_2():
    lava_graph = build_graph(read_data())
    air_graph = build_complement_graph(lava_graph)
    air_pockets = connected_components(air_graph, lava_graph)
    total_surface_area = free_surface_area(lava_graph)
    air_pockets_surface_area = sum(
        free_surface_area(component) for component in connected_components(air_graph, lava_graph)
    )
    return total_surface_area - air_pockets_surface_area
