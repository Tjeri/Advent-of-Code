class SegmentDeduction:
    def __init__(self, raw_input: str) -> None:
        self.raw_numbers: set[str] = set()
        self.raw_output: list[str] = []
        self.numbers: dict[str, str] = dict()

        self.parse_input(raw_input)
        self.deduce()

        self.output = int(''.join([self.numbers[x] for x in self.raw_output]))

    def parse_input(self, raw_input: str) -> None:
        seperator = raw_input.index(' | ')
        for number in raw_input[:seperator].split(' '):
            self.raw_numbers.add(''.join(sorted(number)))
        for number in raw_input[seperator + 3:].split(' '):
            sorted_number = ''.join(sorted(number))
            self.raw_numbers.add(sorted_number)
            self.raw_output.append(sorted_number)

    def deduce(self) -> None:
        one = next(filter(lambda x: len(x) == 2, self.raw_numbers))
        seven = next(filter(lambda x: len(x) == 3, self.raw_numbers))
        four = next(filter(lambda x: len(x) == 4, self.raw_numbers))
        eight = next(filter(lambda x: len(x) == 7, self.raw_numbers))
        (a,) = set(seven) - set(one)
        nine_filter = set(four) | set(a)
        nine = next(filter(lambda x: len(x) == 6 and len(set(x) - nine_filter) == 1, self.raw_numbers))
        (g,) = set(nine) - nine_filter
        (e,) = set(eight) - set(nine)
        six = next(filter(lambda x: len(x) == 6 and next(iter(set(eight) - set(x))) in one, self.raw_numbers))
        (c,) = set(eight) - set(six)
        (f,) = set(one) - set(c)
        zero = next(filter(lambda x: len(x) == 6 and e in x and c in x, self.raw_numbers))
        (d,) = set(eight) - set(zero)
        (b,) = set(eight) - {a, c, d, e, f, g}
        self.numbers[zero] = '0'
        self.numbers[one] = '1'
        self.numbers[''.join(sorted([a, c, d, e, g]))] = '2'
        self.numbers[''.join(sorted([a, c, d, f, g]))] = '3'
        self.numbers[four] = '4'
        self.numbers[''.join(sorted([a, b, d, f, g]))] = '5'
        self.numbers[six] = '6'
        self.numbers[seven] = '7'
        self.numbers[eight] = '8'
        self.numbers[nine] = '9'


unique_lengths = {2, 3, 4, 7}
count = 0
with open('data/day08.txt') as file:
    for line in file.readlines():
        output = line[line.index(' | ') + 3:].strip()
        for segment in output.split(' '):
            if len(segment) in unique_lengths:
                count += 1

print(f'Part 1: {count}')

segments = []
with open('data/day08.txt') as file:
    for line in file.readlines():
        segments.append(SegmentDeduction(line.strip()))

print(f'Part 2: {sum(segment.output for segment in segments)}')
