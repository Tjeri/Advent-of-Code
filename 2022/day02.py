from __future__ import annotations
from enum import Enum


class Sign(Enum):
    Rock = 1
    Paper = 2
    Scissors = 3

    def __lt__(self, other: Sign) -> bool:
        if self == Sign.Scissors and other == Sign.Rock:
            return True
        if self == Sign.Rock and other == Sign.Scissors:
            return False
        return self.value < other.value

    def get_winner(self) -> Sign:
        if self == Sign.Rock:
            return Sign.Paper
        if self == Sign.Paper:
            return Sign.Scissors
        return Sign.Rock

    def get_loser(self) -> Sign:
        if self == Sign.Rock:
            return Sign.Scissors
        if self == Sign.Paper:
            return Sign.Rock
        return Sign.Paper


class Result(Enum):
    Lose = 0
    Draw = 3
    Win = 6

    def get_matching(self, sign: Sign) -> Sign:
        if self == Result.Lose:
            return sign.get_loser()
        if self == Result.Draw:
            return sign
        return sign.get_winner()


sign_map = {'A': Sign.Rock, 'B': Sign.Paper, 'C': Sign.Scissors, 'X': Sign.Rock, 'Y': Sign.Paper, 'Z': Sign.Scissors}
result_map = {'X': Result.Lose, 'Y': Result.Draw, 'Z': Result.Win}

points_for_loss = 0
points_for_draw = 3
points_for_winning = 6

points_1 = 0
points_2 = 0
with open('../data/2022/day02.txt') as file:
    for line in file.readlines():
        opponent, me_result = line.strip().split(' ')
        opponent = sign_map.get(opponent)
        me = sign_map.get(me_result)
        result = result_map.get(me_result)
        points_1 += me.value
        if me < opponent:
            points_1 += Result.Lose.value
        elif me == opponent:
            points_1 += Result.Draw.value
        else:
            points_1 += Result.Win.value
        points_2 += result.value
        points_2 += result.get_matching(opponent).value

print(f'Part 1: {points_1}')
print(f'Part 2: {points_2}')
