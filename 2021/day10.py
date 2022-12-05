import math

bracket_pairs = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}
error_points = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}
completion_points = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}

error_score = 0
completion_scores = []
with open('../data/2021/day10.txt') as file:
    for line in file.readlines():
        expected_closing: list[str] = []
        for c in line.strip():
            if c in bracket_pairs:
                expected_closing.append(bracket_pairs[c])
            else:
                if c == expected_closing[-1]:
                    expected_closing.pop()
                else:
                    error_score += error_points[c]
                    expected_closing.clear()
                    break
        if len(expected_closing):
            line_score = 0
            for c in reversed(expected_closing):
                line_score *= 5
                line_score += completion_points[c]
            completion_scores.append(line_score)

print(f'Part 1: {error_score}')

completion_scores.sort()
completion_score = completion_scores[math.floor(len(completion_scores) / 2)]
print(f'Part 2: {completion_score}')
