# -*- coding: utf-8 -*-utils

from pathlib import Path
from typing import List

from .utils import search_files_pattern


def walk_directories(input_path: Path, output_folder: Path) -> None:
    print("INFO: Browsing through directories to generate columns")

    pattern = '\\.conll$'
    input_path_name = input_path.name
    files = search_files_pattern(input_path, pattern)

    generate_columns(files, input_path_name, output_folder)


def generate_columns(files: List[Path], input_path_name: str, output_path: Path) -> None:
    print("INFO: Generating columns")

    for file in files:
        file_folder_name = file.parent.name
        if file_folder_name != input_path_name:
            file_folder = output_path.joinpath(file_folder_name)
            file_folder.mkdir(parents=True, exist_ok=True)
            output_file = file_folder.joinpath(file.name)
        else:
            output_file = output_path.joinpath(file.name)
        generate(file, output_file)


def generate(file: Path, output_file: Path) -> None:
    with open(file, 'rt', encoding='UTF-8', errors="replace") as actual_file, open(output_file, 'wt', encoding='UTF-8',
                                                                                   errors="replace") as new_file:
        for line in actual_file:
            if not line.startswith("#"):
                if line != "\n":
                    line = line.replace("\n", "")
                    tuples = line.split("\t")
                    if len(tuples) < 10:
                        columns_to_generate = 10 - len(tuples)
                        expand_line(tuples, columns_to_generate)
                        new_line = '\t'.join(tuples) + '\n'
                        new_file.write(new_line)
                    else:
                        new_file.write(line)
                else:
                    new_file.write('\n')
            else:
                new_file.write(line)


def expand_line(tuples: List[str], columns_to_generate: int) -> None:
    for _ in range(columns_to_generate):
        tuples.append("_")
