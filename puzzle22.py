test = False


heading_translations = {1: 0, 1j: 1, -1: 2, -1j: 3}

test_sides = {
    1: {'top': 1, 'bottom': 4, 'left': 9, 'right': 12},
    2: {'top': 5, 'bottom': 8, 'left': 1, 'right': 4},
    3: {'top': 5, 'bottom': 8, 'left': 5, 'right': 8},
    4: {'top': 5, 'bottom': 8, 'left': 9, 'right': 12},
    5: {'top': 9, 'bottom': 12, 'left': 9, 'right': 12},
    6: {'top': 9, 'bottom': 12, 'left': 13, 'right': 16}
}

test_mappings = {
    1: {
        'top': {'side': 2, 'side_edge': 'top', 'invert': True},
        'bottom': {'side': 4, 'side_edge': 'top', 'invert': False},
        'left': {'side': 3, 'side_edge': 'top', 'invert': False},
        'right': {'side': 6, 'side_edge': 'right', 'invert': True}
    },
    2: {
        'top': {'side': 1, 'side_edge': 'top', 'invert': True},
        'bottom': {'side': 5, 'side_edge': 'bottom', 'invert': True},
        'left': {'side': 6, 'side_edge': 'bottom', 'invert': True},
        'right': {'side': 3, 'side_edge': 'left', 'invert': False}
    },
    3: {
        'top': {'side': 1, 'side_edge': 'left', 'invert': False},
        'bottom': {'side': 5, 'side_edge': 'left', 'invert': True},
        'left': {'side': 2, 'side_edge': 'right', 'invert': False},
        'right': {'side': 4, 'side_edge': 'left', 'invert': False}
    },
    4: {
        'top': {'side': 1, 'side_edge': 'bottom', 'invert': False},
        'bottom': {'side': 5, 'side_edge': 'top', 'invert': False},
        'left': {'side': 3, 'side_edge': 'right', 'invert': False},
        'right': {'side': 6, 'side_edge': 'top', 'invert': True}
    },
    5: {
        'top': {'side': 4, 'side_edge': 'bottom', 'invert': False},
        'bottom': {'side': 2, 'side_edge': 'bottom', 'invert': True},
        'left': {'side': 3, 'side_edge': 'bottom', 'invert': True},
        'right': {'side': 6, 'side_edge': 'left', 'invert': False}
    },
    6: {
        'top': {'side': 4, 'side_edge': 'right', 'invert': True},
        'bottom': {'side': 2, 'side_edge': 'top', 'invert': True},
        'left': {'side': 5, 'side_edge': 'right', 'invert': False},
        'right': {'side': 1, 'side_edge': 'right', 'invert': True}
    },
}


sides = {
    1: {'top': 1, 'bottom': 50, 'left': 51, 'right': 100},
    2: {'top': 1, 'bottom': 50, 'left': 101, 'right': 150},
    3: {'top': 51, 'bottom': 100, 'left': 51, 'right': 100},
    4: {'top': 101, 'bottom': 150, 'left': 1, 'right': 50},
    5: {'top': 101, 'bottom': 150, 'left': 51, 'right': 100},
    6: {'top': 151, 'bottom': 200, 'left': 1, 'right': 50}
}

mappings = {
    1: {
        'top': {'side': 6, 'side_edge': 'left', 'invert': False},
        'bottom': {'side': 3, 'side_edge': 'top', 'invert': False},
        'left': {'side': 4, 'side_edge': 'left', 'invert': True},
        'right': {'side': 2, 'side_edge': 'left', 'invert': False}
    },
    2: {
        'top': {'side': 6, 'side_edge': 'bottom', 'invert': False},
        'bottom': {'side': 3, 'side_edge': 'right', 'invert': False},
        'left': {'side': 1, 'side_edge': 'right', 'invert': False},
        'right': {'side': 5, 'side_edge': 'right', 'invert': True}
    },
    3: {
        'top': {'side': 1, 'side_edge': 'bottom', 'invert': False},
        'bottom': {'side': 5, 'side_edge': 'top', 'invert': False},
        'left': {'side': 4, 'side_edge': 'top', 'invert': False},
        'right': {'side': 2, 'side_edge': 'bottom', 'invert': False}
    },
    4: {
        'top': {'side': 3, 'side_edge': 'left', 'invert': False},
        'bottom': {'side': 6, 'side_edge': 'top', 'invert': False},
        'left': {'side': 1, 'side_edge': 'left', 'invert': True},
        'right': {'side': 5, 'side_edge': 'left', 'invert': False}
    },
    5: {
        'top': {'side': 3, 'side_edge': 'bottom', 'invert': False},
        'bottom': {'side': 6, 'side_edge': 'right', 'invert': False},
        'left': {'side': 4, 'side_edge': 'right', 'invert': False},
        'right': {'side': 2, 'side_edge': 'right', 'invert': True}
    },
    6: {
        'top': {'side': 4, 'side_edge': 'bottom', 'invert': False},
        'bottom': {'side': 2, 'side_edge': 'top', 'invert': False},
        'left': {'side': 1, 'side_edge': 'top', 'invert': False},
        'right': {'side': 5, 'side_edge': 'bottom', 'invert': False}
    },
}


