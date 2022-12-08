def get_seat_id(boarding_pass: str) -> int:
    min_row, max_row, min_col, max_col = 0, 127, 0, 7
    for char in boarding_pass:
        if char == 'F':
            max_row = (min_row + max_row) // 2
        elif char == 'B':
            min_row = (min_row + max_row) // 2 + 1
        elif char == 'L':
            max_col = (min_col + max_col) // 2
        elif char == 'R':
            min_col = (min_col + max_col) // 2 + 1
    return min_row * 8 + min_col


seats = []
with open('../data/2020/day05.txt') as file:
    for line in file.readlines():
        seats.append(get_seat_id(line.strip()))

seats.sort()
print(f'Part 1: {seats[-1]}')
for i in range(0, len(seats) - 1):
    if seats[i] + 1 == seats[i + 1] - 1:
        print(f'Part 2: {seats[i] + 1}')
        break
