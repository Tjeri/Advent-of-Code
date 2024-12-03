import sys
sys.path.insert(0, '../aoc')

from aoc.input import read_input

def is_safe(levels: list[int]) -> bool:
    last = levels[0]
    if levels[1] == last:
        return False
    increase = (levels[1] - last) > 0
    for level in levels[1:]:
        if level == last:
            return False
        diff = level - last
        if abs(diff) > 3:
            return False
        if (diff > 0) != increase:
            return False
        last = level
    return True

_lines = read_input(True)
reports = [list(map(int, report.split(' '))) for report in _lines] 
part1 = sum(is_safe(levels) for levels in reports)
print('Part 1:', part1)

part2 = 0
for report in reports:
    if is_safe(report):
        part2 += 1
        continue
    for i in range(len(report)):
        if is_safe(report[0:i] + report[i + 1:]):
            part2 += 1
            break
print('Part 2:', part2)
