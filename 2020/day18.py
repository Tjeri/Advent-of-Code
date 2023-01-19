from __future__ import annotations

from aoc.input import read_input
from aoc.parsing.calculator.parser import parse
from aoc.parsing.calculator.tokenizer import tokenize, TokenType


def calculate(lines: list[str], operator_priorities: list[set[TokenType]]) -> int:
    return sum(parse(tokenize(line), operator_priorities) for line in lines)


_lines = read_input()
print(f'Part 1: {calculate(_lines, [{TokenType.Times, TokenType.Plus}])}')
print(f'Part 2: {calculate(_lines, [{TokenType.Plus}, {TokenType.Times}])}')
