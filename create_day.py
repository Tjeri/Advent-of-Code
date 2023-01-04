import os
import sys
from pathlib import Path

import requests

from dotenv import load_dotenv

load_dotenv()

year = sys.argv[1]
day = sys.argv[2]

base_path = Path(year)
base_path.mkdir(exist_ok=True)
file_path = base_path / f'day{day.zfill(2)}.py'
if not file_path.exists():
    with open(file_path, 'x') as file:
        file.write('from aoc.input import read_input\n\n_lines = read_input(False)\n')
data_path = base_path / 'data' / file_path.stem
data_path.mkdir(exist_ok=True)
sample_path = data_path / 'sample'
if not sample_path.exists():
    with open(sample_path, 'x') as file:
        pass
input_path = data_path / 'input'
if not input_path.exists():
    response = requests.get(f'https://adventofcode.com/{year}/day/{day}/input',
                            cookies={'session': os.getenv('SESSION')})
    with open(input_path, 'x') as file:
        file.write(response.text)
