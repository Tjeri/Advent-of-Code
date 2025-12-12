from aoc.coord2d.point import Point
from aoc.input import read_split_input


class Shape:
    id: int
    points: list[Point]
    width: int
    height: int

    def __init__(self, block: list[str]) -> None:
        self.id = int(block[0][:-1])
        self.points = []
        for y, line in enumerate(block[1:]):
            self.points += [Point(x, y) for x, char in enumerate(line) if char == '#']
        self.width = max(self.points, key=lambda point: point.x).x + 1
        self.height = max(self.points, key=lambda point: point.y).y + 1


class Area:
    size: tuple[int, int]
    expected: list[int]

    def __init__(self, line: str) -> None:
        size = line[:line.index(':')].split('x')
        self.size = (int(size[0]), int(size[1]))
        self.expected = list(map(int, line[line.index(':') + 2:].split(' ')))

    def fits_very_naive(self, shapes: dict[int, Shape]) -> bool:
        total = 0
        for shape_id, amount in enumerate(self.expected):
            shape = shapes[shape_id]
            total += amount * len(shape.points)
        return total < self.size[0] * self.size[1]


_blocks = read_split_input(True)
_shapes = {_shape.id: _shape for _shape in [Shape(_block) for _block in _blocks[:-1]]}
part1_naive = 0
for _line in _blocks[-1]:
    if Area(_line).fits_very_naive(_shapes):
        part1_naive += 1
print(f'Part 1 (naive): {part1_naive}')
