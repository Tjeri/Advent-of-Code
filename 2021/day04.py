from dataclasses import dataclass


@dataclass
class BingoField:
    value: int
    marked: bool = False


class BingoBoard:
    board: list[list[BingoField]]
    last_number: int = 0

    def __init__(self, board_input: list[str]) -> None:
        self.board = []
        for _line in board_input:
            _numbers = _line.strip().split(' ')
            self.board.append([BingoField(int(num)) for num in _numbers if num != ''])

    def get_all_fields(self, marked: bool) -> list[BingoField]:
        all_fields = []
        for _line in self.board:
            for field in _line:
                if marked is field.marked:
                    all_fields.append(field)
        return all_fields

    def mark(self, _number: int) -> bool:
        self.last_number = _number
        for _line in self.board:
            for field in _line:
                if field.value == _number:
                    field.marked = True
                    return self.has_won()
        return False

    def has_won(self) -> bool:
        for _line in self.board:
            if all(field.marked for field in _line):
                return True
        for i in range(0, len(self.board)):
            if all(_line[i].marked for _line in self.board):
                return True
        return False

    @property
    def score(self) -> int:
        unmarked_sum = sum([field.value for field in self.get_all_fields(False)])
        return unmarked_sum * self.last_number


with open('../data/2021/day04.txt') as file:
    lines = file.readlines()

numbers = [int(s) for s in lines[0].strip().split(',')]
boards = []

i = 2
raw_board = []
while i < len(lines):
    line = lines[i].strip()
    if line == '':
        boards.append(BingoBoard(raw_board))
        raw_board = []
        i += 1
        continue
    raw_board.append(line)
    i += 1
boards.append(BingoBoard(raw_board))

winner = None
loser = None
for number in numbers:
    for board in boards:
        if not board.has_won() and board.mark(number):
            if winner is None:
                winner = board
            loser = board

print(f'Part 1: {winner.score}')
print(f'Part 2: {loser.score}')
