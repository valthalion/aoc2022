test = True


def read_data():
    global moves_period

    filename = f'puzzle17{"-test" if test else ""}.in'
    with open(filename, 'r') as f:
        line = next(f).strip()
        moveseq = tuple(1 if c == '>' else -1 for c in line)
    return moveseq


class Piece:
    def __init__(self, position):
        self.position = position

    def move(self, move, shaft):
        self.slide(move, shaft)
        stopped = self.drop(shaft)
        return stopped

    def blocks(self, position=None):
        return self._blocks(position if position is not None else self.position)

    def _blocks(self, position):
        return NotImplementedError

    def collision(self, position, shaft):
        for x, y in self.blocks(position=position):
            if not 0 <= x < 7:
                return True
            if (x, y) in shaft:
                return True
        return False

    def slide(self, move, shaft):
        x, y = self.position
        new_position = (x + move, y)
        if not self.collision(new_position, shaft):
            self.position = new_position

    def drop(self, shaft):
        x, y = self.position
        new_position = (x, y - 1)
        if self.collision(new_position, shaft):
            return True
        self.position = new_position
        return False

    def highest(self):
        return max(y for _, y in self.blocks())


class HorLine(Piece):
    def _blocks(self, position):
        x, y = position
        return set((x + dx, y) for dx in range(0, 4))


class Plus(Piece):
    def _blocks(self, position):
        x, y = position
        return {(x + 1, y), *((x + dx, y + 1) for dx in range(3)), (x + 1, y + 2)}


class Ell(Piece):
    def _blocks(self, position):
        x, y = position
        return {*((x + dx, y) for dx in range(3)), (x + 2, y + 1), (x + 2, y + 2)}


class VerLine(Piece):
    def _blocks(self, position):
        x, y = position
        return set((x, y + dy) for dy in range(4))


class Square(Piece):
    def _blocks(self, position):
        x, y = position
        return set((x + dx, y + dy) for dx in range(2) for dy in range(2))


def piece_sequence():
    while True:
        yield HorLine
        yield Plus
        yield Ell
        yield VerLine
        yield Square


def repeat(it):
    while True:
        yield from iter(it)


def move_sequence():
    moveseq = read_data()
    moves_period = len(moveseq)
    return moves_period, repeat(moveseq)


def play_step(shaft, pieces, moves):
    piece = next(pieces)(position=(2, 4))
    while True:
        move = next(moves)
        stopped = piece.move(move, shaft)
        if stopped:
            shaft |= piece.blocks()
            piece_highest = piece.highest()
            if piece_highest > 0:
                shaft = {(x, y - piece_highest) for (x, y) in shaft if y - piece_highest > -40}
                return piece_highest, shaft
            return 0, shaft


def shaft_hash(shaft, depth=15):
    return tuple((x, -y) for y in range(depth) for x in range(7) if (x, -y) in shaft)


def play(rounds):
    shaft = set((x, 0) for x in range(7))
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
        delta, shaft = play_step(shaft, pieces, moves)
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
            height_left = height_cache[cycle_start + iterations_left] - height_cache[cycle_start]
            return highest + cycles * cycle_height + height_left
        cache[new_shaft] = iteration
    return highest


def part_1():
    return play(rounds=2022)


def part_2():
    return play(rounds=1_000_000_000_000)
