from copy import copy

from aoc.coord2d.point import Point


def get_movement(direction: str) -> Point:
    if direction == 'U':
        return Point(y=-1)
    if direction == 'R':
        return Point(x=1)
    if direction == 'D':
        return Point(y=1)
    if direction == 'L':
        return Point(x=-1)
    raise ValueError


def move_tail(_head: Point, _tail: Point) -> Point:
    diff = _head - _tail
    dx = abs(diff.x)
    dy = abs(diff.y)
    if dx > 1 or dy > 1:
        return _tail + Point(diff.x // max(dx, 1), diff.y // max(dy, 1))
    return _tail


head = Point()
tail_1 = Point()
tails_2 = [Point() for _ in range(9)]
visited_1 = {copy(tail_1)}
visited_2 = {copy(tails_2[-1])}
with open('../data/2022/day09.txt') as file:
    for line in file.readlines():
        _direction, steps = line.strip().split(' ')
        movement = get_movement(_direction)
        for _ in range(int(steps)):
            head += movement
            tail_1 = move_tail(head, tail_1)
            visited_1.add(copy(tail_1))
            for i in range(len(tails_2)):
                tails_2[i] = move_tail(head if i == 0 else tails_2[i - 1], tails_2[i])
            visited_2.add(copy(tails_2[-1]))

print(f'Part 1: {len(visited_1)}')
print(f'Part 2: {len(visited_2)}')