class Board:
    def __init__(self, walls, row_left, row_right, col_top, col_bottom):
        self.walls = walls
        self.row_left = row_left
        self.row_right = row_right
        self.col_top = col_top
        self.col_bottom = col_bottom
        self.position = complex(row_left[1], 1)
        self.heading = 1

    def left(self):
        self.heading *= -1j

    def right(self):
        self.heading *= 1j

    def _fwd(self):
        raise NotImplementedError

    def fwd(self, num_steps):
        for _ in range(num_steps):
            if not self._fwd():
                break

    def move(self, path):
        for movement in path:
            if movement == 'R':
                self.right()
            elif movement == 'L':
                self.left()
            else:
                self.fwd(movement)

    def pwd(self):
        col, row = self.position.real, self.position.imag
        heading = heading_translations[self.heading]
        return 1_000 * row + 4 * col + heading


class FlatBoard(Board):
    def _fwd(self):
        new_pos = self.position + self.heading

        col, row = new_pos.real, new_pos.imag
        if self.heading == 1:
            if col > self.row_right[row]:
                col = self.row_left[row]
        elif self.heading == -1:
            if col < self.row_left[row]:
                col = self.row_right[row]
        elif self.heading == 1j:
            if row > self.col_bottom[col]:
                row = self.col_top[col]
        elif self.heading == -1j:
            if row < self.col_top[col]:
                row = self.col_bottom[col]
        new_pos = complex(col, row)

        if new_pos in self.walls:
            return False
        self.position = new_pos
        return True


class CubeBoard(Board):
    def __init__(self, walls, row_left, row_right, col_top, col_bottom):
        super().__init__(walls, row_left, row_right, col_top, col_bottom)
        self.sides = test_sides if test else sides
        self.mappings = test_mappings if test else mappings
        self.side = 1
        self.side_len = self.sides[1]['bottom'] - self.sides[1]['top'] + 1

    def map(self, row, col, edge):
        new_side, new_edge, invert = self.mappings[self.side][edge].values()
        if edge in ('top', 'bottom'):
            relative_pos = col - self.sides[self.side]['left']
        else:
            relative_pos = row - self.sides[self.side]['top']

        if invert:
            relative_pos = self.side_len - relative_pos - 1

        if new_edge == 'top':
            new_pos = complex(self.sides[new_side]['left'] + relative_pos, self.sides[new_side]['top'])
            new_heading = 1j
        elif new_edge == 'bottom':
            new_pos = complex(self.sides[new_side]['left'] + relative_pos, self.sides[new_side]['bottom'])
            new_heading = -1j
        elif new_edge == 'left':
            new_pos = complex(self.sides[new_side]['left'], self.sides[new_side]['top'] + relative_pos)
            new_heading = 1
        elif new_edge == 'right':
            new_pos = complex(self.sides[new_side]['right'] , self.sides[new_side]['top'] + relative_pos)
            new_heading = -1

        return new_pos, new_heading, new_side

    def _fwd(self):
        new_pos = self.position + self.heading
        new_heading = self.heading
        new_side = self.side

        col, row = new_pos.real, new_pos.imag
        if self.heading == 1:
            if col > self.sides[self.side]['right']:
                new_pos, new_heading, new_side = self.map(row, col, 'right')
        elif self.heading == -1:
            if col < self.sides[self.side]['left']:
                new_pos, new_heading, new_side = self.map(row, col, 'left')
        elif self.heading == 1j:
            if row > self.sides[self.side]['bottom']:
                new_pos, new_heading, new_side = self.map(row, col, 'bottom')
        elif self.heading == -1j:
            if row < self.sides[self.side]['top']:
                new_pos, new_heading, new_side = self.map(row, col, 'top')

        if new_pos in self.walls:
            return False
        self.position = new_pos
        self.heading = new_heading
        self.side = new_side
        return True


def parse_path(line):
    n = 0
    for c in line:
        if c in 'RL':
            if n:
                yield n
                n = 0
            yield c
            continue
        n *= 10
        n += int(c)
    if n:
        yield n


def read_data():
    filename = f'puzzle22{"-test" if test else ""}.in'
    walls = set()
    row_left, row_right, col_top, col_bottom = {}, {}, {}, {}
    with open(filename, 'r') as f:
        row = 0
        while (line := next(f).rstrip()):
            row += 1
            for col, c in enumerate(line, start=1):
                if c not in '.#':
                    continue
                if row not in row_left:
                    row_left[row] = col
                row_right[row] = col
                if col not in col_top:
                    col_top[col] = row
                col_bottom[col] = row
                if c == '#':
                    walls.add(complex(col, row))
        path = tuple(parse_path(next(f).strip()))
    return walls, row_left, row_right, col_top, col_bottom, path


def part_1():
    *board_info, path = read_data()
    board = FlatBoard(*board_info)
    board.move(path)
    return board.pwd()


def part_2():
    *board_info, path = read_data()
    board = CubeBoard(*board_info)
    board.move(path)
    return board.pwd()
