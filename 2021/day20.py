from __future__ import annotations


class Image:
    enhancement_algorithm: str
    rows: list[str]
    outside_bounds: str

    def __init__(self, enhancement_algorithm: str, raw_map: list[str]) -> None:
        self.enhancement_algorithm = self.replace_original_string_format(enhancement_algorithm.strip())
        self.rows = []
        for line in raw_map:
            self.rows.append(self.replace_original_string_format(line.strip()))
        self.outside_bounds = '0'

    def __str__(self) -> str:
        result = ''
        for row in self.rows:
            result += row.replace('1', '#').replace('0', '.') + '\n'
        return result

    @property
    def lit_pixels(self) -> int:
        count = 0
        for row in self.rows:
            count += row.count('1')
        return count

    @staticmethod
    def replace_original_string_format(original: str) -> str:
        return original.replace('.', '0').replace('#', '1')

    def enhance_image(self) -> None:
        new_rows: list[str] = []
        for y in range(-1, len(self.rows) + 1):
            row = ''
            for x in range(-1, len(self.rows[0]) + 1):
                row += self.get_enhanced_pixel(x, y)
            new_rows.append(row)
        self.rows = new_rows
        if self.outside_bounds == '0':
            self.outside_bounds = self.enhancement_algorithm[0]
        else:
            self.outside_bounds = self.enhancement_algorithm[-1]

    def get_pixel(self, x: int, y: int) -> str:
        if x < 0 or y < 0 or x >= len(self.rows[0]) or y >= len(self.rows):
            return self.outside_bounds
        return self.rows[y][x]

    def get_enhanced_pixel(self, x: int, y: int) -> str:
        pixels = ''
        for _y in range(y - 1, y + 2):
            for _x in range(x - 1, x + 2):
                pixels += self.get_pixel(_x, _y)
        return self.enhancement_algorithm[int(pixels, 2)]


file_name = '../data/2021/day20.txt'
with open(file_name) as file:
    data = file.readlines()
image = Image(data[0], data[2:])
image.enhance_image()
image.enhance_image()

part1 = image.lit_pixels
print(f'Part 1: {part1}')
for i in range(50 - 2):
    image.enhance_image()
    print(image)
part2 = image.lit_pixels
print(f'Part 2: {part2}')
