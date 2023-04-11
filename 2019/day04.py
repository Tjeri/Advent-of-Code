from aoc.input import read_input


def is_valid(password: int) -> bool:
    str_pw = str(password)
    last = None
    has_doubled = False
    for char in str_pw:
        if last is None:
            last = char
            continue
        if last == char:
            has_doubled = True
        if last > char:
            return False
        last = char
    return has_doubled


def is_valid_2(password: int) -> bool:
    str_pw = str(password)
    last = None
    digits: dict[str, int] = dict()
    for char in str_pw:
        digits[char] = digits.get(char, 0) + 1
        if last is None:
            last = char
            continue
        if last > char:
            return False
        last = char
    return 2 in digits.values()


_lines = read_input()
_min, _max = [int(_number) for _number in _lines[0].split('-')]

counter1, counter2 = 0, 0
for i in range(_min, _max + 1):
    if is_valid(i):
        counter1 += 1
    if is_valid_2(i):
        counter2 += 1

print(f'Part 1: {counter1}')
print(f'Part 2: {counter2}')
