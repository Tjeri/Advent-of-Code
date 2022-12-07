from __future__ import annotations

from dataclasses import dataclass, field

max_dir_size = 100_000
total_disk_space = 70_000_000
needed_space = 30_000_000


@dataclass
class Dir:
    name: str
    parent: Dir | None
    dirs: list[Dir] = field(default_factory=list)
    files: list[File] = field(default_factory=list)
    file_size: int = 0

    @property
    def size(self):
        return self.file_size + sum(_dir.size for _dir in self.dirs)

    def add_dir(self, name: str) -> None:
        self.dirs.append(Dir(name, self))

    def add_file(self, _file: File) -> None:
        self.files.append(_file)
        self.file_size += _file.size

    def get_dir(self, name: str) -> Dir:
        for _dir in self.dirs:
            if _dir.name == name:
                return _dir
        return self

    def crawl(self) -> list[Dir]:
        yield self
        for _dir in self.dirs:
            yield from _dir.crawl()


@dataclass
class File:
    name: str
    size: int


root = Dir('/', None)
pointer = root
with open('../data/2022/day07.txt') as file:
    for line in file.readlines():
        match line.strip().split(' '):
            case '$', 'cd', '/':
                pointer = root
            case '$', 'cd', '..':
                if pointer.parent is not None:
                    pointer = pointer.parent
            case '$', 'cd', _name:
                pointer = pointer.get_dir(_name)
            case '$', 'ls':
                pass
            case 'dir', _name:
                pointer.add_dir(_name)
            case _size, _name:
                pointer.add_file(File(_name, int(_size)))

part_1 = sum([_dir.size for _dir in root.crawl() if _dir.size <= max_dir_size])
print(f'Part 1: {part_1}')

need_to_free = needed_space - (total_disk_space - root.size)
part_2 = min([_dir.size for _dir in root.crawl() if _dir.size >= need_to_free])
print(f'Part 2: {part_2}')
