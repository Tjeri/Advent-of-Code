from __future__ import annotations

import re
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Pattern

from aoc.input import read_split_input

split_pattern: Pattern[str] = re.compile(' \\| | ')


def collect_rules(rule_lines: list[str]) -> dict[int, tuple[set[int], str]]:
    rules: dict[int, tuple[set[int], str]] = {}
    for line in rule_lines:
        __id, rule_text = line.split(': ')
        _id = int(__id)
        if '"' in rule_text:
            rules[_id] = (set(), rule_text[1])
            continue
        depends_on = {int(part) for part in re.split(split_pattern, rule_text)}
        rules[_id] = (depends_on, rule_text)
    return rules


def collect_dependencies(rules: dict[int, tuple[set[int], str]]) -> dict[int | None, set[int]]:
    dependencies = {}
    for rule_id, (depends_on, _) in rules.items():
        if not depends_on:
            dependencies.setdefault(None, set()).add(rule_id)
        for dependency_id in depends_on:
            dependencies.setdefault(dependency_id, set()).add(rule_id)
    return dependencies


class RegexMatcher:
    rules: list[Pattern[str]]

    def __init__(self) -> None:
        self.rules = []

    def parse_rules(self, rule_lines: list[str]) -> None:
        unfinished_rules = collect_rules(rule_lines)
        dependencies = collect_dependencies(unfinished_rules)
        parsed_rules: dict[int, str] = {}
        for rule_id in dependencies[None]:
            parsed_rules[rule_id] = unfinished_rules[rule_id][1]
            del unfinished_rules[rule_id]
        del dependencies[None]

        ready: list[int] = list(parsed_rules.keys())
        while ready:
            rule_id = ready.pop(0)
            for depending in dependencies.get(rule_id, []):
                depends_on, text = unfinished_rules[depending]
                depends_on.remove(rule_id)
                if not depends_on:
                    del unfinished_rules[depending]
                    rule = self._replace_rule(text, parsed_rules)
                    self._add_rule(parsed_rules, depending, rule)
                    ready.append(depending)
        self.rules = [re.compile(rule) for rule in parsed_rules.values()]

    def validate(self, message: str) -> bool:
        for rule in self.rules:
            if self._check_rule(message, rule):
                return True
        return False

    def _add_rule(self, rules: dict[int, str], rule_id: int, rule: str) -> None:
        rules[rule_id] = rule

    def _check_rule(self, message: str, rule: Pattern[str]) -> bool:
        return bool(re.fullmatch(rule, message))

    @staticmethod
    def _replace_rule(rule: str, rules: dict[int, str]) -> str:
        sides = rule.split(' | ')
        replaced = []
        for side in sides:
            replaced.append(''.join([rules[int(_id)] for _id in side.split(' ')]))
        return f'({"|".join(replaced)})'


class Matcher(ABC):
    @abstractmethod
    def matches(self, text: str) -> tuple[bool, int]:
        pass

    @abstractmethod
    def fully_matches(self, text: str) -> bool:
        pass

    @abstractmethod
    def get_all_matches(self, text: str) -> list[int]:
        pass

    def get_full_matches(self, text: str) -> list[int]:
        return [match for match in self.get_all_matches(text) if match == len(text)]

    @staticmethod
    def parse_rules(rule_lines: list[str], use_recursive: bool = False) -> dict[int, Matcher]:
        unfinished_rules = collect_rules(rule_lines)
        dependencies = collect_dependencies(unfinished_rules)

        matchers: dict[int, Matcher] = {}
        for rule_id in dependencies[None]:
            matchers[rule_id] = StringMatcher(unfinished_rules[rule_id][1])
            del unfinished_rules[rule_id]
        del dependencies[None]

        ready: list[int] = list(matchers.keys())
        while ready:
            rule_id = ready.pop(0)
            for depending in dependencies.get(rule_id, []):
                depends_on, text = unfinished_rules[depending]
                depends_on.remove(rule_id)
                if not depends_on:
                    del unfinished_rules[depending]
                    matcher = Matcher.parse_rule(text, matchers)
                    if use_recursive:
                        if depending == 8:
                            matcher = RecursiveMatcher8(matcher)
                        elif depending == 11:
                            matcher = RecursiveMatcher11(matcher)
                    matchers[depending] = matcher
                    ready.append(depending)
        return matchers

    @staticmethod
    def parse_rule(rule: str, rules: dict[int, Matcher]) -> Matcher:
        matchers = []
        if '|' in rule:
            for side in rule.split(' | '):
                matchers.append(Matcher.parse_rule(side, rules))
            return OrMatcher(matchers)
        if ' ' in rule:
            for part in rule.split(' '):
                matchers.append(rules[int(part)])
            if all(isinstance(matcher, StringMatcher) for matcher in matchers):
                return StringMatcher(''.join(matcher.match for matcher in matchers))
            return ConcatMatcher(matchers)
        return rules[int(rule)]


