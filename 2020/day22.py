from enum import Enum

from aoc.input import read_split_input


class Player(Enum):
    One = 1
    Two = 2


class Combat:
    player1: list[int]
    player2: list[int]

    winner: Player | None = None

    def __init__(self, player1: list[int | str], player2: list[int | str]) -> None:
        self.player1 = list(map(int, player1))
        self.player2 = list(map(int, player2))

    def simulate(self) -> Player:
        while not self.winner:
            self.play_round()
            if not len(self.player1):
                self.winner = Player.Two
            elif not len(self.player2):
                self.winner = Player.One
        return self.winner

    def play_round(self) -> None:
        player1 = self.player1.pop(0)
        player2 = self.player2.pop(0)
        self.add_cards(player1, player2, self.determine_winner(player1, player2))

    def determine_winner(self, player1: int, player2: int) -> Player:
        return Player.One if player1 > player2 else Player.Two

    def add_cards(self, player1: int, player2: int, winner: Player) -> None:
        if winner is Player.One:
            self.player1.append(player1)
            self.player1.append(player2)
        else:
            self.player2.append(player2)
            self.player2.append(player1)

    def winning_score(self) -> int:
        if self.winner is None:
            return 0
        hand = self.player1 if self.winner is Player.One else self.player2
        score = 0
        for i, value in enumerate(reversed(hand)):
            score += (i + 1) * value
        return score


class RecursiveCombat(Combat):
    previous_rounds: set[tuple[tuple[int, ...], tuple[int, ...]]]

    def __init__(self, player1: list[int | str], player2: list[int | str]) -> None:
        super().__init__(player1, player2)
        self.previous_rounds = set()

    @property
    def id(self) -> tuple[tuple[int, ...], tuple[int, ...]]:
        return tuple(self.player1), tuple(self.player2)

    def play_round(self) -> None:
        if self.id in self.previous_rounds:
            self.winner = Player.One
            return
        self.previous_rounds.add(self.id)
        super().play_round()

    def determine_winner(self, player1: int, player2: int) -> Player:
        if len(self.player1) >= player1 and len(self.player2) >= player2:
            return RecursiveCombat(self.player1[:player1], self.player2[:player2]).simulate()
        return super().determine_winner(player1, player2)


_groups = read_split_input()
game = Combat(_groups[0][1:], _groups[1][1:])
game.simulate()
print(f'Part 1: {game.winning_score()}')
game2 = RecursiveCombat(_groups[0][1:], _groups[1][1:])
game2.simulate()
print(f'Part 2: {game2.winning_score()}')
