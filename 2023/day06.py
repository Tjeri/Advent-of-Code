from aoc.input import read_input
import re


def get_possible_records(time: int, best: int):
    beaten = 0
    for i in range(time + 1):
        distance = i * (time - i)
        if distance > best:
            beaten += 1
    return beaten


def part1(lines: list[str]) -> int:
    times = list(map(int, re.split(r' +', lines[0][5:].strip())))
    bests = list(map(int, re.split(r' +', lines[1][9:].strip())))
    races = zip(times, bests)
    result = 1
    for time, best in races:
        result *= get_possible_records(time, best)
    return result


def part2(lines: list[str]) -> int:
    time = int(lines[0][5:].replace(' ', ''))
    best = int(lines[1][9:].replace(' ', ''))
    return get_possible_records(time, best)


_lines = read_input(True)
print(f'Part 1: {part1(_lines)}')
print(f'Part 2: {part2(_lines)}')
