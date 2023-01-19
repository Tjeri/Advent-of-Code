from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Type

from aoc.parsing.calculator.tokenizer import Token, TokenType


class Element(ABC):
    @property
    @abstractmethod
    def value(self) -> int:
        pass


class Number(Element):
    _value: int

    def __init__(self, value: str | int) -> None:
        self._value = value

    @property
    def value(self) -> int:
        return self._value


class Clojure(Element):
    element = Element

    def __init__(self, element: Element) -> None:
        self.element = element

    @property
    def value(self) -> int:
        return self.element.value


class Term(Element, ABC):
    type: TokenType
    left: Element
    right: Element

    def __init__(self, left: Element, right: Element) -> None:
        self.left = left
        self.right = right


class Addition(Term):
    type = TokenType.Plus

    @property
    def value(self) -> int:
        return self.left.value + self.right.value


class Multiplication(Term):
    type = TokenType.Times

    @property
    def value(self) -> int:
        return self.left.value * self.right.value


class TokenParser:
    __bracket_matcher: dict[str, str] = {'(': ')', '[': ']', '{': '}'}
    __default_priorities: list[set[TokenType]] = [{TokenType.Times}, {TokenType.Plus}]
    __term_classes: dict[TokenType, Type[Term]] = {TokenType.Plus: Addition, TokenType.Times: Multiplication}
    tokens: list[Token]
    operator_priorities: list[set[TokenType]]
    index: int = 0

    def __init__(self, tokens: list[Token], operator_priorities: list[set[TokenType]] = None) -> None:
        self.tokens = tokens
        self.operator_priorities = operator_priorities or self.__default_priorities
        if not self.operator_priorities:
            raise ValueError('Operator priorities are empty.')

    def parse(self) -> Term:
        result = None
        while self.index < len(self.tokens):
            token = self.tokens[self.index]
            if token.type is TokenType.Number:
                self.validate_state(result is None)
                result = Number(token.value)
            elif token.type in self.__term_classes:
                self.validate_state(result is not None)
                result = self.parse_term(result, token.type)
            elif token.type is TokenType.BracketOpen:
                self.validate_state(result is None)
                result = self.parse_brackets()
            elif token.type is TokenType.BracketClose:
                self.validate_state(result is not None)
                return result
            else:
                raise ValueError(f'Missing implementation for {token.type}.')
            self.index += 1
        if result is None:
            raise ValueError('Couldn\'t find a result.')
        return result

    def validate_state(self, validate: bool) -> None:
        if not validate:
            raise ValueError(f'Found unexpected token {self.tokens[self.index].type} at {self.index}')

    def parse_term(self, left: Term, token_type: TokenType) -> Term:
        self.index += 1
        token = self.tokens[self.index]
        if token.type not in (TokenType.Number, TokenType.BracketOpen):
            raise ValueError(f'Found unexpected Token {token.type} at {self.index}.')
        if token.type is TokenType.BracketOpen:
            right = self.parse_brackets()
        elif token.type is TokenType.Number:
            right = Number(token.value)
        else:
            raise ValueError(f'Missing implementation for token type {token.type} at {self.index}.')
        return self.balance_term(self.__term_classes[token_type](left, right))

    def balance_term(self, term: Term) -> Term:
        if self.get_priority(term.left) == 0:
            return term
        if isinstance(term.left, Term):
            if self.get_priority(term.left) > self.get_priority(term):
                return term.left.__class__(term.left.left, term.__class__(term.left.right, term.right))
        return term

    def get_priority(self, element: Element) -> int:
        if not isinstance(element, Term):
            return -1
        for i, types in enumerate(self.operator_priorities):
            if element.type in types:
                return i
        raise ValueError(f'Operator priority missing for {element.type}.')

    def parse_brackets(self) -> Clojure:
        opening = self.tokens[self.index]
        if opening.value not in self.__bracket_matcher:
            raise ValueError(f'No matching bracket found for "{opening.value}" at {self.index}')
        self.index += 1
        parsed = self.parse()
        closing = self.tokens[self.index]
        if closing.value != self.__bracket_matcher[opening.value]:
            raise ValueError(f'Mismatch for brackets "{opening.value}" and "{closing.value}" at {self.index}.')
        return Clojure(parsed)


def parse(tokens: list[Token], operator_priorities: list[set[TokenType]] = None) -> int:
    return TokenParser(tokens, operator_priorities).parse().value
