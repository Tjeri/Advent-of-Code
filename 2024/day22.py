from collections import defaultdict

from aoc.input import read_input


def mix_and_prune(num1: int, num2: int) -> int:
    return (num1 ^ num2) % 16777216


def next_random(old: int) -> int:
    step1 = mix_and_prune(old, old * 64)
    step2 = mix_and_prune(step1, step1 // 32)
    return mix_and_prune(step2, step2 * 2048)


def get_random(seed: int, skip: int) -> int:
    num = seed
    for _ in range(skip):
        num = next_random(num)
    return num


def collect_sequences(seed: int, collective: dict[tuple[int, ...], int]) -> None:
    found: set[tuple[int, ...]] = set()
    current = []
    num = seed
    digit = num % 10
    for _ in range(2000):
        _next = next_random(num)
        _digit = _next % 10
        current.append(_digit - digit)
        if len(current) > 4:
            current.pop(0)
        if len(current) == 4:
            t = tuple(current)
            if t not in found:
                collective[t] += _digit
                found.add(t)
        num = _next
        digit = _digit


_lines = read_input(True)
part1 = 0
part2 = defaultdict(lambda: 0)
for _line in _lines:
    part1 += get_random(int(_line), 2000)
    collect_sequences(int(_line), part2)
print('Part 1:', part1)
print('Part 2:', max(value for value in part2.values()))
