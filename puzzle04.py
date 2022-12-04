class Interval:
    def __init__(self, spec):
        self.low, self.high = (int(n) for n in spec.split('-'))

    def __contains__(self, other):
        return self.low <= other.low and self.high >= other.high

    def overlaps(self, other):
        return other.low <= self.high and other.high >= self.low

    def fully_overlaps(self, other):
        return other in self or self in other


def read_data(test=False):
    filename = f'puzzle04{"-test" if test else ""}.in'
    with open(filename, 'r') as f:
        for line in f:
            intervals = tuple(Interval(spec) for spec in line.strip().split(','))
            yield intervals


def part_1():
    return sum(1 for interval1, interval2 in read_data(test=False) if interval1.fully_overlaps(interval2))


def part_2():
    return sum(1 for interval1, interval2 in read_data(test=False) if interval1.overlaps(interval2))
