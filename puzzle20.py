from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


test = False


@dataclass(slots=True)
class Node:
    value: int
    nxt: Optional[Node] = None
    prev: Optional[Node] = None


class LList:
    def __init__(self, it):
        self.head = None
        self.nodes = [Node(value) for value in it]
        for pred, succ in zip(self.nodes, self.nodes[1:]):
            pred.nxt, succ.prev = succ, pred
            if pred.value == 0:
                self.head = pred
        if self.head is None and self.nodes[-1] == 0:
            self.head = self.nodes[-1]
        self.nodes[0].prev, self.nodes[-1].nxt = self.nodes[-1], self.nodes[0]

    def insert_after(self, insert_node, node):
        node.prev, node.nxt = insert_node, insert_node.nxt
        node.prev.nxt, node.nxt.prev = node, node

    def fwd(self, node, n):
        if n == 0:
            return node
        for _ in range(n):
            node = node.nxt
        return node

    def move(self, node, n):
        if n == 0:
            return
        node.prev.nxt, node.nxt.prev = node.nxt, node.prev
        insert_node = self.fwd(node.prev, n % (len(self.nodes) - 1))
        self.insert_after(insert_node, node)

    def mix(self):
        for node in self.nodes:
            self.move(node, node.value)

    def coordinates(self):
        cur = self.head
        for _ in range(3):
            cur = self.fwd(cur, 1_000 % len(self.nodes))
            yield cur.value

    def __len__(self):
        return len(self.nodes)

    def __iter__(self):
        head = self.head
        yield head.value
        cur = head.nxt
        while cur is not head:
            yield cur.value
            cur = cur.nxt


def read_data(key=None):
    filename = f'puzzle20{"-test" if test else ""}.in'
    with open(filename, 'r') as f:
        return LList(int(line) for line in f) if key is None else LList(int(line) * key for line in f)


def part_1():
    llist = read_data()
    llist.mix()
    return sum(llist.coordinates())


def part_2():
    llist = read_data(key=811589153)
    for _ in range(10):
        llist.mix()
    return sum(llist.coordinates())
