import traceback
from pathlib import Path


def read_input(real_input: bool = True, file_id: str | int | None = None, strip_whitespace: bool = True) -> list[str]:
    path = find_file(real_input, file_id, -3)
    with open(path) as file:
        if strip_whitespace:
            return [line.strip() for line in file]
        else:
            return [line.strip('\n').strip('\r') for line in file]


def read_split_input(real_input: bool = True, file_id: str | int | None = None) -> list[list[str]]:
    path = find_file(real_input, file_id, -3)
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


def find_file(real_input: bool = True, file_id: str | int | None = None, stack_pos: int = -2) -> Path:
    stack = traceback.extract_stack()
    file = Path(stack[stack_pos].filename)
    data_path = file.parent / 'data' / file.stem
    file_name = 'input' if real_input else 'sample'
    if file_id is not None:
        file_name += f'_{file_id}'
    return data_path / file_name
