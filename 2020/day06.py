from aoc.input import read_split_input


def count_answers(groups: list[list[str]]) -> tuple[int, int]:
    groups_all_answers = 0
    groups_everyone_yes = 0
    for group in groups:
        all_answers = set()
        everyone_yes = None
        for answers in group:
            all_answers.update(answers)
            if everyone_yes is None:
                everyone_yes = set(answers)
            else:
                everyone_yes.intersection_update(answers)
        groups_all_answers += len(all_answers)
        groups_everyone_yes += len(everyone_yes)
    return groups_all_answers, groups_everyone_yes


part1, part2 = count_answers(read_split_input())
print(f'Part 1: {part1}')
print(f'Part 2: {part2}')
