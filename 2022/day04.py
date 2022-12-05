from __future__ import annotations

fully_contained = 0
overlapping = 0
with open('../data/2022/day04.txt') as file:
    for line in file.readlines():
        line = line.strip()
        first, second = line.split(',')
        _fstart, _fend = first.split('-')
        _sstart, _send = second.split('-')
        fstart, fend, sstart, send = int(_fstart), int(_fend), int(_sstart), int(_send)
        if fstart <= sstart and fend >= send:
            fully_contained += 1
        elif fstart >= sstart and fend <= send:
            fully_contained += 1

        if fstart <= sstart <= fend:
            overlapping += 1
        elif fstart <= send <= fend:
            overlapping += 1
        elif sstart <= fstart <= send:
            overlapping += 1
        elif sstart <= fend <= send:
            overlapping += 1

print(f'Part 1: {fully_contained}')
print(f'Part 2: {overlapping}')
