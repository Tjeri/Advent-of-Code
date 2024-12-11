from parse import parse
import numpy as np
import z4

from aoc.coord2d.point import Point
from aoc.coord3d.point import Point3D
from aoc.input import read_input

hail_pattern = '{:d}, {:d}, {:d} @ {:d}, {:d}, {:d}'


def parse_hail1(line: str) -> tuple[np.array, np.array]:
    px, py, pz, vx, vy, vz = parse(hail_pattern, line).fixed
    return np.array([px, py]), np.array([vx, vy])


def parse_hail2(line: str) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    px, py, pz, vx, vy, vz = parse(hail_pattern, line).fixed
    return (px, py, pz), (vx, vy, vz)


def part1(lines: list[str], min_value: int, max_value: int) -> int:
    total = 0
    hail = [parse_hail1(line) for line in lines]
    for i, (p1, v1) in enumerate(hail[:-1]):
        for p2, v2 in hail[i + 1:]:
            x, err, rank = np.linalg.lstsq(np.array([v1, -v2]).T, p2 - p1)[:3]
            if any(x <= 0):
                continue
            intersect = p1 + x[0] * v1
            if all(intersect >= min_value) and all(intersect <= max_value):
                total += 1
    return total



def part2(lines: list[str]) -> int:
    solver = z4.Solver()
    x, y, z, vx, vy, vz = z4.Reals('x, y, z, vx, vy, vz')
    hail = [parse_hail2(line) for line in lines]
    t = [z4.Real(f't{i}') for i in range(len(hail))]
    for i, ((_x, _y, _z), (_vx, _vy, _vz)) in enumerate(hail):
        solver.add(x + t[i] * vx == _x + t[i] * _vx)
        solver.add(y + t[i] * vy == _y + t[i] * _vy)
        solver.add(z + t[i] * vz == _z + t[i] * _vz)
    solver.check()
    model = solver.model()
    return model.eval(x + y + z)

_lines = read_input(True)
# print(f'Part 1: {part1(_lines,7, 27)}')
#print(f'Part 1: {part1(_lines, 200_000_000_000_000, 400_000_000_000_000)}')
print(f'Part 2: {part2(_lines)}')
