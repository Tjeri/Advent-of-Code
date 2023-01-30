from __future__ import annotations

from typing import Iterable

from aoc.data_structures.linked_list import LinkedListElement, LoopingUniqueLinkedList, UniqueLinkedList
from aoc.input import read_input


class CrabCups:
    cups: list[int]
    index: int = 0
    max: int

    def __init__(self, line: str) -> None:
        self.cups = list(map(int, line))
        self.max = max(self.cups)

    def setup_part_2(self) -> None:
        for cup in range(self.max + 1, 1_000_001):
            self.cups.append(cup)
        self.max = 1_000_000

    @property
    def order(self) -> list[int]:
        index = self.cups.index(1)
        return self.cups[index:] + self.cups[:index]

    @property
    def elements2(self) -> tuple[int, int]:
        index = self.cups.index(1)
        return self.cups[(index + 1) % len(self.cups)], self.cups[(index + 2) % len(self.cups)]

    def simulate(self, moves: int) -> None:
        for i in range(moves):
            if i % 100 == 0:
                print(i)
            self.make_move()

    def make_move(self) -> None:
        value = self.cups[self.index]
        removed_cups = self.pop(self.index + 1), self.pop(self.index + 1), self.pop(self.index + 1)
        destination = self.find_destination(value - 1, removed_cups)
        for cup in reversed(removed_cups):
            self.cups.insert(destination + 1, cup)
        self.index = (self.cups.index(value) + 1) % len(self.cups)

    def pop(self, index: int) -> int:
        if index >= len(self.cups):
            index = 0
        return self.cups.pop(index)

    def find_destination(self, label: int, removed: Iterable[int]) -> int:
        if label <= 0:
            label = self.max
        if label in removed:
            return self.find_destination(label - 1, removed)
        return self.cups.index(label)


class CrabCups2:
    cups: LoopingUniqueLinkedList[int]
    current: LinkedListElement[int]
    max: int

    def __init__(self, line: str) -> None:
        self.cups = LoopingUniqueLinkedList(map(int, line))
        self.current = self.cups.first
        self.max = max(self.cups).value

    def setup_part_2(self) -> None:
        self.cups.extend(range(self.max + 1, 1_000_001))
        self.max = 1_000_000

    @property
    def elements2(self) -> tuple[int, int]:
        one = self.cups.get(1)
        return one.next_element.value, one.next_element.next_element.value

    def simulate(self, moves: int) -> None:
        for i in range(moves):
            if i % 100_000 == 0:
                print(i)
            self.make_move()

    def make_move(self) -> None:
        removed_cups = self.cups.extract_from(self.current.next_element, 3)
        destination = self.find_destination(self.current.value - 1, removed_cups)
        self.cups.insert_list_after(destination, removed_cups, keep_elements=True)
        self.current = self.current.next_element

    def find_destination(self, label: int, removed: UniqueLinkedList[int]) -> LinkedListElement[int]:
        if label <= 0:
            label = self.max
        if label in removed:
            return self.find_destination(label - 1, removed)
        return self.cups.get(label)


_line = read_input(False)[0]
game = CrabCups(_line)
game.simulate(100)
part1 = ''.join(map(str, game.order[1:]))
print(f'Part 1: {part1}')
game = CrabCups2(_line)
game.setup_part_2()
game.simulate(10_000_000)
elements = game.elements2
part2 = elements[0] * elements[1]
print(f'Part 2: {part2}')
