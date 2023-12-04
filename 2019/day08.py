from aoc.input import read_input


def parse_layers(image_string: str, width: int, height: int) -> list[list[str]]:
    image = []
    area = width * height
    position = len(image) * area
    while position < len(image_string):
        layer_string = image_string[position: position + area]
        layer = []
        for y in range(height):
            layer.append(layer_string[y * width: (y + 1) * width])
        image.append(layer)
        position = len(image) * area
    return image


def count_layer_digits(layer: list[str], digit: str) -> int:
    return sum(line.count(digit) for line in layer)


def solve_part1(image: list[list[str]]) -> int:
    least = 6969
    result = 0
    for layer in image:
        zeros = count_layer_digits(layer, '0')
        if zeros < least:
            result = count_layer_digits(layer, '1') * count_layer_digits(layer, '2')
            least = zeros
    return result


def solve_part2(image: list[list[str]]) -> str:
    result = ''
    for y in range(len(image[0])):
        for x in range(len(image[0][0])):
            pixel = '2'
            for layer in image:
                pixel = layer[y][x]
                if pixel != '2':
                    break
            result += pixel
        result += '\n'
    return result.replace("0", " ").replace("1", "█")


_lines = read_input()
_image = parse_layers(_lines[0], 25, 6)

print(f'Part 1: {solve_part1(_image)}')
print(f'Part 2:\n{solve_part2(_image)}')
