from aoc.input import read_input
import re


def parse_card(card: str) -> tuple[set[int], list[int]]:
    winning, owned = card[card.index(': ') + 2:].split(' | ')
    winning, owned = re.split(r' +', winning.strip()), re.split(r' +', owned.strip())
    return {int(num) for num in winning}, [int(num) for num in owned]


def count_won(card: str) -> int:
    won = 0
    owned, winning = parse_card(card)
    for number in winning:
        if number in owned:
            won += 1
    return won


def part1(lines: list[str]) -> int:
    result = 0
    for line in lines:
        won = count_won(line)
        if won:
            result += pow(2, won - 1)
    return result


def part2(lines: list[str]) -> int:
    instances: dict[int, int] = {i + 1: 1 for i in range(len(lines))}
    for i, line in enumerate(lines):
        won = count_won(line)
        for j in range(i + 2, i + 2 + won):
            instances[j] += instances[i + 1]
    return sum(amount for _, amount in instances.items())


_lines = read_input(True)
print(f'Part 1: {part1(_lines)}')
print(f'Part 2: {part2(_lines)}')
