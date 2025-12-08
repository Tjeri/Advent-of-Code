import operator
from functools import reduce

from aoc.coord3d.point import Point3D
from aoc.input import read_input


def parse_junctions(lines: list[str]) -> list[Point3D]:
    return [Point3D(*map(int, line.split(','))) for line in lines]


def calc_distances(junctions: list[Point3D]) -> list[tuple[float, Point3D, Point3D]]:
    distances = []
    for i, junction in enumerate(junctions):
        for junction2 in junctions[i + 1:]:
            distances.append((junction.euclidean_distance(junction2), junction, junction2))
    distances.sort(key=lambda tup: tup[0])
    return distances


def add_to_cluster(connection: tuple[Point3D, Point3D], clusters: list[set[Point3D]]) -> None:
    for i, cluster in enumerate(clusters):
        if any(junction in cluster for junction in connection):
            cluster.update(connection)
            for j, other in enumerate(clusters[i + 1:]):
                if any(junction in other for junction in connection):
                    cluster.update(other)
                    clusters.pop(i + j + 1)
                    break
            break
    else:
        clusters.append({*connection})


def part1(connections: list[tuple[Point3D, Point3D]]) -> int:
    clusters: list[set[Point3D]] = []
    for connection in connections:
        add_to_cluster(connection, clusters)
    sizes = [len(cluster) for cluster in clusters]
    sizes.sort(reverse=True)
    return reduce(operator.mul, sizes[:3])


def part2(connections: list[tuple[Point3D, Point3D]], junctions: int) -> int:
    clusters: list[set[Point3D]] = []
    for connection in connections:
        add_to_cluster(connection, clusters)
        if len(clusters) == 1 and len(clusters[0]) == junctions:
            return connection[0].x * connection[1].x
    return -1


_lines = read_input(True)
_junctions = parse_junctions(_lines)
_distances = calc_distances(_junctions)
print(f'Part 1: {part1([(a, b) for (_, a, b) in _distances[:1000]])}')
print(f'Part 2: {part2([(a, b) for (_, a, b) in _distances], len(_junctions))}')
