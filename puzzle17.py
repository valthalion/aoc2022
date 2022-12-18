from itertools import repeat


test = False


def read_data():
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

def move_sequence():
    moveseq = read_data()
    while True:
        yield from iter(moveseq)


def part_1():
    shaft = set((x, 0) for x in range(7))
    highest = 0
    pieces = piece_sequence()
    moves = move_sequence()
    for piece_n in range(2022):
        piece = next(pieces)(position=(2, highest + 4))
        while True:
            move = next(moves)
            stopped = piece.move(move, shaft)
            if stopped:
                shaft |= piece.blocks()
                piece_highest = piece.highest()
                if piece_highest > highest:
                    highest = piece_highest
                break
    return highest
