from typing import TypeVar, Iterable

T = TypeVar('T')


def flatten(flatten_list: Iterable[Iterable[T]]) -> list[T]:
    return [element for sublist in flatten_list for element in sublist]
