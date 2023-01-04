from aoc.input import read_split_input

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


def read_passports(passport_lines: list[list[str]]) -> list[dict[str, str]]:
    return [read_passport(lines) for lines in passport_lines]


def read_passport(lines: list[str]) -> dict[str, str]:
    passport = dict()
    for line in lines:
        passport.update(map(lambda kv: kv.split(':'), line.split(' ')))
    return passport


def validate_passport_fields(passport: dict[str, str]) -> bool:
    for key, value in passport.items():
        if not validators[key](value):
            return False
    return True


def count_valid_passports(passports: list[dict[str, str]]) -> tuple[int, int]:
    all_required_fields = 0
    actually_valid = 0
    for passport in passports:
        if not required_fields - passport.keys():
            all_required_fields += 1
            if validate_passport_fields(passport):
                actually_valid += 1
    return all_required_fields, actually_valid


part1, part2 = count_valid_passports(read_passports(read_split_input()))
print(f'Part 1: {part1}')
print(f'Part 2: {part2}')
