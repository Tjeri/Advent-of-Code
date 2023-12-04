from typing import TypeVar

T = TypeVar('T')


def flatten(flatten_list: list[list[T]]) -> list[T]:
    return [element for sublist in flatten_list for element in sublist]
