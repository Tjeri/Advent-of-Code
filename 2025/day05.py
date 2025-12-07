import sys
sys.path.append('..')

from aoc.input import read_split_input

def merge_all_ranges(ranges: list[range]) -> list[range]:
    result = ranges
    while True:
        for i, range1 in enumerate(result):
            for j, range2 in enumerate(result[i + 1:]):
                merges = merge_ranges(range1, range2)
                if len(merges) == 2:
                    continue
                result = result[0:i] + result[i + 1:i + j + 1] + result[i + j + 2:] + merges
                break
            else:
                continue
            break
        else:
            break
    return result


def merge_ranges(range1: range, range2: range) -> list[range]:
    if range1.start in range2:
        if range1.stop in range2 or range1.stop ==  range2.stop:
            return [range2]
        return [range(range2.start, range1.stop)]
    if range2.start in range1:
        if range2.stop in range1 or range2.stop == range1.stop:
            return [range1]
        return [range(range1.start, range2.stop)]
    return [range1, range2]

_blocks = read_split_input(True)
_fresh = []
for _line in _blocks[0]:
    _start, _end = _line.split('-')
    _fresh.append(range(int(_start), int(_end) + 1))

part1 = 0
for _available in _blocks[1]:
    ingredient = int(_available)
    for _range in _fresh:
        if ingredient in _range:
            part1 += 1
            break

print(f'Part 1: {part1}')

_fresh = merge_all_ranges(_fresh)
part2 = 0
for _range in _fresh:
    part2 += len(_range)
print(f'Part 2: {part2}')

