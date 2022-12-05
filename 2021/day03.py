digits: int = 0
diagnostics: list[str] = []
with open('../data/2021/day03.txt') as file:
    for line in file.readlines():
        diagnostics.append(line.strip())
digits = len(diagnostics[0])


def count_ones(digit: int, _diagnostics: list[str]) -> int:
    return len([True for x in _diagnostics if x[digit] == '1'])


gamma = ''
epsilon = ''
for i in range(0, digits):
    if count_ones(i, diagnostics) >= len(diagnostics) / 2:
        gamma += '1'
        epsilon += '0'
    else:
        gamma += '0'
        epsilon += '1'

power_consumption = int(gamma, 2) * int(epsilon, 2)
print(f'Part 1: {power_consumption}')

oxygen_generator_rating = None
diagnostics_copy = diagnostics.copy()
for i in range(0, digits):
    ones = count_ones(i, diagnostics_copy)
    most_common = '1' if ones >= len(diagnostics_copy) / 2 else '0'
    diagnostics_copy = list(filter(lambda x: x[i] == most_common, diagnostics_copy))
    if len(diagnostics_copy) == 1:
        oxygen_generator_rating = int(diagnostics_copy[0], 2)
        break

co2_scrubber_rating = None
diagnostics_copy = diagnostics.copy()
for i in range(0, digits):
    ones = count_ones(i, diagnostics_copy)
    least_common = '0' if ones >= len(diagnostics_copy) / 2 else '1'
    diagnostics_copy = list(filter(lambda x: x[i] == least_common, diagnostics_copy))
    if len(diagnostics_copy) == 1:
        co2_scrubber_rating = int(diagnostics_copy[0], 2)
        break

print(f'Part 2: {oxygen_generator_rating * co2_scrubber_rating}')
