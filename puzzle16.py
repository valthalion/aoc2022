from itertools import combinations

import networkx as nx


test = False


def clip(x):
    return x if x > 0 else 0


def read_data():
    filename = f'puzzle16{"-test" if test else ""}.in'
    with open(filename, 'r') as f:
        graph = nx.Graph()
        valves = {}
        for line in f:
            valve_info, tunnels_info = line.split(';')
            valve_tokens = valve_info.split()
            name = valve_tokens[1]
            flow_rate = int(valve_tokens[-1].split('=')[1])
            neighbours = set(word[:-1] if word.endswith(',') else word for word in tunnels_info.split()[4:])
            graph.add_edges_from([(name, neighbour) for neighbour in neighbours])
            if flow_rate:
                valves[name] = flow_rate
    return graph, valves


def transform_graph(graph, valves, start):
    distances = dict(nx.shortest_path_length(graph))
    valve_graph = nx.Graph()
    remaining_valves = set(valves)
    for valve in valves:
        valve_graph.add_edge(valve, start, weight=distances[valve][start])
        remaining_valves.remove(valve)
        for other_valve in valves:
            if valve == other_valve:
                continue
            valve_graph.add_edge(valve, other_valve, weight=distances[valve][other_valve])
    return valve_graph


def find_path(graph, pressures, time, agents=1):
    def _find_path(valves, remaining_time, pressure=0, start='AA'):
        if not (remaining_time and valves):
            return pressure

        best = pressure
        scored_valves = tuple(
            sorted(
                (
                    (score, v)
                    for v in valves
                    if (score := pressures[v] * (remaining_time - graph[start][v]['weight'] - 1)) > 0
                ),
                reverse=True
            )
        )
        valves = set(v for _, v in scored_valves)

        for _, valve in scored_valves:
            dist, valve_pressure = graph[start][valve]['weight'], pressures[valve]
            new_time = remaining_time - dist - 1
            new_pressure = pressure + new_time * valve_pressure
            new_valves = valves - {valve}

            next_steps = sorted(
                (pressures[v] * (new_time - graph[valve][v]['weight'] - 1) for v in new_valves),
                reverse=True
            )
            upper_bound = new_pressure + sum(next_steps[:new_time // 2])

            if upper_bound <= best:
                continue

            candidate = _find_path(new_valves, new_time, new_pressure, start=valve)
            if candidate > best:
                best = candidate

        return best

    return _find_path(valves=set(pressures), remaining_time=time)


def all_combinations(valves):
    for n in range(1, len(valves) // 2 + 1):
        combs = combinations(valves, n)
        for comb in combs:
            v1 = set(comb)
            yield v1, valves - v1


def find_path2(graph, pressures, time):
    def _find_path(valves, remaining_time, pressure=0, start='AA'):
        if not (remaining_time and valves):
            return pressure

        best = pressure
        scored_valves = tuple(
            sorted(
                (
                    (score, v)
                    for v in valves
                    if (score := pressures[v] * (remaining_time - graph[start][v]['weight'] - 1)) > 0
                ),
                reverse=True
            )
        )
        valves = set(v for _, v in scored_valves)

        for _, valve in scored_valves:
            dist, valve_pressure = graph[start][valve]['weight'], pressures[valve]
            new_time = remaining_time - dist - 1
            new_pressure = pressure + new_time * valve_pressure
            new_valves = valves - {valve}

            next_steps = sorted(
                (pressures[v] * (new_time - graph[valve][v]['weight'] - 1) for v in new_valves),
                reverse=True
            )
            upper_bound = new_pressure + sum(next_steps[:new_time // 2])

            if upper_bound <= best:
                continue

            candidate = _find_path(new_valves, new_time, new_pressure, start=valve)
            if candidate > best:
                best = candidate

        return best

    valves = set(pressures)
    return max(
        _find_path(valves1, time) + _find_path(valves2, time)
        for valves1, valves2 in all_combinations(valves)
    )



def part_1():
    graph, valves = read_data()
    graph = transform_graph(graph, valves, start='AA')
    return find_path(graph, pressures=valves, time=30)


def part_2():
    graph, valves = read_data()
    graph = transform_graph(graph, valves, start='AA')
    return find_path2(graph, pressures=valves, time=26)
