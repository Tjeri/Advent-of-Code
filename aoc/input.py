import traceback
from pathlib import Path


def read_input(real_input: bool = True, sample_id: str | None = None) -> list[str]:
    path = find_file(real_input, sample_id, -3)
    with open(path) as file:
        return [line.strip() for line in file]


def read_split_input(real_input: bool = True, sample_id: str | None = None) -> list[list[str]]:
    path = find_file(real_input, sample_id, -3)
    with open(path) as file:
        return split_lines([line.strip() for line in file])


def split_lines(lines: list[str]) -> list[list[str]]:
    result = []
    current = []
    for line in lines:
        if not line:
            if current:
                result.append(current)
            current = []
        else:
            current.append(line)
    if current:
        result.append(current)
    return result


def find_file(real_input: bool = True, sample_id: str | None = None, stack_pos: int = -2) -> Path:
    stack = traceback.extract_stack()
    file = Path(stack[stack_pos].filename)
    data_path = file.parent / 'data' / file.stem
    if real_input:
        return data_path / 'input'
    if not sample_id:
        return data_path / 'sample'
    return data_path / f'sample_{sample_id}'
