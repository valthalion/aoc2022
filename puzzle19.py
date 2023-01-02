from __future__ import annotations
from collections import deque
from typing import NamedTuple


test = False


class MaterialVector(NamedTuple):
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0

    @classmethod
    def of_type(cls, type_idx, num=1):
        components = [0] * 4
        components[type_idx] = num
        return cls(*components)

    def __add__(self, other: MaterialVector) -> MaterialVector:
        return MaterialVector(*(self_comp + other_comp for self_comp, other_comp in zip(self, other)))

    def __sub__(self, other: MaterialVector) -> MaterialVector:
        return MaterialVector(*(self_comp - other_comp for self_comp, other_comp in zip(self, other)))

    def __mul__(self, other: int) -> MaterialVector:
        return MaterialVector(*(other * self_comp for self_comp in self))

    def __floordiv__(self, other):
        return min(self_comp // other_comp for self_comp, other_comp in zip(self, other) if other_comp > 0)

    def __ge__(self, other: MaterialVector) -> bool:
        return all(self_comp >= other_comp for self_comp, other_comp in zip(self, other))

    def __gt__(self, other: MaterialVector) -> bool:
        return all(self_comp > other_comp for self_comp, other_comp in zip(self, other))

    def __le__(self, other: MaterialVector) -> bool:
        return any(self_comp <= other_comp for self_comp, other_comp in zip(self, other))

    def __lt__(self, other: MaterialVector) -> bool:
        return any(self_comp < other_comp for self_comp, other_comp in zip(self, other))

    def __eq__(self, other: MaterialVector) -> bool:
        return all(self_comp == other_comp for self_comp, other_comp in zip(self, other))

    def __ne__(self, other: MaterialVector) -> bool:
        return any(self_comp != other_comp for self_comp, other_comp in zip(self, other))


Robot = MaterialVector
robot_types = (0, 1, 2, 3)


class Blueprint(NamedTuple):
    ore_robot: Robot
    clay_robot: Robot
    obsidian_robot: Robot
    geode_robot: Robot
    number: int


class State(NamedTuple):
    time: int
    resources: MaterialVector
    robots: MaterialVector


def parse_blueprint(line):
    tokens = line.split()
    number = int(tokens[1][:-1])
    ore_robot = Robot(ore=int(tokens[6]))
    clay_robot = Robot(ore=int(tokens[12]))
    obsidian_robot = Robot(ore=int(tokens[18]), clay=int(tokens[21]))
    geode_robot = Robot(ore=int(tokens[27]), obsidian=int(tokens[30]))
    return Blueprint(ore_robot, clay_robot, obsidian_robot, geode_robot, number)


def read_data():
    filename = f'puzzle19{"-test" if test else ""}.in'
    with open(filename, 'r') as f:
        blueprints = [parse_blueprint(line.strip()) for line in f]
    return blueprints


def max_possible(time, resources, robots):
    max_future = (time * (time + 1)) // 2
    return resources.geode + robots.geode * time + max_future


def most_geodes(blueprint, time_steps, initial_resources=MaterialVector(), initial_robots=MaterialVector(ore=1)):
    max_robots = (
        max(blueprint.ore_robot.ore, blueprint.geode_robot.ore, blueprint.obsidian_robot.ore, blueprint.clay_robot.ore),
        blueprint.obsidian_robot.clay,
        blueprint.geode_robot.obsidian,
        time_steps
    )

    best = 0
    queue = [State(time=time_steps, resources=initial_resources, robots=initial_robots)]

    while queue:
        state = queue.pop()
        if state.time == 0:
            continue

        time, resources, robots = state
        for robot in robot_types:
            if robots[robot] >= max_robots[robot]:
                queue.append(State(time=0, resources=resources + robots * time, robots=robots))
                projection = resources.geode
                if projection > best:
                    best = projection
                continue

            new_time, new_resources, raw_mat = time, resources, blueprint[robot]
            while new_time and new_resources < raw_mat:
                new_time -= 1
                new_resources += robots
            if new_time == 0:
                queue.append(State(time=0, resources=new_resources, robots=robots))
                projection = new_resources.geode
                if projection > best:
                    best = projection
                continue

            new_time, new_resources, new_robots = new_time - 1, new_resources - raw_mat + robots, robots + Robot.of_type(robot)
            if max_possible(new_time, new_resources, new_robots) <= best:
                continue

            queue.append(State(time=new_time, resources=new_resources, robots=new_robots))
            projection = new_resources.geode + new_robots.geode * new_time
            if projection > best:
                best = projection
    print(best)
    return best


def quality_level(blueprint, time_steps):
    n = most_geodes(blueprint, time_steps=time_steps)
    return blueprint.number * n


def part_1():
    return sum(quality_level(blueprint, time_steps=24) for blueprint in read_data())


def part_2():
    total = 1
    for blueprint in read_data()[:3]:
        total *= most_geodes(blueprint, time_steps=32)
    return total
