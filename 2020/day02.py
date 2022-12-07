part_1 = 0
part_2 = 0
with open('../data/2020/day02.txt') as file:
    for line in file.readlines():
        min_max, char_, password = line.strip().split(' ')
        __min, __max = min_max.split('-')
        _min, _max = int(__min), int(__max)
        char = char_[0]
        if _min <= password.count(char) <= _max:
            part_1 += 1
        _len = len(password)
        if (_min <= _len and password[_min - 1] == char) != (_max <= _len and password[_max - 1] == char):
            part_2 += 1

print(f'Part 1: {part_1}')
print(f'Part 2: {part_2}')
