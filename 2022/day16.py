from __future__ import annotations

import itertools

from tools.a_star import Node, dijkstra


def read_valves() -> None:
    with open(path) as file:
        for line in file.readlines():
            line = line.strip()
            valve = Valve.from_line(line)
            valves[valve.id] = valve
            if valve.flow_rate > 0:
                to_visit.add(valve.id)


def process_valves() -> None:
    for valve in valves.values():
        valve.add_neighbors()
    for valve_id in [start_valve_id] + list(to_visit):
        distances[valve_id] = dict()
        valve = valves[valve_id]
        for other_id in to_visit:
            other = valves[other_id]
            if other.id == valve_id:
                continue
            distances[valve_id][other.id] = len(dijkstra(valve, other))


class Valve(Node):
    flow_rate: int
    tunnels: list[str]

    def __init__(self, _id: str, flow_rate: int, tunnels: list[str]) -> None:
        super().__init__(_id)
        self.flow_rate = flow_rate
        self.tunnels = tunnels

    def add_neighbors(self) -> None:
        for neighbor_id in self.tunnels:
            self.add_neighbor(valves[neighbor_id])

    @staticmethod
    def from_line(line: str) -> Valve:
        _id = line[6:8]
        flow_rate = int(line[23:line.index(';')])
        tunnels = line[line.index('to valve') + 9:].strip().split(', ')
        return Valve(_id, flow_rate, tunnels)


solved_paths: dict[str, int] = dict()


def find_best_path(pos: str, valve_ids: set[str], minutes_left: int) -> int:
    if minutes_left < 2:
        return 0
    _id = f'{pos}-{",".join(sorted(valve_ids))}-{minutes_left}'
    if _id in solved_paths:
        return solved_paths[_id]
    pressure_released = minutes_left * valves[pos].flow_rate
    if len(valve_ids) == 0:
        solved_paths[_id] = pressure_released
        return pressure_released
    best_solution = 0
    for valve_id in valve_ids:
        result = find_best_path(valve_id, valve_ids - {valve_id}, minutes_left - distances[pos][valve_id])
        if result > best_solution:
            best_solution = result
    pressure_released += best_solution
    solved_paths[_id] = pressure_released
    return pressure_released


def find_best_path_2(pos: str, valve_ids: set[str], minutes_left: int) -> int:
    best_solution = 0
    for combination in itertools.combinations(valve_ids, len(valve_ids) // 2):
        valve_ids_1 = set(combination)
        valve_ids_2 = valve_ids - valve_ids_1
        solution = find_best_path(pos, valve_ids_1, minutes_left)
        solution += find_best_path(pos, valve_ids_2, minutes_left)
        if solution > best_solution:
            best_solution = solution
    return best_solution


start_valve_id = 'AA'
path = '../data/2022/day16.txt'
valves: dict[str, Valve] = dict()
to_visit: set[str] = set()
distances: dict[str, dict[str, int]] = dict()

read_valves()
process_valves()
print(f'Part 1: {find_best_path(start_valve_id, to_visit, 30)}')
print(f'Part 2: {find_best_path_2(start_valve_id, to_visit, 26)}')
