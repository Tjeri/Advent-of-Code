from functools import cache

from aoc.input import read_split_input

@cache
def is_possible(string: str) -> bool:
    if string == '':
        return True
    for option in options:
        if string.startswith(option) and is_possible(string[len(option):]):
            return True
    return False

@cache
def get_combinations(string: str) -> int:
    if string == '':
        return 1
    result = 0
    for option in options:
        if string.startswith(option):
            result += get_combinations(string[len(option):])
    return result


_blocks = read_split_input(True)
options = _blocks[0][0].split(', ')
part1 = 0
part2 = 0
for i, line in enumerate(_blocks[1]):
    if is_possible(line):
        part1 += 1
    part2 += get_combinations(line)
print('Part 1:', part1)
print('Part 2:', part2)
