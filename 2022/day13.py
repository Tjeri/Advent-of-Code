from __future__ import annotations

from functools import cmp_to_key


def compare(left: list | int, right: list | int) -> bool | None:
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return True
        if right < left:
            return False
        return None
    if not isinstance(left, list):
        return compare([left], right)
    if not isinstance(right, list):
        return compare(left, [right])
    for i in range(len(left)):
        if i >= len(right):
            return False
        if (result := compare(left[i], right[i])) is not None:
            return result
    if len(right) > len(left):
        return True
    return None


part_1 = 0
packets = []
with open('../data/2022/day13.txt') as file:
    index = 1
    pair = list()
    for line in file.readlines():
        line = line.strip()
        if line:
            pair.append(eval(line))
            packets.append(eval(line))
            if len(pair) == 2:
                if compare(*pair):
                    part_1 += index
                index += 1
                pair = list()

print(f'Part 1: {part_1}')

packets.append([[2]])
packets.append([[6]])
packets.sort(key=cmp_to_key(lambda left, right: -1 if compare(left, right) else 1))
print(f'Part2: {(packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)}')
