import sys
sys.path.insert(0, '../aoc')

from aoc.input import read_input
import re

pattern1 = re.compile(r'mul\((\d+,\d+)\)')
_lines = read_input(True)
part1 = 0
for line in _lines:
  for mul in pattern1.findall(line):
    a, b = mul.split(',')
    part1 += int(a) * int(b)
print('Part 1:', part1)

pattern2 = re.compile(r'(mul\(\d+,\d+\))|(do\(\))|(don\'t\(\))')
_lines = read_input(True)
enabled = True
part2 = 0
for line in _lines:
  for group in pattern2.findall(line):
    if group[1] == 'do()':
      enabled = True
    elif group[2] == 'don\'t()':
      enabled = False
    elif enabled:
      a, b = pattern1.findall(group[0])[0].split(',')
      part2 += int(a) * int(b)
print('Part 2:', part2)
      
