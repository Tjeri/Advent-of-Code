from functools import cache

from aoc.input import read_input


def parse_line(line: str) -> tuple[str, tuple[int, ...]]:
    records, groups = line.split(' ')
    return records, tuple(map(int, groups.split(',')))


@cache
def find_arrangements(records: str, groups: tuple[int, ...]) -> int:
    if len(groups) == 0:
        return 1
    arrangements = 0
    total_size = sum(groups) + len(groups) - 1
    size = groups[0]
    for i in range(len(records) - total_size + 1):
        if any(records[j] == '#' for j in range(0, i)):
            break
        if len(groups) == 1 and any(records[j] == '#' for j in range(i + size, len(records))):
            continue
        if records[i] == '.':
            continue
        if (all(j < len(records) and records[j] != '.' for j in range(i, i + size))
                and (i + size == len(records) or records[i + size] != '#')
                and (i == 0 or records[i - 1] != '#')):
            arrangements += find_arrangements(records[i + size + 1:], groups[1:])
    return arrangements


def part1(lines: list[str]) -> int:
    result = 0
    for line in lines:
        result += find_arrangements(*parse_line(line))
    return result


def part2(lines: list[str]) -> int:
    result = 0
    for i, line in enumerate(lines):
        records, groups = parse_line(line)
        result += find_arrangements((records + '?') * 4 + records, groups * 5)
    return result


_lines = read_input(True)
print(f'Part 1: {part1(_lines)}')
print(f'Part 2: {part2(_lines)}')
