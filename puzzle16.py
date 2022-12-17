test = False


class Valve:
    def __init__(self, line):
        valve_info, tunnels_info = line.split(';')
        valve_tokens = valve_info.split()
        self.name = valve_tokens[1]
        self.flow_rate = int(valve_tokens[-1].split('=')[1])
        self.neighbours = set(word[:-1] if word.endswith(',') else word for word in tunnels_info.split()[4:])


def read_data():
    filename = f'puzzle16{"-test" if test else ""}.in'
    with open(filename, 'r') as f:
        valves = {}
        for line in f:
            valve = Valve(line)
            valves[valve.name] = valve
    return valves


def find_path(valves, current, time, useful_valves, pressure=0, visited=tuple(), open_valves=None):
    new_visited = (*visited, current)
    if open_valves is None:
        open_valves = set()
    if time == 1:
        return pressure, new_visited
    if len(open_valves) == useful_valves:
        return pressure + (time - 1) * sum(valves[v].flow_rate for v in open_valves), new_visited
    visited_set = set(visited)
    current_valve = valves[current]
    new_time = time - 1
    if visited:
        last = visited[-1]
        if last == current:
            last = visited[-2]
    else:
        last = None
    new_pressure = pressure + sum(valves[v].flow_rate for v in open_valves)

    best_pressure, best_path = -1, None
    if current_valve.flow_rate > 0 and current not in open_valves:
        # open current
        candidate_pressure, path = find_path(valves, current=current, time=new_time, useful_valves=useful_valves,
                                             pressure=new_pressure + current_valve.flow_rate, visited=new_visited,
                                             open_valves={*open_valves, current})
        if candidate_pressure > best_pressure:
            best_pressure, best_path = candidate_pressure, path
    first_candidates = current_valve.neighbours - visited_set
    second_candidates = current_valve.neighbours & visited_set
    # last_candidate = set()
    if last in second_candidates:
        second_candidates.remove(last)
        # last_candidate.add(last)
    candidates = (*first_candidates, *second_candidates)  # (*first_candidates, *second_candidates, *last_candidate)
    if not candidates:
        candidates = (last,)
    for candidate in candidates:
        candidate_pressure, path = find_path(valves, current=candidate, time=new_time, useful_valves=useful_valves,
                                             pressure=new_pressure, visited=new_visited, open_valves=open_valves)
        if candidate_pressure > best_pressure:
            best_pressure, best_path = candidate_pressure, path
    return best_pressure, best_path


def part_1():
    valves = read_data()
    useful_valves = sum(1 for valve in valves.values() if valve.flow_rate > 0)
    return find_path(valves, current='AA', time=30, useful_valves=useful_valves)
