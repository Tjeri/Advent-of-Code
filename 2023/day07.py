from __future__ import annotations

from enum import auto, IntEnum

from aoc.input import read_input

card_map1 = {str(i): i for i in range(2, 10)} | {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
card_map2 = {str(i): i for i in range(2, 10)} | {'J': 1, 'T': 10, 'Q': 12, 'K': 13, 'A': 14}


class Type(IntEnum):
    HighCard = auto()
    OnePair = auto()
    TwoPair = auto()
    ThreeOfAKind = auto()
    FullHouse = auto()
    FourOfAKind = auto()
    FiveOfAKind = auto()


class Hand:
    cards: list[int]

    def __init__(self, cards: str) -> None:
        self.cards = [card_map1[card] for card in cards]

    def __lt__(self, other: Hand) -> bool:
        if self.type < other.type:
            return True
        if self.type > other.type:
            return False
        for i in range(5):
            if self.cards[i] < other.cards[i]:
                return True
            if self.cards[i] > other.cards[i]:
                return False
        return False

    def count(self, card: int) -> int:
        return len([1 for _card in self.cards if _card == card])

    def get_sorted_unique_counts(self) -> list[int]:
        result = [self.count(card) for card in set(self.cards)]
        result.sort(reverse=True)
        return result

    @property
    def type(self) -> Type:
        unique_counts = self.get_sorted_unique_counts()
        if unique_counts[0] == 5:
            return Type.FiveOfAKind
        if unique_counts[0] == 4:
            return Type.FourOfAKind
        if unique_counts[0] == 3:
            if unique_counts[1] == 2:
                return Type.FullHouse
            return Type.ThreeOfAKind
        if unique_counts[0] == 2:
            if unique_counts[1] == 2:
                return Type.TwoPair
            return Type.OnePair
        return Type.HighCard


class Hand2(Hand):
    def __init__(self, cards: str) -> None:
        self.cards = [card_map2[card] for card in cards]

    def get_sorted_unique_counts(self) -> list[int]:
        jokers = self.count(card_map2['J'])
        result = [self.count(card) for card in set(self.cards) if card != card_map2['J']]
        if len(result) == 0:
            result.append(0)
        result.sort(reverse=True)
        result[0] += jokers
        return result


def part1(lines: list[str]) -> int:
    hands = []
    for line in lines:
        hand, bid = line.split(' ')
        hands.append((Hand(hand), int(bid)))
    hands.sort(key=lambda hand: hand[0])
    result = 0
    for i, (_, bid) in enumerate(hands):
        result += (i + 1) * bid
    return result


def part2(lines: list[str]) -> int:
    hands = []
    for line in lines:
        hand, bid = line.split(' ')
        hands.append((Hand2(hand), int(bid)))
    hands.sort(key=lambda hand: hand[0])
    result = 0
    for i, (_, bid) in enumerate(hands):
        result += (i + 1) * bid
    return result


_lines = read_input(True)
print(f'Part 1: {part1(_lines)}')
print(f'Part 2: {part2(_lines)}')
