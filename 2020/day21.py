from __future__ import annotations

import re
from dataclasses import dataclass

from aoc.input import read_input


@dataclass
class Recipe:
    ingredients: set[str]
    allergens: set[str]


class AllergenAssessment:
    RecipePattern = re.compile(r'(?P<ingredients>((\w+) ?)+) \(contains (?P<allergens>((\w+)(, )?)+)\)')

    recipes: list[Recipe]
    ingredients: dict[str, str | None]
    allergens: dict[str, set[str]]

    def __init__(self, recipe_lines: list[str]) -> None:
        self.recipes = []
        self.ingredients = {}
        self.allergens = {}
        self.parse_recipes(recipe_lines)
        self.find_allergens()
        self.filter_allergens()
        self.collect_ingredients()

    def parse_recipes(self, recipe_lines: list[str]) -> None:
        for line in recipe_lines:
            matches = self.RecipePattern.fullmatch(line).groupdict()
            self.recipes.append(Recipe(set(matches['ingredients'].split(' ')), set(matches['allergens'].split(', '))))

    def find_allergens(self) -> None:
        for recipe in self.recipes:
            for allergen in recipe.allergens:
                if allergen not in self.allergens:
                    self.allergens[allergen] = set(recipe.ingredients)
                else:
                    self.allergens[allergen].intersection_update(recipe.ingredients)

    def filter_allergens(self):
        while any(len(ingredients) > 1 for ingredients in self.allergens.values()):
            for allergen, ingredients in self.allergens.items():
                if len(ingredients) == 1:
                    for _allergen, _ingredients in self.allergens.items():
                        if allergen == _allergen:
                            continue
                        _ingredients -= ingredients

    def collect_ingredients(self):
        for recipe in self.recipes:
            for ingredient in recipe.ingredients:
                if ingredient not in self.ingredients:
                    for allergen, _ingredients in self.allergens.items():
                        if next(iter(_ingredients)) == ingredient:
                            self.ingredients[ingredient] = allergen
                            break
                    else:
                        self.ingredients[ingredient] = None

    def part1(self) -> int:
        result = 0
        for ingredient, allergen in self.ingredients.items():
            if allergen is not None:
                continue
            for recipe in self.recipes:
                if ingredient in recipe.ingredients:
                    result += 1
        return result

    def part2(self) -> str:
        return ','.join(next(iter(ingredients)) for allergen, ingredients in sorted(self.allergens.items()))


_lines = read_input()
assessment = AllergenAssessment(_lines)
print(f'Part 1: {assessment.part1()}')
print(f'Part 2: {assessment.part2()}')
