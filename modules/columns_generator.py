# -*- coding: utf-8 -*-

from pathlib import Path
from re import search
from typing import List


def walk_directories(input_path: Path, output_folder: Path) -> None:
    print("INFO: Browsing through directories to generate columns")

    pattern = '\\.conll$'
    input_path_name = input_path.name
    files = []

    for item in input_path.glob("*"):
        if item.is_dir() and not item.name.startswith('.'):
            for element in item.iterdir():
                if element.is_file() and search(pattern, element.name):
                    files.append(element)
        elif item.is_file() and not item.name.startswith('.') and search(pattern, item.name):
            files.append(item)
        else:
            continue

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
        read_file(file, output_file)


def read_file(file: Path, output_file: Path) -> None:
    with open(file, 'rt', encoding='UTF-8', errors="replace") as actual_file, open(output_file, 'wt', encoding='UTF-8',
                                                                                   errors="replace") as new_file:
        for line in actual_file:
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


def expand_line(tuples: List[str], columns_to_generate: int) -> None:
    for _ in range(columns_to_generate):
        tuples.append("_")
