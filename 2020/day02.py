from aoc.input import read_input


def count_valid_passwords(lines: list[str]) -> tuple[int, int]:
    valid1 = 0
    valid2 = 0
    for line in lines:
        min_max, char_, password = line.strip().split(' ')
        __min, __max = min_max.split('-')
        _min, _max = int(__min), int(__max)
        char = char_[0]
        if _min <= password.count(char) <= _max:
            valid1 += 1
        _len = len(password)
        if (_min <= _len and password[_min - 1] == char) != (_max <= _len and password[_max - 1] == char):
            valid2 += 1
    return valid1, valid2


part_1, part_2 = count_valid_passwords(read_input())
print(f'Part 1: {part_1}')
print(f'Part 2: {part_2}')
