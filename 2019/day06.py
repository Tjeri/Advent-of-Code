from aoc.input import read_input


def read_orbits(lines: list[str]) -> dict[str, list[str]]:
    result = {}
    for line in lines:
        base, orbit = line.split(')')
        result.setdefault(base, []).append(orbit)
    return result


def find_overlap(orbits: dict[str, list[str]], origin: str, destination: str) -> str:
    origin_path = find_path(orbits, 'COM', origin)
    destination_path = set(find_path(orbits, 'COM', destination))
    for node in reversed(origin_path):
        if node in destination_path:
            return node
    return 'COM'


def find_path(orbits: dict[str, list[str]], origin: str, destination: str) -> list[str]:
    if origin == destination:
        return [destination]
    children = orbits.get(origin, [])
    for child in children:
        path = find_path(orbits, child, destination)
        if path:
            return [origin] + path
    return []


def count_orbits(orbits: dict[str, list[str]], orbiter: str = 'COM', layer: int = 0) -> int:
    return layer + sum(count_orbits(orbits, child, layer + 1) for child in orbits.get(orbiter, []))


_lines = read_input()
_orbits = read_orbits(_lines)
print(f'Part 1: {count_orbits(_orbits)}')

_overlap = find_overlap(_orbits, 'YOU', 'SAN')
_part2 = len(find_path(_orbits, _overlap, 'YOU')) + len(find_path(_orbits, _overlap, 'SAN')) - 4
print(f'Part 2: {_part2}')
