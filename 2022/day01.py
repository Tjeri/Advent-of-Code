highest = [0, 0, 0]
current = 0
with open('../data/2022/day01.txt') as file:
    for line in file.readlines():
        line = line.strip()
        if line:
            current += int(line)
        else:
            pos = 0
            for i in range(3):
                if current > highest[i]:
                    pos = i + 1
            if pos:
                highest.insert(pos, current)
                highest.pop(0)
            current = 0

print(f'Part 1: {highest[2]}')
print(f'Part 2: {sum(highest)}')
