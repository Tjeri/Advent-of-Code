from heapq import heappush, heappop
from typing import TypeVar, Generic

T = TypeVar('T')


class PriorityQueue(Generic[T]):
    elements: list[T]

    def __init__(self) -> None:
        self.elements = list()

    def push(self, item: T, priority: float) -> None:
        heappush(self.elements, (priority, item))

    def pop(self) -> T:
        return heappop(self.elements)[1]

    def __bool__(self) -> bool:
        return len(self.elements) > 0

    def __len__(self) -> int:
        return len(self.elements)
