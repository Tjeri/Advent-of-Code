from aoc.input import read_input


def parse_line(line: str) -> list[int]:
    return list(map(int, line.split(' ')))


def extrapolate_forwards(numbers: list[int]) -> int:
    if any(numbers):
        return numbers[-1] + extrapolate_forwards([numbers[i + 1] - number for i, number in enumerate(numbers[:-1])])
    return 0


def extrapolate_backwards(numbers: list[int]) -> int:
    if any(numbers):
        return numbers[0] - extrapolate_backwards([numbers[i + 1] - number for i, number in enumerate(numbers[:-1])])
    return 0


def extrapolate(line: str, forwards: bool) -> int:
    numbers = parse_line(line)
    if forwards:
        return extrapolate_forwards(numbers)
    return extrapolate_backwards(numbers)


def extrapolate_all(lines: list[str], forwards: bool) -> int:
    result = 0
    for line in lines:
        result += extrapolate(line, forwards)
    return result


_lines = read_input(True)
print(f'Part 1: {extrapolate_all(_lines, True)}')
print(f'Part 2: {extrapolate_all(_lines, False)}')
