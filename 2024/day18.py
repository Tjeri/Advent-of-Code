from aoc.coord2d.point import Point
from aoc.coord2d.rect import Rect
from aoc.input import read_input
from aoc.pathfinding2.a_star import dijkstra

def part1(points: list[Point]) -> float:
    def neighbors(point) -> dict[Point, float]:
        return {neighbor: 1 for neighbor in point.get_direct_neighbors() if neighbor in size and neighbor not in walls}

    start = Point(0, 0)
    goal = Point(width - 1, height - 1)
    size = Rect(start, goal)
    walls = set(points[:take])
    return dijkstra(start, lambda x: x == goal, neighbors)[0]


def part2(points: list[Point]) -> Point:
    def neighbors(of_point) -> dict[Point, float]:
        return {neighbor: 1 for neighbor in of_point.get_direct_neighbors() if neighbor in size and neighbor not in walls}

    start = Point(0, 0)
    goal = Point(width - 1, height - 1)
    size = Rect(start, goal)
    walls = set(points[:take])
    for point in points[take:]:
        walls.add(point)
        if len(dijkstra(start, lambda x: x == goal, neighbors)[1]) == 0:
            return point



real_input = True
_lines = read_input(real_input)
width, height = (71, 71) if real_input else (7, 7)
take = 1024 if real_input else 12
_points = []
for _line in _lines:
    _points.append(Point(*map(int, _line.split(','))))
print(part1(_points))
print(part2(_points))
