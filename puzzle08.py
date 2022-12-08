test = False


def read_data():
    filename = f'puzzle08{"-test" if test else ""}.in'
    field = {}
    with open(filename, 'r') as f:
        for r, row in enumerate(f):
            for c, value in enumerate(row.strip()):
                field[(r, c)] = int(value)
    return field, r + 1, c + 1


def visible_from_outside(field, height, width):
    visible = set()

    # horizontal borders
    visible |= set((0, c) for c in range(width))
    visible |= set((height - 1, c) for c in range(width))

    # horizontal borders, skip corners (already in horizontal)
    visible |= set((r, 0) for r in range(1, height - 1))
    visible |= set((r, width - 1) for r in range(1, height - 1))

    # vertical line of sight
    for c in range(1, width - 1):
        # top-down
        max_tree_height = field[(0, c)]
        for r in range(1, height - 1):
            if (tree_height := field[(r, c)]) > max_tree_height:
                visible.add((r, c))
                max_tree_height = tree_height

        # bottom-up
        max_tree_height = field[(height - 1, c)]
        for r in reversed(range(1, height - 1)):
            if (tree_height := field[(r, c)]) > max_tree_height:
                visible.add((r, c))
                max_tree_height = tree_height

    # horizontal line of sight
    for r in range(1, height - 1):
        # left-right
        max_tree_height = field[(r, 0)]
        for c in range(1, width - 1):
            if (tree_height := field[(r, c)]) > max_tree_height:
                visible.add((r, c))
                max_tree_height = tree_height

        # bottom-up
        max_tree_height = field[(r, width - 1)]
        for c in reversed(range(1, width - 1)):
            if (tree_height := field[(r, c)]) > max_tree_height:
                visible.add((r, c))
                max_tree_height = tree_height

    return visible


def scenic_scores(field, height, width):
    for r in range(height):
        for c in range(width):
            # borders
            if r == 0 or r == height - 1 or c == 0 or c == width - 1:
                yield 0
                continue

            tree_height = field[(r, c)]

            visible_up = 0
            for new_r in reversed(range(r)):
                visible_up += 1
                if field[(new_r, c)] >= tree_height:
                    break

            visible_down = 0
            for new_r in range(r + 1, height):
                visible_down += 1
                if field[(new_r, c)] >= tree_height:
                    break

            visible_left = 0
            for new_c in reversed(range(c)):
                visible_left += 1
                if field[(r, new_c)] >= tree_height:
                    break

            visible_right = 0
            for new_c in range(c + 1, width):
                visible_right += 1
                if field[(r, new_c)] >= tree_height:
                    break

            yield visible_up * visible_down * visible_left * visible_right


def part_1():
    return len(visible_from_outside(*read_data()))


def part_2():
    return max(scenic_scores(*read_data()))
