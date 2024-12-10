from aoc.input import read_input
from aoc.coord2d.point import Point


class Map:
    tmap: dict[Point, int] = dict()

    def __init__(self, lines: list[str]) -> None:
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == '.':
                    continue
                self.tmap[Point(x, y)] = int(char)

    def calc_score(self) -> int:
        trailheads: list[Point] = [pos for pos, height in self.tmap.items() if height == 0]
        height = 0
        currents = {pos: {pos} for pos in trailheads}
        while height < 9:
            nexts: dict[Point, set[Point]] = dict()
            height += 1
            for pos, heads in currents.items():
                for neighbor in pos.get_direct_neighbors():
                    if neighbor in self.tmap and self.tmap[neighbor] == height:
                        nexts.setdefault(neighbor, set()).update(heads)
            currents = nexts
        return sum(len(heads) for heads in currents.values())

    def calc_rating(self) -> int:
        trailheads: list[Point] = [pos for pos, height in self.tmap.items() if height == 0]
        height = 0
        currents = {pos: 1 for pos in trailheads}
        while height < 9:
            nexts: dict[Point, int] = dict()
            height += 1
            for pos, score in currents.items():
                for neighbor in pos.get_direct_neighbors():
                    if neighbor in self.tmap and self.tmap[neighbor] == height:
                        nexts.setdefault(neighbor, 0)
                        nexts[neighbor] += score
            currents = nexts
        return sum(currents.values())


_lines = read_input(True)
_map = Map(_lines)
print('Part 1:', _map.calc_score())
print('Part 2:', _map.calc_rating())