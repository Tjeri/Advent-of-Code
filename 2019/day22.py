from __future__ import annotations

from typing import Callable
import math

from aoc.input import read_input
from aoc.maths.modular_inverse import mod_inverse


class Equation:
    x_factor: int
    rest: int
    total: int

    def __init__(self, x_factor: int, rest: int, total: int) -> None:
        self.x_factor = x_factor
        self.rest = rest
        self.total = total
        self.x_factor %= total
        self.rest %= total

    @staticmethod
    def from_lines(lines: list[str], total_cards: int) -> Equation:
        equation = Equation(1, 0, total_cards)

        for line in lines:
            match line.split(' '):
                case 'deal', 'into', 'new', 'stack':
                    equation = equation.deal_into_new_stack()
                case 'cut', amount:
                    equation = equation.cut(int(amount))
                case 'deal', 'with', 'increment', increment:
                    equation = equation.deal_with_increment(int(increment))
                case 'Result:', *numbers:
                    print(f'Expected Result:\n{[int(_num) for _num in numbers]}')
                case _:
                    raise ValueError(f'Unknown command: {line}')

        return equation

    def solve(self, x: int) -> int:
        return (self.x_factor * x + self.rest) % self.total

    def solve_x(self, result: int) -> int:
        return (result - self.rest) * mod_inverse(self.x_factor, self.total) % self.total

    def deal_into_new_stack(self) -> Equation:
        return Equation(-self.x_factor, self.total - 1 - self.rest, self.total)

    def cut(self, amount: int) -> Equation:
        return Equation(self.x_factor, self.rest - amount, self.total)

    def deal_with_increment(self, increment: int) -> Equation:
        return Equation(self.x_factor * increment, self.rest * increment, self.total)

    def interlace(self, other: Equation) -> Equation:
        return Equation(self.x_factor * other.x_factor, self.x_factor * other.rest + self.rest, self.total)

    def interlace_multiple(self, iterations: int) -> Equation:
        iteration = 1
        cache: dict[int, Equation] = {1: self}
        result = self
        while iteration < iterations:
            if iteration * 2 <= iterations:
                iteration *= 2
                result = result.interlace(result)
                cache[iteration] = result
                continue
            needed = iterations - iteration
            use = pow(2, math.floor(math.log2(needed)))
            result = result.interlace(cache[use])
            iteration += use
        return result


_lines = read_input()
equation = Equation.from_lines(_lines, 10_007)
print(f'Part 1: {equation.solve(2019)}')
equation = Equation.from_lines(_lines, 119_315_717_514_047)
interlaced = equation.interlace_multiple(101_741_582_076_661)
print(f'Part 2: {interlaced.solve_x(2020)}')
