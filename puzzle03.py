def read_data(test=False):
    filename = f'puzzle03{"-test" if test else ""}.in'
    with open(filename, 'r') as f:
        for line in f:
            yield line.strip()


def priority(item):
    num = ord(item)
    if num >= 97:  # lowercase: ord('a') = 97
        return num - 96  # num - 97 +  1
    return num - 38  # ord('A') = 65; num - 65 + 27


def check_sack(items):
    pocket_size = len(items) // 2
    pocket1, pocket2 = set(items[:pocket_size]), set(items[pocket_size:])
    return pocket1, pocket2


def shared_item(item_sets):
    common = item_sets[0]
    for item_set in item_sets[1:]:
        common &= item_set
    return common.pop()


def group_sacks(sacks):
    while True:
        try:
            yield (set(next(sacks)), set(next(sacks)), set(next(sacks)))
        except StopIteration:
            break


def part_1(test=False):
    sacks = (check_sack(items) for items in read_data(test))
    priorities = (priority(shared_item(sack)) for sack in sacks)
    return sum(priorities)


def part_2():
    sacks = read_data(test=False)
    groups = group_sacks(sacks)
    badges = (shared_item(sack_group) for sack_group in groups)
    return sum(priority(badge) for badge in badges)
