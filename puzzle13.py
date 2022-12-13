from itertools import zip_longest


test = False


def read_data():
    filename = f'puzzle13{"-test" if test else ""}.in'
    packet_pairs = []
    with open(filename, 'r') as f:
        while True:
            left = eval(next(f).strip())
            right = eval(next(f).strip())
            packet_pairs.append((left, right))
            try:
                next(f)
            except StopIteration:
                break
    return packet_pairs


def cmp_values(left, right):
    if left < right:
        return True
    if left > right:
        return False
    return None


def cmp(left, right):
    if isinstance(left, int):  # int, ?
        if isinstance (right, int):  # int, int
            return cmp_values(left, right)
        return cmp([left], right)  # int, list
    if isinstance(right, int):  # list, int
        return cmp(left, [right])
    # list, list
    for new_left, new_right in zip_longest(left, right):
        if new_left is None:  # left ends first
            return True
        if new_right is None:  # right ends first
            return False
        comparison = cmp(new_left, new_right)
        if comparison is None:
            continue
        return comparison
    return None


def part_1():
    packet_pairs = read_data()
    return sum(idx for idx, packet_pair in enumerate(packet_pairs, start=1) if cmp(*packet_pair))


def part_2():
    sep1 = [[2]]
    sep2 = [[6]]
    idx1, idx2 = 0, 1  # start with [sep1, sep2], assume insertion sort but only keep track of these indices
    for packet_pair in read_data():
        for packet in packet_pair:
            if cmp(packet, sep1):
                idx1 += 1
                idx2 += 1
                continue
            if cmp(packet, sep2):
                idx2 +=1
    return (idx1 + 1) * (idx2 + 1)  # 1-based indices for the decoder key
