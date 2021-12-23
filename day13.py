file_name = 'data/day13.txt'

dots: set[tuple[int, int]] = set()
folds: list[tuple[str, int]] = list()
with open(file_name) as file:
    for line in file.readlines():
        if ',' in line:
            a, b = line.strip().split(',')
            dots.add((int(a), int(b)))
        elif 'fold along' in line:
            where, value = line.strip()[line.index('along') + 6:].split('=')
            folds.append((where, int(value)))


def do_fold(i: int) -> set[tuple[int, int]]:
    fold = folds[i]
    result = set()
    if fold[0] == 'x':
        for x, y in dots:
            if x < fold[1]:
                result.add((x, y))
            else:
                result.add((fold[1] - (x - fold[1]), y))
    else:
        for x, y in dots:
            if y < fold[1]:
                result.add((x, y))
            else:
                result.add((x, fold[1] - (y - fold[1])))
    return result


print(f'Part 1: {len(do_fold(0))}')
for j in range(0, len(folds)):
    dots = do_fold(j)

output = ''
for y in range(0, max(y for x, y in dots) + 1):
    for x in range(0, max(x for x, y in dots) + 1):
        if (x, y) in dots:
            output += '█'
        else:
            output += ' '
    output += '\n'
print('Part 2:')
print(output)

