from math import lcm

import networkx as nx


test = False


def chain_tuple(it):
    return tuple(item for subit in it for item in subit)


def read_data():
    filename = f'puzzle24{"-test" if test else ""}.in'
    blizzards = {'^': [], 'v': [], '<': [], '>': []}
    with open(filename, 'r') as f:
        for row, line in enumerate(f, start=-1):  # row 0 after wall
            for col, char in enumerate(line.strip(), start=-1):  # also skip wall column
                if char in blizzards:
                    blizzards[char].append((row, col))
    n_rows, n_cols = row, col  # normally end in n{row|col}s - 1, but the last wall is added
    return n_rows, n_cols, blizzards


def build_graph(n_rows, n_cols, blizzards):
    time_steps = lcm(n_rows, n_cols)
    all_positions = set((r, c) for r in range(n_rows) for c in range(n_cols))
    blizzard_positions = [
        {((r - t) % n_rows, c) for r, c in blizzards['^']} |
        {((r + t) % n_rows, c) for r, c in blizzards['v']} |
        {(r, (c - t) % n_cols) for r, c in blizzards['<']} |
        {(r, (c + t) % n_cols) for r, c in blizzards['>']}
        for t in range(time_steps)
    ]
    nodes = {(r, c, t) for t in range(time_steps) for r, c in all_positions - blizzard_positions[t]}

    def moves(orig):
        r, c, t = orig
        next_t = (t + 1) % time_steps
        if (dest := (r - 1, c, next_t)) in nodes:
            yield (orig, dest)
        if (dest := (r + 1, c, next_t)) in nodes:
            yield (orig, dest)
        if (dest := (r, c - 1, next_t)) in nodes:
            yield (orig, dest)
        if (dest := (r, c + 1, next_t)) in nodes:
            yield (orig, dest)
        if (dest := (r, c, next_t)) in nodes:
            yield (orig, dest)

    graph = nx.DiGraph()
    graph.add_edges_from(chain_tuple(moves(node) for node in nodes))

    graph.add_edges_from(tuple(
        (('start', t), ('start', (t + 1) % time_steps)) for t in range(time_steps - 1)
    ))
    graph.add_edges_from(tuple(
        (('start', t), (0, 0, (t + 1) % time_steps)) for t in range(time_steps)
    ))
    graph.add_edges_from(tuple(
        ((0, 0, t), ('start', (t + 1) % time_steps)) for t in range(time_steps)
    ))
    graph.add_edges_from(tuple(
        (('start', t), 'start') for t in range(time_steps - 1)
    ))

    last_row, last_col = n_rows - 1, n_cols - 1
    graph.add_edges_from(tuple(
        (('end', t), ('end', (t + 1) % time_steps)) for t in range(time_steps - 1)
    ))
    graph.add_edges_from(tuple(
        (('end', t), (last_row, last_col, (t + 1) % time_steps)) for t in range(time_steps)
    ))
    graph.add_edges_from(tuple(
        ((last_row, last_col, t), ('end', (t + 1) % time_steps)) for t in range(time_steps)
    ))
    graph.add_edges_from(tuple(
        (('end', t), 'end') for t in range(time_steps - 1)
    ))
    return graph, time_steps


def part_1():
    graph, _ = build_graph(*read_data())
    return nx.shortest_path_length(graph, ('start', 0), 'end') - 1

def part_2():
    accumulated_time = 0
    graph, time_steps = build_graph(*read_data())
    accumulated_time += nx.shortest_path_length(graph, ('start', accumulated_time % time_steps), 'end') - 1
    accumulated_time += nx.shortest_path_length(graph, ('end', accumulated_time % time_steps), 'start') - 1
    accumulated_time += nx.shortest_path_length(graph, ('start', accumulated_time % time_steps), 'end') -1
    return accumulated_time
