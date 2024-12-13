import z4
from parse import parse

from aoc.input import read_split_input


def solve(ax, ay, bx, by, px, py) -> int:
    for a in range(101):
        for b in range(101):
            if a * ax + b * bx == px and a * ay + b * by == py:
                return 3 * a + b
    return 0


def solve2_naive(ax, ay, bx, by, px, py) -> int:
    px += 10_000_000_000_000
    py += 10_000_000_000_000
    b_start = min(px // bx, py // by)
    a_end = min(px // ax, py // ay)
    b = b_start
    a = 0
    while a <= a_end:
        rx = a * ax + b * bx
        ry = a * ay + b * by
        if rx == px and ry == py:
            return 3 * a + b
        aold = a
        a = max((px - b * bx) // ax, (py - b * by) // ay)
        if aold == a:
            break
        rx = a * ax + b * bx
        ry = a * ay + b * by
        if rx == px and ry == py:
            return 3 * a + b
        bold = b
        b = min((px - a * ax) // bx, (py - a * ay) // by)
        if bold == b:
            break
        rx = a * ax + b * bx
        ry = a * ay + b * by
        if rx == px and ry == py:
            return 3 * a + b
    for da in range(-1, 2):
        for db in range(-1, 2):
            rx = (a+da) * ax + (b+db) * bx
            ry = (a+da) * ay + (b+db) * by
            if rx == px and ry == py:
                return 3 * (a+da) + (b+db)
    return 0


def solve2_solver(ax, ay, bx, by, px, py) -> int:
    px += 10_000_000_000_000
    py += 10_000_000_000_000
    a, b = z4.Ints('a b')
    best = None
    for solution in z4.find_all_solutions([a * ax + b * bx == px, a * ay + b * by == py]):
        score = 3 * solution.get_interp(a).as_long() + solution.get_interp(b).as_long()
        if best is None or score < best:
            best = score
    if best is None:
        return 0
    return best


def solve2_maths(ax, ay, bx, by, px, py) -> int:
    px += 10_000_000_000_000
    py += 10_000_000_000_000
    b = (px * ay - py * ax) / (bx * ay - by * ax)
    if int(b) != b:
        return 0
    a = (px - b * bx) / ax
    if int(a) != a:
        return 0
    return int(3 * a + b)


button_pattern = 'Button {:l}: X+{x:d}, Y+{y:d}'
prize_pattern = 'Prize: X={x:d}, Y={y:d}'
_blocks = read_split_input(True)
part1 = 0
part2_solver = 0
part2_search = 0
part2_maths = 0
for block in _blocks:
    _a = parse(button_pattern, block[0], evaluate_result=int)
    _b = parse(button_pattern, block[1], evaluate_result=int)
    prize = parse(prize_pattern, block[2], evaluate_result=int)
    part1 += solve(_a.named['x'], _a.named['y'], _b.named['x'], _b.named['y'], prize.named['x'], prize.named['y'])
    part2_solver += solve2_solver(_a.named['x'], _a.named['y'], _b.named['x'], _b.named['y'], prize.named['x'], prize.named['y'])
    part2_search += solve2_naive(_a.named['x'], _a.named['y'], _b.named['x'], _b.named['y'], prize.named['x'], prize.named['y'])
    part2_maths += solve2_maths(_a.named['x'], _a.named['y'], _b.named['x'], _b.named['y'], prize.named['x'], prize.named['y'])

print('Part 1:', part1)
print('Part 2 - solver:', part2_solver)
print('Part 2 - search:', part2_search)
print('Part 2 - maths :', part2_maths)
