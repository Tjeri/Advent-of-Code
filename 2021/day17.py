from dataclasses import dataclass

file_name = '../data/2021/day17.txt'


@dataclass
class Area:
    x_min: int
    x_max: int
    y_min: int
    y_max: int


class Probe:
    x: int = 0
    y: int = 0
    xv: int
    yv: int
    max_y: int = 0
    target_area: Area
    reached_target_area: bool = False

    def __init__(self, xv: int, yv: int, _target_area: Area) -> None:
        self.xv = xv
        self.yv = yv
        self.target_area = _target_area

    def is_in_target_x(self) -> bool:
        return self.target_area.x_min <= self.x <= self.target_area.x_max

    def is_in_target_y(self) -> bool:
        return self.target_area.y_min <= self.y <= self.target_area.y_max

    def should_do_step(self) -> bool:
        if self.xv == 0 and not self.is_in_target_x():
            return False
        if self.yv < 0 and self.y <= self.target_area.y_min:
            return False
        return True

    def do_step(self) -> None:
        self.x += self.xv
        self.y += self.yv
        if self.xv > 0:
            self.xv -= 1
        elif self.xv < 0:
            self.xv += 1
        self.yv -= 1
        if self.y > self.max_y:
            self.max_y = self.y
        if self.is_in_target_x() and self.is_in_target_y():
            self.reached_target_area = True


with open(file_name) as file:
    data = file.readline()
sep_index = data.index(', ')
target_area = Area(
    int(data[data.index('x=') + 2:data.index('..')]),
    int(data[data.index('..') + 2:sep_index]),
    int(data[data.index('y=') + 2:data.index('..', sep_index)]),
    int(data[data.index('..', sep_index) + 2:])
)

part1 = 0
part2 = 0
for start_xv in range(0, target_area.x_max + 1):
    if sum(range(0, start_xv + 1)) < target_area.x_min:
        continue
    for start_yv in range(target_area.y_min, -target_area.y_min):
        probe = Probe(start_xv, start_yv, target_area)
        while probe.should_do_step():
            probe.do_step()
        if probe.reached_target_area:
            part2 += 1
            if probe.max_y > part1:
                part1 = probe.max_y

print(f'Part 1: {part1}')
print(f'Part 2: {part2}')
