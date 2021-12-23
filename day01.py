from typing import Optional

numbers = []
with open('data/day01.txt') as file:
    for line in file.readlines():
        numbers.append(int(line))

increases = 0
last: Optional[int] = None

for number in numbers:
    if last is not None and number > last:
        increases += 1
    last = number

print(f'Part 1: {increases}')

increases = 0
last = None

for i in range(0, len(numbers) - 2):
    _sum = sum(numbers[i:i+3])
    if last is not None and _sum > last:
        increases += 1
    last = _sum

print(f'Part 2: {increases}')
