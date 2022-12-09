sum_1 = 0
sum_2 = 0
with open('../data/2020/day06.txt') as file:
    group_1 = set()
    group_2 = None
    for line in file.readlines():
        line = line.strip()
        if line:
            group_1.update(line)
            if group_2 is None:
                group_2 = set(line)
            else:
                group_2.intersection_update(line)
        else:
            sum_1 += len(group_1)
            sum_2 += len(group_2)
            group_1 = set()
            group_2 = None
    sum_1 += len(group_1)
    sum_2 += len(group_2)

print(f'Part 1: {sum_1}')
print(f'Part 2: {sum_2}')
