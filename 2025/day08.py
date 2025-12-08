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


def calc_clusters(connections: list[tuple[Point3D, Point3D]]) -> list[int]:
    clusters: list[set[Point3D]] = []
    for a, b in connections:
        for cluster in clusters:
            if a in cluster or b in cluster:
                cluster.add(a)
                cluster.add(b)
                break
        else:
            clusters.append({a, b})

    while True:
        changed = False
        for i, cluster in enumerate(clusters):
            for j, other in enumerate(clusters[i + 1:]):
                if cluster & other:
                    cluster.update(other)
                    clusters.pop(i + j + 1)
                    changed = True
                    break
        if not changed:
            break
    sizes = [len(cluster) for cluster in clusters]
    sizes.sort(reverse=True)
    return sizes


def part2(connections: list[tuple[Point3D, Point3D]], junctions: int) -> int:
    clusters: list[set[Point3D]] = []
    for a, b in connections:
        for i, cluster in enumerate(clusters):
            if a in cluster or b in cluster:
                cluster.add(a)
                cluster.add(b)
                for j, other in enumerate(clusters[i + 1:]):
                    if a in other or b in other:
                        cluster.update(other)
                        clusters.pop(i + j + 1)
                        break
                break
        else:
            clusters.append({a, b})
        if len(clusters) == 1 and len(clusters[0]) == junctions:
            return a.x * b.x
    return -1


_lines = read_input(True)
_junctions = parse_junctions(_lines)
_distances = calc_distances(_junctions)
_sizes = calc_clusters([(a, b) for (_, a, b) in _distances[:1000]])
print(f'Part 1: {reduce(operator.mul, _sizes[:3])}')
print(f'Part 2: {part2([(a, b) for (_, a, b) in _distances], len(_junctions))}')