@dataclass
class StringMatcher(Matcher):
    match: str

    def matches(self, text: str) -> tuple[bool, int]:
        return text.startswith(self.match), len(self.match)

    def fully_matches(self, text: str) -> bool:
        return text == self.match

    def get_all_matches(self, text: str) -> list[int]:
        return [len(self.match)] if text.startswith(self.match) else []


@dataclass
class ConcatMatcher(Matcher):
    matchers: list[Matcher]

    def matches(self, text: str) -> tuple[bool, int]:
        index = 0
        for matcher in self.matchers:
            matches, consumes = matcher.matches(text[index:])
            if not matches:
                return False, 0
            index += consumes
        return True, index

    def fully_matches(self, text: str) -> bool:
        matches, consumes = self.matches(text)
        return matches and len(text) == consumes

    def get_all_matches(self, text: str) -> list[int]:
        matches = self.matchers[0].get_all_matches(text)
        if not matches:
            return []
        for matcher in self.matchers[1:]:
            new_matches = []
            for old_match in matches:
                matcher_matches = matcher.get_all_matches(text[old_match:])
                new_matches += [old_match + new_match for new_match in matcher_matches]
            if not new_matches:
                return []
            matches = new_matches
        return matches


@dataclass
class OrMatcher(Matcher):
    matchers: list[Matcher]

    def matches(self, text: str) -> tuple[bool, int]:
        for matcher in self.matchers:
            matches, consumes = matcher.matches(text)
            if matches:
                return matches, consumes
        return False, 0

    def fully_matches(self, text: str) -> bool:
        for matcher in self.matchers:
            matches, consumes = matcher.matches(text)
            if matches and consumes == len(text):
                return True
        return False

    def get_all_matches(self, text: str) -> list[int]:
        matches = []
        for matcher in self.matchers:
            matches += matcher.get_all_matches(text)
        return matches

    def get_full_matches(self, text: str) -> list[int]:
        return [match for match in self.get_all_matches(text) if match == len(text)]


class RecursiveMatcher8(Matcher):
    matcher: Matcher

    def __init__(self, matcher: Matcher) -> None:
        self.matcher = OrMatcher([matcher, ConcatMatcher([matcher, self])])

    def matches(self, text: str) -> tuple[bool, int]:
        return self.matcher.matches(text)

    def fully_matches(self, text: str) -> bool:
        return self.matcher.fully_matches(text)

    def get_all_matches(self, text: str) -> list[int]:
        return self.matcher.get_all_matches(text)


class RecursiveMatcher11(Matcher):
    matcher: Matcher

    def __init__(self, matcher: Matcher) -> None:
        if not isinstance(matcher, ConcatMatcher):
            raise ValueError
        self.matcher = OrMatcher([matcher, ConcatMatcher([matcher.matchers[0], self, matcher.matchers[1]])])

    def matches(self, text: str) -> tuple[bool, int]:
        return self.matcher.matches(text)

    def fully_matches(self, text: str) -> bool:
        return self.matcher.fully_matches(text)

    def get_all_matches(self, text: str) -> list[int]:
        return self.matcher.get_all_matches(text)


def part1_regex(rules_lines: list[str], messages: list[str]) -> int:
    matcher = RegexMatcher()
    matcher.parse_rules(rules_lines)
    matching = 0
    for message in messages:
        if matcher.validate(message):
            matching += 1
    return matching


def part1_custom(rules_line: list[str], messages: list[str]) -> int:
    matcher = OrMatcher(list(Matcher.parse_rules(rules_line).values()))
    matching = 0
    for message in messages:
        if matcher.fully_matches(message):
            matching += 1
    return matching


def part2_custom(rules_line: list[str], messages: list[str]) -> int:
    matcher = OrMatcher(list(Matcher.parse_rules(rules_line, True).values()))
    matching = 0
    for message in messages:
        if matcher.get_full_matches(message):
            matching += 1
    return matching


_groups = read_split_input()
print(f'Part 1 (regex): {part1_regex(*_groups)}')
print(f'Part 1 (custom): {part1_custom(*_groups)}')
print(f'Part 2: {part2_custom(*_groups)}')
