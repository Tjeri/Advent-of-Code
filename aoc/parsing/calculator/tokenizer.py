from __future__ import annotations

from enum import Enum


class TokenType(Enum):
    Number = '0123456789'
    Plus = '+'
    Times = '*'
    BracketOpen = '([{'
    BracketClose = ')]}'

    @staticmethod
    def from_char(char: str) -> TokenType | None:
        if char in ' \n\r\t':
            return None
        for token_type in TokenType:
            if char in token_type.value:
                return token_type
        return None

    def has_value(self) -> bool:
        return self in (TokenType.Number, TokenType.BracketOpen, TokenType.BracketClose)

    def can_have_multiple_chars(self) -> bool:
        return self is TokenType.Number


class Token:
    type: TokenType
    value: str | int | None = None

    def __init__(self, token_type: TokenType, value: str | int) -> None:
        self.type = token_type
        if not token_type.has_value():
            return
        if token_type is TokenType.Number:
            self.value = int(value)
        else:
            self.value = value

    def __str__(self) -> str:
        if self.value is None:
            return self.type.name
        return f'{self.type} ({self.value})'

    def __repr__(self) -> str:
        return str(self)


def tokenize(text: str) -> list[Token]:
    tokens = []
    index = 0
    while index < len(text):
        char = text[index]
        token_type = TokenType.from_char(char)
        if not token_type:
            index += 1
            continue
        if token_type.can_have_multiple_chars():
            index, value = tokenize_type_with_multiple_chars(text, index, token_type)
            tokens.append(Token(token_type, value))
        else:
            tokens.append(Token(token_type, char))
            index += 1
    return tokens


def tokenize_type_with_multiple_chars(text: str, start: int, token_type: TokenType) -> tuple[int, str]:
    end = start + 1
    while end < len(text) and TokenType.from_char(text[end]) is token_type:
        end += 1
    return end, text[start:end]
