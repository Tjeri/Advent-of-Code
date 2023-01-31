from __future__ import annotations

from typing import Any, Generator, Generic, Hashable, Iterable, Reversible, TypeVar

T = TypeVar('T', bound=Hashable)


class LinkedListElement(Generic[T]):
    value: T
    previous_element: LinkedListElement | None
    next_element: LinkedListElement | None

    def __init__(self, value: T, *, previous_element: LinkedListElement | None = None,
                 next_element: LinkedListElement | None = None):
        self.value = value
        self.previous_element = previous_element
        self.next_element = next_element

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        return hash(self.value)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, LinkedListElement):
            raise TypeError('can only compare LinkedListElements')
        if not isinstance(other.value, self.value.__class__):
            raise TypeError('can only compare LinkedListElements with the same value type')
        return self.value == other.value

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, LinkedListElement):
            raise TypeError('can only compare LinkedListElements')
        if not isinstance(other.value, self.value.__class__):
            raise TypeError('can only compare LinkedListElements with the same value type')
        return self.value < other.value


Element = LinkedListElement[T]
ElementOrValue = T | Element


class UniqueLinkedList(Generic[T], Reversible[T]):
    first: LinkedListElement | None = None
    last: LinkedListElement | None = None
    elements: dict[T, Element]

    def __init__(self, elements: UniqueLinkedList[T] | Iterable[ElementOrValue] | None = None) -> None:
        self.elements = {}
        if elements is None:
            return
        self.extend(elements)

    def get(self, value: T) -> Element | None:
        return self.elements.get(value)

    def set(self, elements: Iterable[ElementOrValue], *, keep_elements: bool = False) -> None:
        if self.first is not None:
            self.clear(uncouple_elements=True)
        new_elements = self._add_elements(elements, keep_elements=keep_elements)
        if not new_elements:
            return

        if isinstance(elements, UniqueLinkedList) and keep_elements:
            self.first = elements.first
            self.last = elements.last
            self.first.previous_element = None
            self.last.next_element = None
            return

        iterator = iter(new_elements.values())
        self.first = self._get_element(next(iterator), replace=True)
        self.first.previous_element = None
        self.last = self.first
        for element in iterator:
            element = self._get_element(element, replace=True)
            self.last.next_element = element
            element.previous_element = self.last
            self.last = element
        self.last.next_element = None

    def append(self, element: ElementOrValue, *, keep_element: bool = False) -> Element:
        element = self._add_element(element, keep_element=keep_element)
        if self.first is None:
            self.first = element
        else:
            self.last.next_element = element
            element.previous_element = self.last
        self.last = element
        return element

    def prepend(self, element: ElementOrValue, *, keep_element: bool = False) -> Element:
        if self.first is None:
            return self.append(element, keep_element=keep_element)
        element = self._add_element(element, keep_element=keep_element)
        self.first.previous_element = element
        element.next_element = self.first
        self.first = element
        return Element

    def extend(self, elements: UniqueLinkedList[T] | Iterable[ElementOrValue], *, keep_elements: bool = False) -> None:
        if self.first is None:
            return self.set(elements, keep_elements=keep_elements)
        new_elements = self._add_elements(elements, keep_elements=keep_elements)
        if not new_elements:
            return
        if isinstance(elements, UniqueLinkedList) and keep_elements:
            self.last.next_element = elements.first
            elements.first.previous_element = self.last
            self.last = elements.last
            self.last.next_element = None
            return

        for element in new_elements.values():
            element = self._get_element(element, replace=True)
            self.last.next_element = element
            element.previous_element = self.last
            self.last = element
        self.last.next_element = None

    def pre_extend(self, elements: UniqueLinkedList[T] | Iterable[ElementOrValue], *,
                   keep_elements: bool = False) -> None:
        if self.first is None:
            self.extend(elements, keep_elements=keep_elements)
            return
        new_elements = self._add_elements(elements, keep_elements=keep_elements)
        if not new_elements:
            return
        if isinstance(elements, UniqueLinkedList) and keep_elements:
            self.first.previous_element = elements.last
            elements.last.next_element = self.first
            self.first = elements.first
            return

        if not isinstance(elements, Reversible):
            elements = list(elements)
        for element in reversed(elements):
            element = self._get_element(element, replace=True)
            self.first.previous_element = element
            element.next_element = self.first
            self.first = element
        self.first.previous_element = None

    def insert_before(self, element: ElementOrValue, insert: ElementOrValue, *, keep_element: bool = False) -> Element:
        element = self._get_element(element)
        if element is self.first:
            return self.prepend(insert, keep_element=keep_element)
        insert = self._add_element(insert, keep_element=keep_element)
        insert.next_element = element
        insert.previous_element = element.previous_element
        if element.previous_element is not None:
            element.previous_element.next_element = insert
        element.previous_element = insert
        return insert

    def insert_before_index(self, index: int, insert: ElementOrValue, *, keep_element: bool = False) -> Element:
        return self.insert_before(self[index], insert, keep_element=keep_element)

    def insert_after(self, element: ElementOrValue, insert: ElementOrValue, *, keep_element: bool = False) -> Element:
        element = self._get_element(element)
        if element is self.last:
            return self.append(insert, keep_element=keep_element)
        insert = self._add_element(insert, keep_element=keep_element)
        insert.previous_element = element
        insert.next_element = element.next_element
        if element.next_element is not None:
            element.next_element.previous_element = insert
        element.next_element = insert
        return insert

    def insert_list_after(self, element: ElementOrValue, inserts: Iterable[ElementOrValue], *,
                          keep_elements: bool = False) -> None:
        if element is self.last:
            return self.extend(inserts, keep_elements=keep_elements)
        next_element = element.next_element
        previous_last = self.last
        self.last = element
        self.extend(inserts, keep_elements=keep_elements)
        self.last.next_element = next_element
        next_element.previous_element = self.last
        self.last = previous_last

    def insert_after_index(self, index: int, insert: ElementOrValue, *, keep_element: bool = False) -> Element:
        return self.insert_after(self[index], insert, keep_element=keep_element)

    def remove(self, element: ElementOrValue) -> Element:
        element = self._get_element(element)
        if element.previous_element is not None:
            element.previous_element.next_element = element.next_element
        if element.next_element is not None:
            element.next_element.previous_element = element.previous_element
        if element is self.first:
            self.first = element.next_element
        if element is self.last:
            self.last = element.previous_element
        del self.elements[element.value]
        return element

    def extract(self, start: ElementOrValue, end: ElementOrValue) -> UniqueLinkedList[T]:
        start = self._get_element(start)
        end = self._get_element(end)
        self._check_correct_order(start, end)
        if start.previous_element:
            start.previous_element.next_element = end.next_element
            start.previous_element = None
        if end.next_element:
            end.next_element.previous_element = start.previous_element
            end.next_element = None
        if start is self.first:
            self.first = end.next_element
        if end is self.last:
            self.last = start.previous_element
        result = UniqueLinkedList()
        result.first = start
        result.last = end
        result._add_elements(result, keep_elements=True)
        for element in result:
            del self.elements[element.value]
        return result

    def extract_from(self, start: ElementOrValue, amount: int) -> UniqueLinkedList[T]:
        if amount < 1:
            raise ValueError(f'amount must be at least 1, but is {amount}')
        if amount > len(self):
            raise ValueError(f'amount is {amount}, but list has only {len(self)} elements')
        start = self._get_element(start)
        end = start
        for _ in range(1, amount):
            if not end.next_element:
                raise ValueError(f'not enough elements to extract {amount} from {start.value}')
            end = end.next_element
        return self.extract(start, end)

    def extract_index(self, start_index: int, end_index: int) -> UniqueLinkedList[T]:
        return self.extract_from(self[start_index], (end_index - start_index + 1) % len(self))

    def extract_from_index(self, start_index: int, amount: int) -> UniqueLinkedList[T]:
        return self.extract_from(self[start_index], amount)

    def clear(self, *, uncouple_elements: bool = True) -> None:
        if uncouple_elements:
            for element in self:
                element.previous_element = None
                element.next_element = None
        self.first = None
        self.last = None
        self.elements.clear()

    def sort(self) -> None:
        self.first = None
        self.last = None
        last_element: Element | None = None
        for value, element in sorted(self.elements.items()):
            if last_element is not None:
                last_element.next_element = element
                element.previous_element = last_element
            else:
                self.first = element
                element.previous_element = None
            last_element = element
        self.last = last_element
        if self.last is not None:
            self.last.next_element = None

    def reverse(self) -> None:
        last = self.last
        self.last = self.first
        self.first = last
        for element in self.elements.values():
            previous = element.previous_element
            element.previous_element = element.next_element
            element.next_element = previous

    def copy(self) -> UniqueLinkedList[T]:
        result = UniqueLinkedList()
        self._copy_into(result)
        return result

    def _copy_into(self, new_list: UniqueLinkedList[T]) -> None:
        if not self:
            return
        new_list.elements = {value: LinkedListElement(value) for value, element in self.elements.items()}
        new_list.first = new_list.elements[self.first.value]
        new_list.last = new_list.elements[self.last.value]
        current: Element | None = None
        for element in self:
            copy = new_list.elements[element.value]
            if current is not None:
                current.next_element = copy
                copy.previous_element = current
            current = copy

    def __str__(self) -> str:
        return f'UniqueLinkedList({list(self)})'

    def __repr__(self) -> str:
        return str(self)

    def __bool__(self) -> bool:
        return self.first is not None

    def __len__(self) -> int:
        return len(self.elements)

    def __iter__(self) -> Generator[Element, None, None]:
        element = self.first
        while element:
            yield element
            element = element.next_element
            if element is self.first:
                break

    def __reversed__(self) -> Generator[Element, None, None]:
        element = self.last
        while element:
            yield element
            element = element.previous_element
            if element is self.last:
                break

    def __getitem__(self, item: Any) -> Element:
        length = len(self.elements)
        if not isinstance(item, int):
            raise TypeError(f'list indices must be integers, not {type(item)}')
        if item < 0:
            item += length
        if item < 0 or item >= length:
            raise IndexError('list index out of range')
        if item == 0:
            return self.first
        if item == length - 1 or item == -1:
            return self.last
        if item <= length // 2:
            for i, element in enumerate(self):
                if i == item:
                    return element
        else:
            for i, element in enumerate(reversed(self)):
                if length - i - 1 == item:
                    return element

    def __contains__(self, item: Any) -> bool:
        if isinstance(item, LinkedListElement):
            return self.get(item.value) is item
        return self.get(item) is not None

    def _get_element(self, element: ElementOrValue, *, replace: bool = False) -> Element:
        value = element.value if isinstance(element, LinkedListElement) else element
        if value not in self.elements:
            raise ValueError(f'element {value} is not part of the list')
        if value is element or replace:
            return self.elements[value]
        if element is not self.elements[value]:
            raise ValueError(f'element {value} is not part of the list')
        return element

    def _add_element(self, element: ElementOrValue, *, keep_element: bool = False) -> Element:
        if not isinstance(element, LinkedListElement):
            element = LinkedListElement(element)
        elif not keep_element:
            element = LinkedListElement(element.value)
        if element.value in self.elements:
            raise ValueError(f'an element with value {element.value} already exists in list')
        self.elements[element.value] = element
        return element

    def _add_elements(self, elements: Iterable[ElementOrValue], *, keep_elements: bool = False) -> dict[T, Element]:
        update = {}
        for element in elements:
            if not isinstance(element, LinkedListElement):
                element = LinkedListElement(element)
            elif not keep_elements:
                element = LinkedListElement(element.value)
            if element.value in self.elements:
                raise ValueError(f'an element with value {element.value} already exists in list')
            if element.value in update:
                raise ValueError(f'tried to add an element with value {element.value} multiple times')
            update[element.value] = element
        self.elements.update(update)
        return update

    def _check_correct_order(self, first: Element, second: Element) -> None:
        element = first
        while element is not second and element is not None:
            element = element.next_element
        if element is None:
            raise ValueError(f'expected {second.value} to be after {first.value}, but did not find it')


