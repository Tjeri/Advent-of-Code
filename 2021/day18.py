from __future__ import annotations

import json
import operator
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import reduce
from typing import Optional


class Element(ABC):
    parent: Optional[Pair] = None

    def __add__(self, other) -> Pair:
        if not isinstance(other, Element):
            raise ValueError
        new_pair = Pair(self, other)
        self.parent = new_pair
        other.parent = new_pair
        new_pair.reduce()
        return new_pair

    @property
    @abstractmethod
    def magnitude(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def left_value(self) -> Value:
        raise NotImplementedError

    @property
    @abstractmethod
    def right_value(self) -> Value:
        raise NotImplementedError

    def reduce(self) -> None:
        while True:
            if self.explode():
                continue
            if self.split():
                continue
            return

    @abstractmethod
    def explode(self, layer: int = 0) -> bool:
        raise NotImplementedError

    @abstractmethod
    def split(self) -> bool:
        raise NotImplementedError


@dataclass
class Pair(Element):
    left: Element
    right: Element

    def __str__(self) -> str:
        return f'[{self.left}, {self.right}]'

    @property
    def magnitude(self) -> int:
        return 3 * self.left.magnitude + 2 * self.right.magnitude

    @property
    def left_value(self) -> Value:
        return self.left.left_value

    @property
    def right_value(self) -> Value:
        return self.right.right_value

    def bubble_left(self) -> Optional[Pair]:
        if self.parent is None:
            return None
        if self.parent.left is not self:
            return self.parent
        return self.parent.bubble_left()

    def bubble_right(self) -> Optional[Pair]:
        if self.parent is None:
            return None
        if self.parent.right is not self:
            return self.parent
        return self.parent.bubble_right()

    def explode_child(self, child: Pair) -> None:
        if child is self.left:
            self.left = Value(0)
        else:
            self.right = Value(0)

    def explode(self, layer: int = 0) -> bool:
        if layer < 4:
            return self.left.explode(layer + 1) or self.right.explode(layer + 1)
        if not isinstance(self.left, Value) or not isinstance(self.right, Value):
            raise ValueError
        bubble_left = self.bubble_left()
        if bubble_left is not None:
            bubble_left.left.right_value.value += self.left.value
        bubble_right = self.bubble_right()
        if bubble_right is not None:
            bubble_right.right.left_value.value += self.right.value
        self.parent.explode_child(self)
        return True

    def split(self) -> bool:
        if self.left.split():
            if isinstance(self.left, Value):
                self.left = self.left.split_to_pair()
                self.left.parent = self
            return True
        if self.right.split():
            if isinstance(self.right, Value):
                self.right = self.right.split_to_pair()
                self.right.parent = self
            return True
        return False


@dataclass
class Value(Element):
    value: int

    def __str__(self) -> str:
        return f'{self.value}'

    @property
    def magnitude(self) -> int:
        return self.value

    @property
    def left_value(self) -> Value:
        return self

    @property
    def right_value(self) -> Value:
        return self

    def explode(self, layer: int = 0) -> bool:
        return False

    def split(self) -> bool:
        return self.value >= 10

    def split_to_pair(self) -> Pair:
        dm = divmod(self.value, 2)
        left_value = Value(dm[0])
        right_value = Value(dm[0] + dm[1])
        new_pair = Pair(left_value, right_value)
        left_value.parent = new_pair
        right_value.parent = new_pair
        return new_pair


def build_tree(_data) -> Element:
    if isinstance(_data, int):
        return Value(_data)
    pair = Pair(build_tree(_data[0]), build_tree(_data[1]))
    pair.left.parent = pair
    pair.right.parent = pair
    return pair


file_name = '../data/2021/day18.txt'
raw_numbers = []
with open(file_name) as file:
    for line in file.readlines():
        raw_numbers.append(json.loads(line.strip()))

part1 = reduce(operator.add, [build_tree(number) for number in raw_numbers]).magnitude
print(f'Part 1: {part1}')

part2 = 0
for i, number1 in enumerate(raw_numbers[:-1]):
    for j, number2 in enumerate(raw_numbers[i + 1:]):
        magnitude1 = (build_tree(number1) + build_tree(number2)).magnitude
        magnitude2 = (build_tree(number2) + build_tree(number1)).magnitude
        part2 = max(part2, magnitude1, magnitude2)

print(f'Part 2: {part2}')
