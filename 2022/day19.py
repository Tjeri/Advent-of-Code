from __future__ import annotations

from dataclasses import dataclass

from parse import *
from tools.parsing import parse_input


@dataclass
class Blueprint:
    id: int
    ore_robot_ore: int
    clay_robot_ore: int
    obsidian_robot_ore: int
    obsidian_robot_clay: int
    geode_robot_ore: int
    geode_robot_obsidian: int

    @property
    def max_ore_cost(self) -> int:
        return max(self.ore_robot_ore, self.clay_robot_ore, self.obsidian_robot_ore, self.geode_robot_ore)

    @staticmethod
    def from_line(line: str) -> Blueprint:
        pattern = 'Blueprint {:d}: ' \
                  'Each ore robot costs {:d} ore. ' \
                  'Each clay robot costs {:d} ore. ' \
                  'Each obsidian robot costs {:d} ore and {:d} clay. ' \
                  'Each geode robot costs {:d} ore and {:d} obsidian.'
        return Blueprint(*parse(pattern, line.strip()))


@dataclass
class Situation:
    blueprint: Blueprint

    time_left: int
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0

    ore_robots: int = 1
    clay_robots: int = 0
    obsidian_robots: int = 0
    geode_robots: int = 0

    prev: Situation | None = None

    @property
    def tuple(self) -> tuple[int, ...]:
        return (
            self.ore, self.clay, self.obsidian, self.geode,
            self.ore_robots, self.clay_robots, self.obsidian_robots, self.geode_robots
        )

    @property
    def optimistic_geodes(self) -> int:
        result = self.geode
        robots = self.geode_robots
        for _ in range(self.time_left):
            result += robots
            robots += 1
        return result

    def _next_params(self) -> dict[str, int]:
        return {
            'blueprint': self.blueprint,
            'time_left': self.time_left - 1,
            'ore': self.ore + self.ore_robots,
            'clay': self.clay + self.clay_robots,
            'obsidian': self.obsidian + self.obsidian_robots,
            'geode': self.geode + self.geode_robots,
            'ore_robots': self.ore_robots,
            'clay_robots': self.clay_robots,
            'obsidian_robots': self.obsidian_robots,
            'geode_robots': self.geode_robots,
            'prev': self
        }

    def possible_next_situations(self) -> list[Situation]:
        result: list[Situation] = [self.collect()]
        if self.time_left == 1:
            return result
        if self.can_build_geode_robot():
            result.append(self.build_geode_robot())
            # return [self.build_geode_robot()]
        if self.can_build_obsidian_robot():
            result.append(self.build_obsidian_robot())
            # return [self.build_obsidian_robot(), self.collect()]
        # result: list[Situation] = [self.collect()]
        if self.can_build_ore_robot():
            result.append(self.build_ore_robot())
        if self.can_build_clay_robot():
            result.append(self.build_clay_robot())
        return result

    def collect(self) -> Situation:
        return Situation(**self._next_params())

    def can_build_ore_robot(self) -> bool:
        return self.ore >= self.blueprint.ore_robot_ore and self.ore_robots < self.blueprint.max_ore_cost

    def build_ore_robot(self) -> Situation:
        params = self._next_params()
        params['ore'] -= self.blueprint.ore_robot_ore
        params['ore_robots'] += 1
        if params['ore'] < params['ore_robots'] - 1:
            raise RuntimeError
        return Situation(**params)

    def can_build_clay_robot(self) -> bool:
        return self.ore >= self.blueprint.clay_robot_ore and self.clay_robots < self.blueprint.obsidian_robot_clay

    def build_clay_robot(self) -> Situation:
        params = self._next_params()
        params['ore'] -= self.blueprint.clay_robot_ore
        params['clay_robots'] += 1
        if params['ore'] < params['ore_robots']:
            raise RuntimeError
        return Situation(**params)

    def can_build_obsidian_robot(self) -> bool:
        return self.clay_robots > 0 \
            and self.clay >= self.blueprint.obsidian_robot_clay \
            and self.ore >= self.blueprint.obsidian_robot_ore \
            and self.obsidian_robots < self.blueprint.geode_robot_obsidian

    def build_obsidian_robot(self) -> Situation:
        params = self._next_params()
        params['ore'] -= self.blueprint.obsidian_robot_ore
        params['clay'] -= self.blueprint.obsidian_robot_clay
        params['obsidian_robots'] += 1
        if params['ore'] < params['ore_robots']:
            raise RuntimeError
        if params['clay'] < params['clay_robots']:
            raise RuntimeError
        return Situation(**params)

    def can_build_geode_robot(self) -> bool:
        return self.obsidian_robots > 0 \
            and self.obsidian >= self.blueprint.geode_robot_obsidian \
            and self.ore >= self.blueprint.geode_robot_ore

    def build_geode_robot(self) -> Situation:
        params = self._next_params()
        params['ore'] -= self.blueprint.geode_robot_ore
        params['obsidian'] -= self.blueprint.geode_robot_obsidian
        params['geode_robots'] += 1
        if params['ore'] < params['ore_robots']:
            raise RuntimeError
        if params['obsidian'] < params['obsidian_robots']:
            raise RuntimeError
        return Situation(**params)


def find_max_geodes(blueprint: Blueprint, days: int) -> int:
    situations: list[Situation] = [Situation(blueprint, days)]
    next_situations: list[Situation] = list()
    seen: set[tuple[int, ...]] = set()
    for _ in range(days):
        current_best: int = 0
        for situation in situations:
            options = situation.possible_next_situations()
            for next_situation in options:
                if next_situation.tuple in seen:
                    continue
                seen.add(next_situation.tuple)
                optimistic = next_situation.optimistic_geodes
                if optimistic > current_best:
                    current_best = optimistic
                if optimistic >= current_best:
                    next_situations.append(next_situation)
        situations = next_situations
        next_situations = list()
    return max(_situation.geode for _situation in situations)


def part1() -> int:
    quality_levels = 0
    for _blueprint in blueprints:
        quality_levels += _blueprint.id * find_max_geodes(_blueprint, 24)
    return quality_levels


def part2() -> int:
    geodes = 1
    for _blueprint in blueprints:
        if _blueprint.id > 3:
            break
        geodes *= find_max_geodes(_blueprint, 32)
    return geodes


blueprints: list[Blueprint] = list()
with open('../data/2022/day19.txt') as file:
    for _line in file.readlines():
        blueprints.append(Blueprint.from_line(_line))

print(f'Part 1: {part1()}')
print(f'Part 2: {part2()}')
