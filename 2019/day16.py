import itertools
from typing import Iterator

from aoc.input import read_input
from aoc.utils.list import flatten

base_pattern = [0, 1, 0, -1]


def build_pattern(multiplier: int) -> Iterator[int]:
    pattern = itertools.cycle(flatten([multiplier * [element] for element in base_pattern]))
    next(pattern)
    return pattern


def flawed_frequency_transmission_phase(input_list: list[int]) -> list[int]:
    output_list = []
    for i in range(1, len(input_list) + 1):
        pattern = build_pattern(i)
        output_list.append(abs(sum([next(pattern) * element for element in input_list])) % 10)
    return output_list


def flawed_frequency_transmission(input_list: list[int], phases: int) -> str:
    for _ in range(phases):
        input_list = flawed_frequency_transmission_phase(input_list)
    return ''.join(str(digit) for digit in input_list)


def flawed_frequency_transmission_phase_part2(input_list: list[int]) -> list[int]:
    output_list = [input_list[-1]]
    for i in range(2, len(input_list) + 1):
        output_list.append((input_list[-i] + output_list[-1]) % 10)
    return output_list[::-1]


def flawed_frequency_transmission_part2(input_list: list[int], phases: int) -> str:
    for _ in range(phases):
        input_list = flawed_frequency_transmission_phase_part2(input_list)
    return ''.join(str(digit) for digit in input_list)


_lines = read_input()
_input_list = [int(digit) for digit in _lines[0]]
print(f'Part 1: {flawed_frequency_transmission(_input_list, 100)[:8]}')

_skip_digits = int(_lines[0][:7])
_repeated_input_list = _input_list * 10_000
print(f'Part 2: {flawed_frequency_transmission_part2(_repeated_input_list[_skip_digits:], 100)[:8]}')
