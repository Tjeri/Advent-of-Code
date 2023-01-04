from aoc.input import read_input


def is_sum(number: int, options: list[int]) -> bool:
    for i in range(len(options)):
        for j in range(i + 1, len(options)):
            if options[i] != options[j] and options[i] + options[j] == number:
                return True
    return False


def find_first_invalid_number(preamble: int, numbers: list[int]) -> int:
    for i in range(preamble, len(numbers)):
        if not is_sum(numbers[i], numbers[i - preamble:i]):
            return numbers[i]
    raise ValueError


def solve_xmas(invalid_number: int, numbers: list[int]) -> int:
    for i in range(len(numbers)):
        for j in range(i, len(numbers)):
            current_range = numbers[i:j + 1]
            if sum(current_range) == invalid_number:
                return min(current_range) + max(current_range)
    return 0


_numbers = list(map(int, read_input()))
_invalid_number = find_first_invalid_number(25, _numbers)
print(f'Part 1: {_invalid_number}')
print(f'Part 2: {solve_xmas(_invalid_number, _numbers)}')
