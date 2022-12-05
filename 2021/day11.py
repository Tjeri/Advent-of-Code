path = '../data/2021/day11.txt'
board_size = 10
steps = 100


class OctopusConfig:
    board: list[list[int]]
    steps: int = 0
    flashes: int = 0
    first_full_flash = None

    def __init__(self):
        self.board = []

    def add_input_line(self, _line: str) -> None:
        row = []
        for c in _line.strip():
            row.append(int(c))
        self.board.append(row)

    def do_step(self) -> None:
        self.steps += 1
        old_flashes = self.flashes
        for y in range(board_size):
            for x in range(board_size):
                self.board[y][x] += 1

        for y in range(board_size):
            for x in range(board_size):
                if self.board[y][x] > 9:
                    self.flash(x, y)
        if not self.first_full_flash:
            if self.flashes == old_flashes + 100:
                self.first_full_flash = self.steps

    def flash(self, x: int, y: int) -> None:
        self.flashes += 1
        self.board[y][x] = 0
        for _y in range(y - 1, y + 2):
            if _y < 0 or _y >= board_size:
                continue
            for _x in range(x - 1, x + 2):
                if _x < 0 or _x >= board_size or self.board[_y][_x] == 0:
                    continue
                self.board[_y][_x] += 1
                if self.board[_y][_x] > 9:
                    self.flash(_x, _y)


config = OctopusConfig()
with open(path) as file:
    for line in file.readlines():
        config.add_input_line(line)

for i in range(steps):
    config.do_step()

while not config.first_full_flash:
    config.do_step()

print(f'Part 1: {config.flashes}')
print(f'Part 2: {config.first_full_flash}')
