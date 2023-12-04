import re

from aoc.input import read_input

digits1 = {str(d): d for d in range(1, 10)}
digits2 = digits1 | {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}


def solve(lines: list[str], digits: dict[str, int]) -> int:
    result = 0
    for line in lines:
        result += find_number(line, digits)
    return result


def find_number(line: str, digits: dict[str, int]) -> int:
    first_index = len(line)
    last_index = -1
    first_digit = None
    last_digit = None
    for find, digit in digits.items():
        index = line.find(find)
        rindex = line.rfind(find)
        if index >= 0:
            if index < first_index:
                first_index = index
                first_digit = digit
            if rindex > last_index:
                last_index = rindex
                last_digit = digit
    return int(f'{first_digit}{last_digit}')


_lines = read_input(True)

print(f'Part 1: {solve(_lines, digits1)}')
print(f'Part 2: {solve(_lines, digits2)}')
