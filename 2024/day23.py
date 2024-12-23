from collections import defaultdict

from aoc.input import read_input


def find_sets_of_3(routes: dict[str, list[str]]) -> set[list[str]]:
    result = set()
    for pc, connections in routes.items():
        for pc2 in connections:
            for pc3 in routes[pc2]:
                if pc != pc3 and pc in routes[pc3]:
                    result.add(list(sorted((pc, pc2, pc3))))
    return result


def explore_sets(pc: str, routes: dict[str, list[str]]) -> list[list[str]]:
    sets = [[pc, pc2] for pc2 in routes[pc]]
    changed = True
    while changed:
        changed = False
        for pcs in sets:
            for pc3 in routes[pcs[-1]]:
                if pc3 in pcs:
                    continue
                pc3_connections = routes[pc3]
                if all(pc in pc3_connections for pc in pcs):
                    pcs.append(pc3)
                    changed = True
    return sets


def find_biggest_set(routes: dict[str, list[str]]) -> list[str]:
    sets = []
    for pc, connections in routes.items():
        sets += explore_sets(pc, routes)
    return max(sets, key=len)


_lines = read_input(True)
_routes = defaultdict(list)
for _line in _lines:
    a, b = _line.split('-')
    _routes[a].append(b)
    _routes[b].append(a)

part1 = len([_set for _set in find_sets_of_3(_routes) if any(_pc for _pc in _set if _pc.startswith('t'))])
print('Part 1:', part1)
part2 = ','.join(sorted(find_biggest_set(_routes)))
print('Part 2:', part2)
