from __future__ import annotations

from dataclasses import dataclass
from operator import add, sub, mul, floordiv, eq
from typing import Optional


test = False


def none_aware(f):
    def inner(left, right):
        if left is None or right is None:
            return None
        return f(left, right)
    return inner


ops = {
    '+': none_aware(add),
    '-': none_aware(sub),
    '*': none_aware(mul),
    '/': none_aware(floordiv),
    '=': none_aware(eq)
}


@dataclass
class Node:
    _value: Optional[int] = None
    left: Optional[Node] = None
    right: Optional[Node] = None
    opname: Optional[string] = None
    op: Optional[Callable] = None

    @property
    def value(self):
        if self._value is None and self.op is not None:
            self._value = self.op(self.left.value, self.right.value)
        return self._value

    def set_target(self, target):
        if self.opname is None:
            self._value = target
            return

        self._value = target
        fixed, calc = (self.left, self.right) if self.right._value is None else (self.right, self.left)
        if self.opname == '=':  # assuming target == True
            calc.set_target(fixed._value)
        elif self.opname == '+':
            calc.set_target(target - fixed._value)
        elif self.opname == '*':
            calc.set_target(target // fixed._value)
        elif self.opname == '-':
            if calc is self.left:
                calc.set_target(target + fixed._value)
            else:
                calc.set_target(fixed._value - target)
        elif self.opname == '/':
            if calc is self.left:
                calc.set_target(target * fixed._value)
            else:
                calc.set_target(fixed._value // target)
        else:
            raise ValueError('Unknown operator', self.op)


def read_data(part=1):
    filename = f'puzzle21{"-test" if test else ""}.in'
    monkeys = {}
    with open(filename, 'r') as f:
        for line in f:
            name, spec = line.strip().split(': ')
            tokens = spec.split()
            if len(tokens) == 1:
                monkeys[name] = Node(_value=int(spec))
                continue
            left, op, right = tokens
            monkeys[name] = Node(left=left, right=right, opname=op, op=ops[op])

    for monkey in monkeys.values():
        if monkey.left is not None:
            monkey.left = monkeys[monkey.left]
            monkey.right = monkeys[monkey.right]

    if part == 2:
        monkeys['root'].opname = '='
        monkeys['root'].op = ops['=']
        monkeys['humn']._value = None

    return monkeys


def part_1():
    monkeys = read_data()
    root = monkeys['root']
    return root.value


def part_2():
    monkeys = read_data(part=2)
    root = monkeys['root']
    root.value
    root.set_target(True)
    return monkeys['humn'].value
