from __future__ import annotations

from copy import copy
from typing import Generator, Generic, Hashable, Iterable, Reversible, Type, TypeVar

T = TypeVar('T', bound=Hashable)
List = TypeVar('List', bound='LoopingList')


class Element(Generic[T]):
    value: T
    previous: Element[T] | None = None
    next: Element[T] | None = None

    def __init__(self, value: T, /) -> None:
        self.value = value

    def insert(self, element: Element[T]) -> None:
        _next = self.next

        self.next = element
        element.previous = self
        if _next:
            _next.previous = element
            element.next = _next

    def uncouple(self) -> None:
        self.previous = None
        self.next = None

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f'<{self.value}>'

    def __hash__(self) -> int:
        return hash(self.value)


_add = ['__delitem__', '__doc__', '__eq__', '__getitem__', '__ne__', '__setitem__']
_maybe = ['__ge__', '__gt__', '__imul__', '__le__', '__lt__', '__mul__', '__rmul__']
_pickle = ['__getstate__', '__reduce__', '__reduce_ex__']

_list = ['index', 'insert', 'pop', 'remove', 'reverse', 'sort']
_deque = ['index', 'insert', 'pop',
          'popleft', 'remove', 'reverse', 'rotate']


class LoopingList(Generic[T], Reversible):
    _elements: dict[T, Element]
    _start: Element | None = None

    def __init__(self, values: Iterable[T] = (), /) -> None:
        self._elements = {}
        self._set(values)

    @property
    def start(self) -> T | None:
        return self._start.value if self._start is not None else None

    def element(self, value: T) -> Element[T]:
        if value not in self._elements:
            raise ValueError(f'no element with value {value} in list')
        return self._elements[value]

    def next(self, value: T) -> T:
        element = self.element(value)
        return element.next.value

    def append(self, value: T, /) -> None:
        if self._start is None:
            self._set([value])
            return
        self.append_after(value, self.start)

    def append_after(self, value: T, /, after: T) -> None:
        after = self.element(after)
        element = self._add_element(value)
        after.insert(element)

    def extend(self, values: Iterable[T], /) -> None:
        if self._start is None:
            return self._set(values)
        self.extend_after(values, self._start.previous.value)

    def extend_after(self, values: Iterable[T], /, after: T) -> None:
        after = self.element(after)
        elements = self._add_elements(values)
        for element in elements:
            after.insert(element)
            after = element

    def remove(self, value: T, /) -> T:
        element = self.element(value)
        if element is self._start:
            if element.next is element:
                self.clear()
                return value
            self._start = element.next
        element.previous.next = element.next
        element.next.previous = element.previous
        element.uncouple()
        del self._elements[value]
        return value

    def remove_after(self, value: T, /) -> T:
        return self.remove(self.element(value).next)

    def remove_multiple(self, from_value: T, /, amount: int = 1) -> list[T]:
        if len(self) < amount:
            raise ValueError(f'can\'t remove {amount} elements from list with {len(self)} elements')
        element = self.element(from_value)
        result = []
        while len(result) < amount:
            value = element.value
            element = element.next
            result.append(self.remove(value))
        return result

    def remove_multiple_after(self, after: T, /, amount: int = 1) -> list[T]:
        return self.remove_multiple(self.next(after), amount)

    def rotate(self, new_start: T) -> None:
        self._start = self.element(new_start)

    def clear(self) -> None:
        for element in self._elements.values():
            element.uncouple()
        self._start = None
        self._elements.clear()

    def __str__(self) -> str:
        return f'LoopingList{list(self)}'

    def __repr__(self) -> str:
        return str(self)

    def __bool__(self) -> bool:
        return self._start is not None

    def __len__(self) -> int:
        return len(self._elements)

    def __contains__(self, item: T) -> bool:
        return item in self._elements

    def __iter__(self) -> Generator[T, None, None]:
        element = self._start
        while element:
            yield element.value
            element = element.next
            if element is self._start:
                break

    def __reversed__(self) -> Generator[T, None, None]:
        element = self._start
        while element:
            element = element.previous
            yield element.value
            if element is self._start:
                break

    def __copy__(self: List[T]) -> Type[List[T]]:
        return self.__class__(self)

    def __add__(self: List[T], other: Iterable[T]) -> List[T]:
        result = copy(self)
        result.extend(other)
        return result

    def __iadd__(self, other: Iterable[T]) -> None:
        self.extend(other)

    def __radd__(self: List[T], other: Iterable[T]) -> List[T]:
        result = copy(self)
        result.extend(other)
        return result

    def _set(self, values: Iterable[T]) -> None:
        if self._start is not None:
            self.clear()

        elements = self._add_elements(values)
        if not elements:
            return
        self._start = elements[0]
        self._start.next = self._start
        self._start.previous = self._start
        for element in elements:
            self._start.previous.insert(element)

    def _add_element(self, value: T) -> Element[T]:
        if value in self._elements:
            raise ValueError(f'an element with value {value} already exists in list')
        element = Element(value)
        self._elements[value] = element
        return element

    def _add_elements(self, values: Iterable[T]) -> list[Element[T]]:
        elements = []
        for value in values:
            if value in self._elements:
                raise ValueError(f'an element with value {value} already exists in list')
            elements.append(Element(value))
        for element in elements:
            self._elements[element.value] = element
        return elements