class LoopingUniqueLinkedList(UniqueLinkedList[T]):
    def __init__(self, elements=None) -> None:
        super().__init__(elements)
        self._fix_loop()

    def _fix_loop(self) -> None:
        if self.first:
            self.first.previous_element = self.last
            self.last.next_element = self.first

    def append(self, element, *, keep_element=False) -> Element:
        result = super().append(element, keep_element=keep_element)
        self._fix_loop()
        return result

    def prepend(self, element, *, keep_element=False) -> Element:
        result = super().prepend(element, keep_element=keep_element)
        self._fix_loop()
        return result

    def extend(self, elements, *, keep_elements=False) -> None:
        super().extend(elements, keep_elements=keep_elements)
        self._fix_loop()

    def pre_extend(self, elements, *, keep_elements=False) -> None:
        super().pre_extend(elements, keep_elements=keep_elements)
        self._fix_loop()

    def insert_before(self, element, insert, *, keep_element=False) -> Element:
        result = super().insert_before(element, insert, keep_element=keep_element)
        self._fix_loop()
        return result

    def insert_after(self, element, insert, *, keep_element=False) -> Element:
        result = super().insert_after(element, insert, keep_element=keep_element)
        self._fix_loop()
        return result

    def insert_list_after(self, element: ElementOrValue, inserts: Iterable[ElementOrValue], *,
                          keep_elements: bool = False) -> None:
        super().insert_list_after(element, inserts, keep_elements=keep_elements)
        self._fix_loop()

    def remove(self, element) -> Element:
        result = super().remove(element)
        self._fix_loop()
        return result

    def extract(self, start: ElementOrValue, end: ElementOrValue) -> UniqueLinkedList[T]:
        start = self._get_element(start)
        end = self._get_element(end)
        result = UniqueLinkedList()
        result.first = start
        result.last = end
        start_previous = start.previous_element
        end_next = end.next_element
        start.previous_element = None
        end.next_element = None
        result._add_elements(result, keep_elements=True)
        if len(result) == len(self):
            self.clear(uncouple_elements=False)
            return result
        while self.first in result:
            self.first = self.first.next_element
            if self.first is None:
                self.first = end_next
        while self.last in result:
            self.last = self.last.previous_element
            if self.last is None:
                self.last = start_previous
        self._fix_loop()
        start_previous.next_element = end_next
        end_next.previous_element = start_previous
        for element in result:
            del self.elements[element.value]
        return result

    def extract_from(self, start, amount) -> UniqueLinkedList[T]:
        result = super().extract_from(start, amount)
        self._fix_loop()
        return result

    def sort(self) -> None:
        super().sort()
        self._fix_loop()

    def reverse(self) -> None:
        super().reverse()
        self._fix_loop()

    def copy(self) -> LoopingUniqueLinkedList[T]:
        result = LoopingUniqueLinkedList()
        self._copy_into(result)
        return result

    def __str__(self) -> str:
        return f'LoopingUniqueLinkedList({list(self)})'

    def __getitem__(self, item: Any) -> Element:
        length = len(self.elements)
        if not isinstance(item, int):
            raise TypeError(f'list indices must be integers, not {type(item)}')
        item %= length
        return super().__getitem__(item)
