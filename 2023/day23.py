from collections import defaultdict

from aoc.coord2d.point import Point
from aoc.input import read_input


def parse_map(lines: list[str]) -> tuple[dict[Point, str], Point, Point]:
    trail_map = {}
    start = None
    end = None
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != '#':
                end = Point(x, y)
                if y == 0:
                    start = end
                trail_map[end] = char
    return trail_map, start, end


def parse_graph(trail_map: dict[Point, str], start: Point, end: Point) -> dict[Point, dict[Point, int]]:
    graph = defaultdict(dict)
    visited = {start}
    point = start
    while True:
        if point == end:
            graph[start][end] = len(visited) - 1
            return graph
        neighbors = get_neighbors(trail_map, point)
        filtered = {neighbor for neighbor in neighbors if neighbor not in visited}
        if len(filtered) == 0:
            raise ValueError
        if len(filtered) == 1 and neighbors.count(point) <= 1:
            point = filtered.pop()
            visited.add(point)
            continue
        graph[start][point] = len(visited)
        for neighbor in filtered:
            other = parse_graph(trail_map, neighbor, end)
            node, path = other.pop(neighbor).popitem()
            graph[point][node] = path + 2
            graph.update(other)
        break
    return graph


def get_neighbors(trail_map: dict[Point, str], point: Point) -> list[Point]:
    neighbors = []
    for neighbor in point.get_direct_neighbors():
        if neighbor not in trail_map:
            continue
        tile = trail_map[neighbor]
        if tile == '.':
            neighbors.append(neighbor)
        elif tile == '>':
            neighbors.append(neighbor + Point(1, 0))
        elif tile == '<':
            neighbors.append(neighbor + Point(-1, 0))
        elif tile == '^':
            neighbors.append(neighbor + Point(0, -1))
        elif tile == 'v':
            neighbors.append(neighbor + Point(0, 1))
    return neighbors


def flood_search(graph: dict[Point, dict[Point, int]], start: Point, end: Point,
                 visited: set[Point] | None = None) -> int:
    if start == end:
        return 0
    if visited is None:
        visited = {start}
    result = None
    for neighbor, cost in graph[start].items():
        if neighbor in visited:
            continue
        path = flood_search(graph, neighbor, end, visited | {start})
        if path is None:
            continue
        if result is None:
            result = path + cost
        else:
            result = max(result, path + cost)
    return result


def make_bidi(graph: dict[Point, dict[Point, int]]) -> dict[Point, dict[Point, int]]:
    bidi = defaultdict(dict)
    for point, neighbors in graph.items():
        bidi[point].update(neighbors.copy())
        for neighbor, cost in neighbors.items():
            bidi[neighbor][point] = cost
    return bidi


_lines = read_input(True)
_map, _start, _end = parse_map(_lines)
_graph = parse_graph(_map, _start, _end)
print(f'Part 1: {flood_search(_graph, _start, _end)}')
_bidi_graph = make_bidi(_graph)
print(f'Part 2: {flood_search(_bidi_graph, _start, _end)}')
