from __future__ import annotations

import math
from typing import Callable


class Monkey:
    id: int
    items: list[int]
    operation: Callable[[int], int]
    test_divisible: int
    throw_true: int
    throw_false: int

    inspected_items: int = 0

    @staticmethod
    def from_text(*lines: str) -> Monkey:
        monkey = Monkey()
        monkey.id = int(lines[0][7:-1])
        monkey.items = [int(item) for item in lines[1][16:].split(', ')]
        monkey.operation = eval(f'lambda old: {lines[2][17:]}')
        monkey.test_divisible = int(lines[3][19:])
        monkey.throw_true = int(lines[4][25:])
        monkey.throw_false = int(lines[5][26:])
        return monkey

    def take_turn(self) -> None:
        while self.items:
            item = self.items.pop(0)
            # inspect
            self.inspected_items += 1
            if chillness == 1:
                item = self.operation(item) % lmc
            else:
                item = self.operation(item) // chillness
            # throw
            throw_to = self.throw_true if item % self.test_divisible == 0 else self.throw_false
            monkeys[throw_to].catch(item)

    def catch(self, item: int) -> None:
        self.items.append(item)


def read_monkeys() -> None:
    with open(path) as file:
        monkey_lines = list()
        for line in file.readlines():
            line = line.strip()
            if line:
                monkey_lines.append(line)
            else:
                monkey = Monkey.from_text(*monkey_lines)
                monkeys[monkey.id] = monkey
                monkey_lines = list()


def find_monkey_lmc() -> int:
    return math.lcm(*[monkey.test_divisible for monkey in monkeys.values()])


def simulate(turns: int) -> None:
    for turn in range(turns):
        for i in range(len(monkeys)):
            monkey = monkeys[i]
            monkey.take_turn()


def get_monkey_inspections_sorted() -> list[int]:
    return sorted(map(lambda _monkey: _monkey.inspected_items, monkeys.values()), reverse=True)


path = '../data/2022/day11.txt'
chillness = 3
monkeys: dict[int, Monkey] = dict()
lmc: int

read_monkeys()
lmc = find_monkey_lmc()
simulate(20)
sorted_monkeys = get_monkey_inspections_sorted()
print(f'Part 1: {sorted_monkeys[0] * sorted_monkeys[1]}')

chillness = 1
read_monkeys()
simulate(10_000)
sorted_monkeys = get_monkey_inspections_sorted()
print(f'Part 2: {sorted_monkeys[0] * sorted_monkeys[1]}')
