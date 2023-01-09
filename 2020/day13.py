import itertools

from aoc.input import read_input
from aoc.maths.chinese_remainder import solve_chinese_remainder_theorem


def calculate_part1(earliest_departure, busses: list[int]) -> int:
    shortest_wait = max(busses)
    part1 = 0
    for bus in busses:
        if bus == 0:
            continue
        waiting = bus - earliest_departure % bus
        if waiting < shortest_wait:
            shortest_wait = waiting
            part1 = waiting * bus
    return part1


def calculate_part2_slow(busses: list[int]) -> int:
    ordered: list[tuple[int, int]] = [bus for bus in enumerate(busses) if bus[1] != 0]
    ordered.sort(key=lambda x: x[1], reverse=True)
    first, others = ordered[0], ordered[1:]
    for t in itertools.count(first[1] - first[0], first[1]):
        for index, bus in others:
            if (t + index) % bus != 0:
                break
        else:
            return t


def calculate_part2_fast(busses: list[int]) -> int:
    prepare = [((bus - i) % bus, bus) for i, bus in enumerate(busses) if bus > 0]
    return solve_chinese_remainder_theorem(prepare)


_lines = read_input()
_busses = [int(_id) if _id != 'x' else 0 for _id in _lines[1].split(',')]

print(f'Part 1: {calculate_part1(int(_lines[0]), _busses)}')
print(f'Part 2: {calculate_part2_fast(_busses)}')
print(f'Part 2 (slow): {calculate_part2_slow(_busses)}')
