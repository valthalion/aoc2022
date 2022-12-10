test = False


class Device:
    def __init__(self):
        self.reset()

    def reset(self):
        self.register = 1

    def noop(self):
        yield self.register

    def addx(self, arg):
        yield self.register
        self.register += arg
        yield self.register

    def load_program(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                cmd, *args = line.strip().split()
                yield cmd, tuple(int(arg) for arg in args)

    def run(self, program):
        yield self.register # in 1st cycle register will always be unmodified
        # Each cmd assumes the first cycle has been output, yields additional cycles for execution
        # then yields the new register value, corresponding to the first cycle of the next cmd
        for cmd, args in program:
            yield from getattr(self, cmd)(*args)

    def draw(self, program, width=40, height=6):
        total_pixels = width * height
        screen = [list('.' * width) for _ in range(height)]
        for pixel, sprite_pos in enumerate(self.run(program)):
            if pixel >= total_pixels:
                break
            row, col = divmod(pixel, width)
            if abs(col - sprite_pos) <= 1:
                screen[row][col] = '#'
        return '\n'.join(''.join(row) for row in screen)


def part_1():
    filename = f'puzzle10{"-test" if test else ""}.in'
    device = Device()
    program = device.load_program(filename)
    signal_strength = 0
    for cycle, register in enumerate(device.run(program), start=1):
        if (cycle - 20) % 40 == 0:
            signal_strength += cycle * register
        if cycle >= 220:
            break
    return signal_strength


def part_2():
    filename = f'puzzle10{"-test" if test else ""}.in'
    device = Device()
    program = device.load_program(filename)
    screen = device.draw(program)
    print(screen)
    return None
