from __future__ import annotations

from copy import copy
from dataclasses import dataclass
from enum import Enum
from typing import Callable

from aoc.input import read_input


class TokenType(Enum):
    Number = '0123456789'
    Addition = '+'
    Multiplication = '*'
    ParenthesisOpen = '('
    ParenthesisClose = ')'

    @classmethod
    def special_from_char(cls, char: str) -> TokenType | None:
        if char == ' ':
            return None
        try:
            return cls(char)
        except ValueError:
            return None


@dataclass
class Token:
    type: TokenType
    value: int | None = None


def tokenize(line: str) -> list[Token]:
    tokens = []
    num: str = ''
    for char in line:
        if char in TokenType.Number.value:
            num += char
            continue
        if num:
            tokens.append(Token(TokenType.Number, int(num)))
            num = ''
        token_type = TokenType.special_from_char(char)
        if token_type:
            tokens.append(Token(token_type))
    if num:
        tokens.append(Token(TokenType.Number, int(num)))
    return tokens


def parse(tokens: list[Token]) -> int:
    value = None
    op = None
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.type is TokenType.ParenthesisOpen:
            _i, _value = parse_parentheses(tokens[i + 1:], parse)
            i += _i
            token = Token(TokenType.Number, _value)
        if token.type is TokenType.ParenthesisClose:
            raise ValueError('Shouldn\'t find closing parenthesis in parse.')
        if token.type is TokenType.Number:
            if value is None:
                value = token.value
            else:
                if op is None:
                    raise ValueError('Operator missing.')
                value = op(value, token.value)
                op = None
        elif token.type is TokenType.Addition:
            if op is not None:
                raise ValueError('Multiple Operators')
            op = int.__add__
        elif token.type is TokenType.Multiplication:
            if op is not None:
                raise ValueError('Multiple Operators')
            op = int.__mul__
        else:
            raise ValueError(f'Missing TokenType: {token.type}')
        i += 1
    if value is None:
        raise ValueError('Empty Term?')
    return value


def parse2(original_tokens: list[Token]) -> int:
    tokens = copy(original_tokens)
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.type is TokenType.ParenthesisOpen:
            j, value = parse_parentheses(tokens[i + 1:], parse2)
            tokens = tokens[:i] + [Token(TokenType.Number, value)] + tokens[i + j + 1:]
        i += 1
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.type is TokenType.Addition:
            tokens[i - 1].value += tokens[i + 1].value
            tokens = tokens[:i] + tokens[i + 2:]
            i -= 1
        i += 1
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.type is TokenType.Multiplication:
            tokens[i - 1].value *= tokens[i + 1].value
            tokens = tokens[:i] + tokens[i + 2:]
            i -= 1
        i += 1
    return tokens[0].value


def parse_parentheses(tokens: list[Token], parser: Callable[[list[Token]], int]) -> tuple[int, int]:
    find_close = 0
    for i, token in enumerate(tokens):
        if token.type is TokenType.ParenthesisClose:
            if find_close == 0:
                return i + 1, parser(tokens[:i])
            find_close -= 1
        elif token.type is TokenType.ParenthesisOpen:
            find_close += 1
    raise ValueError('Missing closing parenthesis.')


_lines = read_input()
part1 = 0
for _line in _lines:
    _tokens = tokenize(_line)
    part1 += parse(_tokens)
print(f'Part 1: {part1}')
part2 = 0
for _line in _lines:
    _tokens = tokenize(_line)
    part2 += parse2(_tokens)
print(f'Part 2: {part2}')
