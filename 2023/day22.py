from collections import defaultdict

from parse import parse

from aoc.coord3d.cuboid import Cuboid
from aoc.coord3d.point import Point3D
from aoc.input import read_input

brick_pattern = '{:d},{:d},{:d}~{:d},{:d},{:d}'


def parse_bricks(lines: list[str]) -> list[Cuboid]:
    return [parse_brick(line) for line in lines]


def parse_brick(line: str) -> Cuboid:
    x1, y1, z1, x2, y2, z2 = parse(brick_pattern, line)
    return Cuboid(Point3D(x1, y1, z2), Point3D(x2, y2, z1))


def sort_bricks(bricks: list[Cuboid]) -> None:
    bricks.sort(key=lambda brick: brick.bottom_right.z)


def drop_bricks(bricks: list[Cuboid]) -> None:
    highest = defaultdict(int)
    for brick in bricks:
        peak = max(highest[point] for point in brick.all_points_2d)
        drop = brick.bottom_right.z - peak - 1
        if drop > 0:
            brick.top_left.z -= drop
            brick.bottom_right.z -= drop
        for point in brick.all_points_2d:
            highest[point] = brick.top_left.z


def calculate_support(bricks: list[Cuboid]) -> tuple[dict[int, set[int]], dict[int, set[int]]]:
    supports = defaultdict(set)
    supported_by = defaultdict(set)
    for i, brick in enumerate(bricks):
        for j, other in enumerate(bricks[i + 1:]):
            if bricks_touch_2d(brick, other) and other.bottom_right.z - brick.top_left.z == 1:
                supports[i].add(i + j + 1)
                supported_by[i + j + 1].add(i)
    return supports, supported_by

def bricks_touch_2d(brick: Cuboid, other: Cuboid) -> bool:
    return (brick.top_left.x <= other.bottom_right.x
            and brick.bottom_right.x >= other.top_left.x
            and brick.top_left.y <= other.bottom_right.y
            and brick.bottom_right.y >= other.top_left.y)


def part1(bricks: list[Cuboid], supports: dict[int, set[int]], supported_by: dict[int, set[int]]) -> int:
    disintegrable = 0
    for i in range(len(bricks)):
        for j in supports[i]:
            if len(supported_by[j]) == 1:
                break
        else:
            disintegrable += 1
    return disintegrable


def count_falling(disintegrate: int, supports: dict[int, set[int]], supported_by: dict[int, set[int]],
                  gone: set[int] | None = None) -> int:
    if disintegrate not in supports:
        return 0
    if gone is None:
        gone = {disintegrate}
    falling = set()
    for supported in supports[disintegrate]:
        for support in supported_by[supported]:
            if support != supported_by and support not in gone:
                break
        else:
            falling.add(supported)
    fall = len(falling - gone)
    gone |= falling
    for brick in falling:
        fall += count_falling(brick, supports, supported_by, gone)
    return fall


def part2(bricks: list[Cuboid], supports: dict[int, set[int]], supported_by: dict[int, set[int]]) -> int:
    total = 0
    for i in range(len(bricks)):
        total += count_falling(i, supports, supported_by)
    return total


_lines = read_input(True)
_bricks = parse_bricks(_lines)
sort_bricks(_bricks)
drop_bricks(_bricks)
_supports, _supported_by = calculate_support(_bricks)
print(f'Part 1: {part1(_bricks, _supports, _supported_by)}')
print(f'Part 2: {part2(_bricks, _supports, _supported_by)}')
