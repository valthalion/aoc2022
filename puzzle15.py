import re
from typing import NamedTuple


test = False
line_re = re.compile(r'.+x=(?P<sx>\-?\d+), y=(?P<sy>\-?\d+):.+x=(?P<bx>\-?\d+), y=(?P<by>\-?\d+)')


class Point(NamedTuple):
    x: int
    y: int

    def __sub__(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)


class Sensor:
    def __init__(self, position: Point, closest_beacon: Point):
        self.position = position
        self.closest_beacon = closest_beacon
        self.radius = position - closest_beacon

    def covered_interval(self, y):
        delta_y = abs(self.position.y - y)
        radius = self.radius - delta_y
        if radius < 0:
            return set()
        low, high = self.position.x - radius, self.position.x + radius
        if self.closest_beacon.y == y:
            if self.closest_beacon.x < self.position.x:
                low += 1
            else:
                high -= 1
        return set(range(low, high + 1))

    def perimeter(self, limit):
        x, y = self.position.x, self.position.y + self.radius + 1
        if y > limit:
            x += y - limit
            y = limit
        while y > self.position.y and x <= limit and y >= 0:
            yield Point(x, y)
            x += 1
            y -= 1

        x, y = self.position.x + self.radius + 1, self.position.y
        if x > limit:
            y -= x - limit
            x = limit
        while x > self.position.x and x >= 0 and y >= 0:
            yield Point(x, y)
            x -= 1
            y -= 1

        x, y = self.position.x, self.position.y - self.radius - 1
        if y < 0:
            x += y  # x -= 0 - y
            y = 0
        while y < self.position.y and x >= 0 and y <= limit:
            yield Point(x, y)
            x -= 1
            y += 1

        x, y = self.position.x - self.radius - 1, self.position.y
        if x < 0:
            y -= x  # y -= 0 - x
            x = 0
        while x > self.position.x and x <= limit and y <= limit:
            yield Point(x, y)
            x += 1
            y += 1

    def __contains__(self, other):
        return self.position - other <= self.radius

    def __repr__(self):
        return f'Sensor(x={self.position.x}, y={self.position.y}, r={self.radius})'

    __str__ = __repr__
        

def parse_line(line):
    m = line_re.match(line)
    return (
        Point(int(m.group('sx')), int(m.group('sy'))),
        Point(int(m.group('bx')), int(m.group('by')))
    )


def read_data():
    filename = f'puzzle15{"-test" if test else ""}.in'
    with open(filename, 'r') as f:
        for line in f:
            yield parse_line(line.strip())


def find_beacon(sensors, size):
    for sensor in sensors:
        candidates = [
            point
            for point in sensor.perimeter(limit=size)
            if all(point not in other_sensor for other_sensor in sensors)
        ]
        if candidates:
            if len(candidates) > 1:
                raise RuntimeError('Unexpected number of candidates:', candidates)
            return candidates.pop()


def part_1():
    line = 10 if test else 2_000_000
    sensors = [Sensor(sensor, beacon) for sensor, beacon in read_data()]
    covered_positions = set()
    for sensor in sensors:
        covered_positions |= sensor.covered_interval(y=line)
    return len(covered_positions)


def part_2():
    size = 20 if test else 4_000_000
    sensors = [Sensor(sensor, beacon) for sensor, beacon in read_data()]
    missing_beacon = find_beacon(sensors, size)
    freq = 4_000_000 * missing_beacon.x + missing_beacon.y
    return freq
