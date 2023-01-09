from aoc.hyper_coord.point import HyperPoint
from aoc.hyper_coord.rect import HyperRect
from aoc.input import read_input


class ConwayCubes:
    hypercubes: set[HyperPoint]
    dimensions: int

    def __init__(self, lines: list[str], dimensions: int) -> None:
        self.hypercubes = set()
        self.dimensions = dimensions
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == '#':
                    self.hypercubes.add(HyperPoint(x, y, *[0 for _ in range(dimensions - 2)]))

    def simulate_turn(self):
        edge = HyperPoint.create_uniform(1, self.dimensions)
        field_to_check = HyperRect(HyperPoint.create_uniform(0, self.dimensions),
                                   HyperPoint.create_uniform(0, self.dimensions))
        for hypercube in self.hypercubes:
            field_to_check.update(hypercube - edge)
            field_to_check.update(hypercube + edge)

        new_hypercubes = set()
        for hypercube in field_to_check.all_points:
            neighbors = len([neighbor for neighbor in hypercube.all_neighbors if neighbor in self.hypercubes])
            if hypercube in self.hypercubes and 2 <= neighbors <= 3:
                new_hypercubes.add(hypercube)
            elif hypercube not in self.hypercubes and neighbors == 3:
                new_hypercubes.add(hypercube)
        self.hypercubes = new_hypercubes


_lines = read_input()

game3d = ConwayCubes(_lines, 3)
for _ in range(6):
    game3d.simulate_turn()
print(f'Part 1: {len(game3d.hypercubes)}')

game4d = ConwayCubes(_lines, 4)
for _ in range(6):
    game4d.simulate_turn()
print(f'Part 2: {len(game4d.hypercubes)}')
