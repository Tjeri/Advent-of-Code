import sys
sys.path.insert(0, '../aoc')

from aoc.input import read_split_input

_blocks = read_split_input(True)
rules = dict()
for line in _blocks[0]:
    x, y = line.split('|')
    rules.setdefault(y, list()).append(x)

part1 = 0
for line in _blocks[1]:
    pages = line.split(',')
    history = set()
    for page in pages:
        check = [p for p in rules.get(page, []) if p in pages]
        if page in rules and any(p not in history for p in check):
            break
        history.add(page)
    else:
        part1 += int(pages[len(pages) // 2])
print('Part 1:', part1)

rules = dict()
for line in _blocks[0]:
    x, y = line.split('|')
    rules.setdefault(x, list()).append(y)
part2 = 0
for line in _blocks[1]:
    pages = line.split(',')
    new_pages = []
    for page in pages:
        new_index = len(new_pages)
        check = [p for p in rules.get(page, []) if p in pages]
        for c in check:
            if c in new_pages[:new_index]:
                new_index = min(new_index, new_pages.index(c))
        new_pages.insert(new_index, page)
    if pages != new_pages:
        part2 += int(new_pages[len(new_pages) // 2])
print('Part 2:', part2)

