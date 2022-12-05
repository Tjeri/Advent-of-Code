from __future__ import annotations

A = ord('A')
a = ord('a')


def get_priority(char: str) -> int:
    if char < 'a':
        return ord(char) - A + 27
    else:
        return ord(char) - a + 1


priority = 0
group_priority = 0

group = set()
group_size = 0
with open('../data/2022/day03.txt') as file:
    for line in file.readlines():
        line = line.strip()

        # part 1
        mid = len(line) // 2
        first, second = set(line[0:mid]), set(line[mid:])
        priority += get_priority((first & second).pop())

        # part 2
        if group_size == 0:
            group = set(line)
        else:
            group &= set(line)
        group_size += 1
        if group_size == 3:
            group_priority += get_priority(group.pop())
            group_size = 0

print(f'Part 1: {priority}')
print(f'Part 2: {group_priority}')
