from collections import Counter

from aoc.input import read_input

def part1(paths: dict[str, list[str]]) -> int:
    result = 0
    positions = ['you']
    while True:
        next_positions = []
        for position in positions:
            for next_position in paths[position]:
                if next_position == 'out':
                    result += 1
                else:
                    next_positions.append(next_position)
        if next_positions:
            positions = next_positions
        else:
            break
    return result

def part2(paths: dict[str, list[str]]) -> int:
    result = 0
    positions = Counter([('svr', False, False)])
    while True:
        next_positions = Counter()
        for (position, dac, fft), amount in positions.items():
            for next_position in paths[position]:
                if next_position == 'out':
                    if dac and fft:
                        result += amount
                else:
                    next_positions[(next_position, dac or next_position == 'dac',
                                    fft or next_position == 'fft')] += amount
        if next_positions:
            positions = next_positions
        else:
            break
    return result


_lines = read_input(True)
_paths: dict[str, list[str]] = {}
for _line in _lines:
    _paths[_line[:_line.index(':')]] = _line[_line.index(':') + 2:].split(' ')
print(f'Part 1: {part1(_paths)}')
print(f'Part 2: {part2(_paths)}')
