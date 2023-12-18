from __future__ import annotations

import re

from aoc.input import read_input


def HASH(string: str) -> int:
    value = 0
    for char in string:
        value += ord(char)
        value *= 17
        value %= 256
    return value


class HASHMAP:
    boxes: list[list[tuple[str, int]]]

    def __init__(self) -> None:
        self.boxes = [[] for _ in range(256)]

    @property
    def focusing_power(self) -> int:
        result = 0
        for i in range(256):
            for j, (_, value) in enumerate(self.boxes[i]):
                result += (i + 1) * (j + 1) * value
        return result

    def add(self, label: str, value: int) -> None:
        box = self.boxes[HASH(label)]
        for i, (_label, _value) in enumerate(box):
            if _label == label:
                box[i] = (label, value)
                return
        box.append((label, value))

    def remove(self, label: str) -> None:
        box = self.boxes[HASH(label)]
        for i, (_label, _) in enumerate(box):
            if _label == label:
                box.pop(i)
                break


def part2(steps: list[str]):
    hashmap = HASHMAP()
    for step in steps:
        label, value = re.split('[-=]', step)
        if '=' in step:
            hashmap.add(label, int(value))
        else:
            hashmap.remove(label)
    return hashmap.focusing_power


_lines = read_input(True)
print(f'Part 1: {sum(HASH(part) for part in _lines[0].split(","))}')
print(f'Part 2: {part2(_lines[0].split(","))}')
