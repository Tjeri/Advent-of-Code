required_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
validators = {
    'byr': lambda byr: 1920 <= int(byr) <= 2002,
    'iyr': lambda iyr: 2010 <= int(iyr) <= 2020,
    'eyr': lambda eyr: 2020 <= int(eyr) <= 2030,
    'hgt': lambda hgt: hgt[-2:] == 'cm' and 150 <= int(hgt[:-2]) <= 193 or hgt[-2:] == 'in' and 59 <= int(
        hgt[:-2]) <= 76,
    'hcl': lambda hcl: hcl[0] == '#' and int(hcl[1:], 16),
    'ecl': lambda ecl: ecl in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'},
    'pid': lambda pid: len(pid) == 9 and int(pid),
    'cid': lambda cid: True
}


# noinspection PyBroadException
def validate_fields(_fields: dict[str, str]) -> bool:
    try:
        for key, value in _fields.items():
            if not validators[key](value):
                return False
        return True
    except Exception:
        return False


valid_1 = 0
valid_2 = 0
with open('../data/2020/day04.txt') as file:
    fields = dict()
    for line in file.readlines():
        line = line.strip()
        if line:
            for _key, _value in map(lambda kv: kv.split(':'), line.split(' ')):
                fields[_key] = _value
        else:
            if not required_fields - fields.keys():
                valid_1 += 1
                if validate_fields(fields):
                    valid_2 += 1
            fields = dict()

print(f'Part 1: {valid_1}')
print(f'Part 2: {valid_2}')
