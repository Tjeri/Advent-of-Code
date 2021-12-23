file_name = 'data/day14.txt'

start = None
rules: dict[str, str] = dict()
with open(file_name) as file:
    for line in file.readlines():
        line = line.strip()
        if start is None:
            start = line
            continue
        if not len(line):
            continue
        key, value = line.split(' -> ')
        rules[key] = value

pairs: dict[str, int] = dict()
for i in range(1, len(start)):
    pair = start[i - 1: i + 1]
    pairs[pair] = pairs.get(pair, 0) + 1


def do_quick_insertions(_pairs):
    new_pairs: dict[str, int] = dict()
    for _pair, amount in _pairs.items():
        insert = rules.get(_pair)
        if insert is None:
            new_pairs[_pair] = new_pairs.get(_pair, 0) + amount
        else:
            pair1 = _pair[0] + insert
            pair2 = insert + _pair[1]
            new_pairs[pair1] = new_pairs.get(pair1, 0) + amount
            new_pairs[pair2] = new_pairs.get(pair2, 0) + amount
    return new_pairs


def count_elements() -> dict[str, int]:
    count: dict[str, int] = dict()
    for _pair, amount in pairs.items():
        count[_pair[0]] = count.get(_pair[0], 0) + amount
    count[start[-1]] = count.get(start[-1], 0) + 1
    return count


def get_min_max() -> tuple[int, int]:
    _min = None
    _max = None
    for _, val in count_elements().items():
        if _min is None or val < _min:
            _min = val
        if _max is None or val > _max:
            _max = val
    return _min, _max


for _ in range(10):
    pairs = do_quick_insertions(pairs)
__min, __max = get_min_max()
print(f'Part 1: {__max - __min}')

for _ in range(30):
    pairs = do_quick_insertions(pairs)
__min, __max = get_min_max()
print(f'Part 2: {__max - __min}')
