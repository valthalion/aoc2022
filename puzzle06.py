from collections import deque, defaultdict


test = False


def read_data():
    filename = f'puzzle06{"-test" if test else ""}.in'
    with open(filename, 'r') as f:
        if test:
            return tuple(iter(line.strip()) for line in f)
        else:
            return iter(next(f).strip())


def find_marker(stream, length=4):
    counts = defaultdict(int)
    marker = deque(maxlen=length)

    for _ in range(length - 1):
        item = next(stream)
        marker.append(item)
        counts[item] += 1

    for pos, item in enumerate(stream, start=length):
        marker.append(item)
        counts[item] += 1
        if all(count <= 1 for count in counts.values()):
            return ''.join(marker), pos
        removed = marker.popleft()
        counts[removed] -= 1


def part_1():
    if test:
        streams = read_data()
        results = []
        for stream in streams:
            marker, pos = find_marker(stream)
            results.append(pos)
        return results

    stream = read_data()
    marker, pos = find_marker(stream)
    return marker, pos


def part_2():
    if test:
        streams = read_data()
        results = []
        for stream in streams:
            marker, pos = find_marker(stream, length=14)
            results.append(pos)
        return results

    stream = read_data()
    marker, pos = find_marker(stream, length=14)
    return marker, pos
