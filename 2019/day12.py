from __future__ import annotations

import itertools
import math
from dataclasses import dataclass

from parse import parse

from aoc.coord3d.point import Point3D
from aoc.input import read_input

moon_pattern = '<x={:d}, y={:d}, z={:d}>'


def cmp(a: int, b: int) -> int:
    return (a > b) - (a < b)


@dataclass(unsafe_hash=True)
class State:
    positions: tuple[int, ...]
    velocities: tuple[int, ...]


class Moon:
    position: Point3D
    velocity: Point3D

    def __init__(self, position: Point3D) -> None:
        self.position = position
        self.velocity = Point3D()

    def __str__(self) -> str:
        return f'pos=<x={self.position.x}, y={self.position.y}, z={self.position.z}>, ' \
               f'vel=<x={self.velocity.x}, y={self.velocity.y}, z={self.velocity.z}>'

    @property
    def potential_energy(self) -> int:
        return abs(self.position.x) + abs(self.position.y) + abs(self.position.z)

    @property
    def kinetic_energy(self) -> int:
        return abs(self.velocity.x) + abs(self.velocity.y) + abs(self.velocity.z)

    @property
    def total_energy(self) -> int:
        return self.potential_energy * self.kinetic_energy

    def update_velocity(self, other: Moon) -> None:
        change = Point3D(
            cmp(other.position.x, self.position.x),
            cmp(other.position.y, self.position.y),
            cmp(other.position.z, self.position.z)
        )
        self.velocity += change
        other.velocity -= change

    def move(self) -> None:
        self.position += self.velocity


class System:
    moons: list[Moon]

    x_states: set[State]
    y_states: set[State]
    z_states: set[State]

    x_repeat: int = 0
    y_repeat: int = 0
    z_repeat: int = 0

    def __init__(self, moons: list[Moon]) -> None:
        self.moons = moons
        x, y, z = self.make_states()
        self.x_states = {x}
        self.y_states = {y}
        self.z_states = {z}

    def __str__(self) -> str:
        return '\n'.join([str(moon) for moon in self.moons])

    @property
    def total_energy(self) -> int:
        return sum(moon.total_energy for moon in self.moons)

    @property
    def is_finite(self) -> bool:
        return bool(self.x_repeat and self.y_repeat and self.z_repeat)

    @property
    def first_repeat(self) -> int:
        if not self.is_finite:
            return -1
        return math.lcm(self.x_repeat, self.y_repeat, self.z_repeat)

    def make_states(self) -> tuple[State, State, State]:
        return (
            State(tuple(moon.position.x for moon in self.moons), tuple(moon.velocity.x for moon in self.moons)),
            State(tuple(moon.position.y for moon in self.moons), tuple(moon.velocity.y for moon in self.moons)),
            State(tuple(moon.position.z for moon in self.moons), tuple(moon.velocity.z for moon in self.moons))
        )

    def simulate(self, steps: int) -> None:
        for i in range(steps):
            self.time_step()

    def find_repetition(self) -> None:
        while not self.is_finite:
            self.time_step()

    def time_step(self) -> None:
        self.apply_gravity()
        self.apply_velocity()
        self.check_repetition()

    def apply_gravity(self) -> None:
        for moon1, moon2 in itertools.combinations(self.moons, 2):
            moon1.update_velocity(moon2)

    def apply_velocity(self) -> None:
        for moon in self.moons:
            moon.move()

    def check_repetition(self) -> None:
        x, y, z = self.make_states()
        if not self.x_repeat:
            if x in self.x_states:
                self.x_repeat = len(self.x_states)
            else:
                self.x_states.add(x)
        if not self.y_repeat:
            if y in self.y_states:
                self.y_repeat = len(self.y_states)
            else:
                self.y_states.add(y)
        if not self.z_repeat:
            if z in self.z_states:
                self.z_repeat = len(self.z_states)
            else:
                self.z_states.add(z)


_lines = read_input()
_moons = [Moon(Point3D(*parse(moon_pattern, _line, evaluate_result=int))) for _line in _lines]
_system = System(_moons)
_system.simulate(1000)
print(f'Part 1: {_system.total_energy}')
_system.find_repetition()
print(f'Part 2: {_system.first_repeat}')
