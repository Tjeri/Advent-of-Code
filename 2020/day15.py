from aoc.input import read_input

Round = int


class Solver:
    spoken_numbers: dict[int, list[Round]]
    last_number: int
    last_round: int

    def __init__(self, line: str) -> None:
        numbers = list(map(int, line.split(',')))
        self.spoken_numbers = {number: [i] for i, number in enumerate(numbers)}
        self.last_number = numbers[-1]
        self.last_round = len(numbers) - 1

    def speak(self, until_round) -> None:
        for i in range(self.last_round + 1, until_round):
            last_rounds = self.spoken_numbers.get(self.last_number)
            if not last_rounds or len(last_rounds) == 1:
                self.last_number = 0
            else:
                self.last_number = last_rounds[-1] - last_rounds[-2]
            self.spoken_numbers.setdefault(self.last_number, []).append(i)
            self.last_round = i


_lines = read_input()
solver = Solver(_lines[0])
solver.speak(2020)
print(f'Part 1: {solver.last_number}')
solver.speak(30_000_000)
print(f'Part 2: {solver.last_number}')
