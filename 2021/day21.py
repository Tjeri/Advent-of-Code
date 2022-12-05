from __future__ import annotations

from dataclasses import dataclass


class DeterministicDie:
    value: int = 0
    rolls: int = 0

    def roll(self) -> int:
        self.rolls += 1
        self.value += 1
        if self.value > 100:
            self.value = 1
        return self.value


class DiracDie:
    p1_pos: int = 0
    p1_score: int = 0
    p2_pos: int = 0
    p2_score: int = 0

    die: DeterministicDie

    def __init__(self, start_p1: int, start_p2: int) -> None:
        self.p1_pos = start_p1
        self.p2_pos = start_p2
        self.die = DeterministicDie()

    @property
    def losing_score(self) -> int:
        return self.p1_score if self.p1_score < self.p2_score else self.p2_score

    def simulate_game(self) -> None:
        while True:
            if self.take_turn(True):
                break
            if self.take_turn(False):
                break

    def take_turn(self, player1: bool) -> bool:
        roll = self.die.roll() + self.die.roll() + self.die.roll()
        if player1:
            self.p1_pos += roll
            self.p1_pos %= 10
            self.p1_score += self.p1_pos + 1
            if self.p1_score >= 1000:
                return True
        else:
            self.p2_pos += roll
            self.p2_pos %= 10
            self.p2_score += self.p2_pos + 1
            if self.p2_score >= 1000:
                return True
        return False


file_name = '../data/2021/day21.txt'
with open(file_name) as file:
    data = file.readlines()

game1 = DiracDie(int(data[0].strip()[-1]) - 1, int(data[1].strip()[-1]) - 1)
game1.simulate_game()

part1 = game1.losing_score * game1.die.rolls
print(f'Part 1: {part1}')


class MultiverseDirac:
    boards: dict[DiracConfiguration, int]
    p1_wins: int = 0
    p2_wins: int = 0
    possible_rolls: dict[int, int]

    def __init__(self, start_p1: int, start_p2: int) -> None:
        start_config = DiracConfiguration(start_p1, 0, start_p2, 0, True)
        self.boards = {start_config: 1}
        self.possible_rolls = {
            3: 1,
            4: 3,
            5: 6,
            6: 7,
            7: 6,
            8: 3,
            9: 1
        }

    def do_turn(self) -> None:
        new_boards: dict[DiracConfiguration, int] = dict()
        for config, amount in self.boards.items():
            for roll, roll_amount in self.possible_rolls.items():
                new_config = config.take_turn(roll)
                if new_config.winning_score >= 21:
                    if new_config.winner_p1:
                        self.p1_wins += roll_amount * amount
                    else:
                        self.p2_wins += roll_amount * amount
                else:
                    new_boards[new_config] = new_boards.get(new_config, 0) + roll_amount * amount
        self.boards = new_boards

    def simulate(self) -> None:
        while len(self.boards) > 0:
            self.do_turn()


@dataclass
class DiracConfiguration:
    p1_pos: int
    p1_score: int
    p2_pos: int
    p2_score: int

    p1_turn: bool

    def __hash__(self):
        return hash(f'{self.p1_pos}:{self.p1_score}/{self.p2_pos}:{self.p2_score} - {self.p1_turn}')

    @property
    def winner_p1(self) -> bool:
        return self.p1_score > self.p2_score

    @property
    def winning_score(self) -> int:
        return self.p1_score if self.p1_score > self.p2_score else self.p2_score

    @property
    def losing_score(self) -> int:
        return self.p1_score if self.p1_score < self.p2_score else self.p2_score

    def take_turn(self, roll: int) -> DiracConfiguration:
        new_config = DiracConfiguration(self.p1_pos, self.p1_score, self.p2_pos, self.p2_score, not self.p1_turn)
        if self.p1_turn:
            new_config.p1_pos += roll
            new_config.p1_pos %= 10
            new_config.p1_score += new_config.p1_pos + 1
        else:
            new_config.p2_pos += roll
            new_config.p2_pos %= 10
            new_config.p2_score += new_config.p2_pos + 1
        return new_config


game2 = MultiverseDirac(int(data[0].strip()[-1]) - 1, int(data[1].strip()[-1]) - 1)
game2.simulate()
part2 = game2.p1_wins if game2.p1_wins > game2.p2_wins else game2.p2_wins
print(f'Part 2: {part2}')
