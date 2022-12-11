from math import prod


test = False


def divisible_by(n):
    def inner(x):
        return x % n == 0
    return inner


class ModItem:
    def __init__(self, mods, item):
        self.mods = {mod: item % mod for mod in mods}

    def __add__(self, other):
        for mod in self.mods:
            self.mods[mod] = (self.mods[mod] + other) % mod
        return self

    def __mul__(self, other):
        if isinstance(other, ModItem):
            for mod in self.mods:
                # (a * b) % m = ((a % m) * (b % m)) % m, but here a % m == a and b % m == b by construction
                self.mods[mod] = (self.mods[mod] * other.mods[mod]) % mod
        else:
            for mod in self.mods:
                # (a * b) % m = ((a % m) * (b % m)) % m, but here a % m == a by construction
                self.mods[mod] = (self.mods[mod] * (other % mod)) % mod
        return self


    def __mod__(self, mod):
        return self.mods[mod]


class Monkey:
    from_id = {}

    def __init__(self, spec):
        self.parse(spec)
        self.inspections = 0
        Monkey.from_id[self.id] = self

    def parse(self, spec):
        self.id = int(spec[0].strip().split()[1][:-1])
        self.items = [int(n) for n in spec[1].split(':')[1].strip().split(', ')]
        operation = spec[2].split('=')[1].strip()
        self._operation = eval(f'lambda old: {operation}')
        self._test_number = int(spec[3].strip().split()[-1])
        self._test = divisible_by(self._test_number)
        self._target_true = int(spec[4].strip().split()[-1])
        self._target_false = int(spec[5].strip().split()[-1])

    def inspect(self, item):
        self.inspections += 1
        return self._operation(item) // 3

    def select_target(self, item):
        return Monkey.from_id[self._target_true if self._test(item) else self._target_false]

    def turn(self):
        for item in self.items:
            new_item = self.inspect(item)
            target = self.select_target(new_item)
            self.throw(new_item, target)
        self.items = []

    def throw(self, item, target):
        target.catch(item)

    def catch(self, item):
        self.items.append(item)


class ModMonkey(Monkey):
    mods = []

    def __init__(self, spec):
        super().__init__(spec)
        ModMonkey.mods.append(self._test_number)

    def convert_items(self):
        self.items = [ModItem(ModMonkey.mods, item) for item in self.items]

    def inspect(self, item):
        self.inspections += 1
        return self._operation(item)


def read_data(monkey_type):
    filename = f'puzzle11{"-test" if test else ""}.in'
    monkeys = []
    with open(filename, 'r') as f:
        while True:
            spec = [next(f), next(f), next(f), next(f), next(f), next(f)]
            monkeys.append(monkey_type(spec))
            try:
                next(f)
            except StopIteration:
                break
    return monkeys


def part_1():
    monkeys = read_data(monkey_type=Monkey)
    for _ in range(20):
        for monkey in monkeys:
            monkey.turn()
    monkey_business = prod(sorted(monkey.inspections for monkey in monkeys)[-2:])
    return monkey_business


def part_2():
    monkeys = read_data(monkey_type=ModMonkey)
    for monkey in monkeys:
        monkey.convert_items()
    for _ in range(10_000):
        for monkey in monkeys:
            monkey.turn()
    monkey_business = prod(sorted(monkey.inspections for monkey in monkeys)[-2:])
    return monkey_business
