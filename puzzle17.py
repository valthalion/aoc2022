from collections import deque


test = False


def read_data():
    filename = f'puzzle17{"-test" if test else ""}.in'
    with open(filename, 'r') as f:
        line = next(f).strip()
        moveseq = tuple(1 if c == '>' else -1 for c in line)
    return moveseq


class Piece:
    def __init__(self):
        self.x = 2
        self.y = 4
        self.width = None
        self.height = None
        self.lines = None  # bottom up

    def _slide(self, move):
        self.x += move
        if move > 0:
            for idx in range(self.height):
                self.lines[idx] >>= 1
        else:
            for idx in range(self.height):
                self.lines[idx] <<= 1

    def move(self, move, shaft):
        self.slide(move, shaft)
        stopped = self.drop(shaft)
        return stopped

    def collision(self, shaft):
        if self.y > 0:
            return False
        row = -self.y
        for line in self.lines:
            if line & shaft[row]:
                return True
            row -= 1
            if row < 0:
                break
        return False

    def slide(self, move, shaft):
        if 0 <= self.x + move <= 7 - self.width:  # slide is possible for
            self._slide(move)
            if self.collision(shaft):  # collision wiht a fallen rock
                self._slide(-move)  # revert move

    def drop(self, shaft):
        self.y -= 1
        if self.collision(shaft):
            self.y += 1
            return True
        return False

    def highest(self):
        return self.y + self.height - 1

    def blend_with(self, shaft):
        row = -self.y
        for line in self.lines:
            shaft[row] |= line
            row -= 1


class HorLine(Piece):
    def __init__(self):
        super().__init__()
        self.width = 4
        self.height = 1
        self.lines = [0b0011110]


class Plus(Piece):
    def __init__(self):
        super().__init__()
        self.width = 3
        self.height = 3
        self.lines = [0b0001000,
                      0b0011100,
                      0b0001000]


class Ell(Piece):
    def __init__(self):
        super().__init__()
        self.width = 3
        self.height = 3
        self.lines = [0b0011100,
                      0b0000100,
                      0b0000100]


class VerLine(Piece):
    def __init__(self):
        super().__init__()
        self.width = 1
        self.height = 4
        self.lines = [0b0010000,
                      0b0010000,
                      0b0010000,
                      0b0010000]


class Square(Piece):
    def __init__(self):
        super().__init__()
        self.width = 2
        self.height = 2
        self.lines = [0b0011000,
                      0b0011000]


def piece_sequence():
    while True:
        yield HorLine()
        yield Plus()
        yield Ell()
        yield VerLine()
        yield Square()


def repeat(it):
    while True:
        yield from iter(it)


def move_sequence():
    moveseq = read_data()
    moves_period = len(moveseq)
    return moves_period, repeat(moveseq)


def play_step(shaft, pieces, moves):
    piece = next(pieces)
    while True:
        move = next(moves)
        stopped = piece.move(move, shaft)
        if stopped:
            piece_highest = piece.highest()
            if piece_highest > 0:
                shaft.extendleft([0] * piece_highest)
                piece.y -= piece_highest
            piece.blend_with(shaft)
            return max(0, piece_highest)


def envelope(shaft):
    current = 0
    for line in shaft:
        current |= line
        if current == 0b1111111:
            break
        yield current


def shaft_hash(shaft, depth=17):
    return tuple(shaft)[:depth]
    # return tuple(envelope(shaft))


def play(rounds):
    shaft = deque([0b1111111], maxlen=40)
    highest = 0
    pieces = piece_sequence()
    moves_period, moves = move_sequence()
    iteration = 0
    # cache key = cycle position identifier = (piece type, position in wind cycle, shaft blocks)
    new_shaft = (iteration % 5, iteration % moves_period, shaft_hash(shaft))
    cache = {new_shaft: iteration}
    height_cache = {0: 0}

    while iteration < rounds:
        iteration += 1
        delta = play_step(shaft, pieces, moves)
        highest += delta
        height_cache[iteration] = highest
        new_shaft = (iteration % 5, iteration % moves_period, shaft_hash(shaft))
        if new_shaft in cache:
            # calculate height from cycle
            cycle_end = iteration
            cycle_start = cache[new_shaft]
            cycle_length = cycle_end - cycle_start
            cycle_height = highest - height_cache[cycle_start]
            iterations_left = rounds - iteration
            cycles, iterations_left = divmod(iterations_left, cycle_length)
            highest += cycles * cycle_height
            break
        cache[new_shaft] = iteration
    else:  # no break -> reached iterations without finding a cycle
        return highest

    for _ in range(iterations_left):
        highest += play_step(shaft, pieces, moves)

    return highest


def part_1():
    return play(rounds=2022)


def part_2():
    return play(rounds=1_000_000_000_000)
