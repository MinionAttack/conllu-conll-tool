# -*- coding: utf-8 -*-

from pathlib import Path
from typing import List

from .utils import search_files_pattern


def walk_directories(input_folder: Path, output_folder: Path, column_from: int, column_to: int) -> None:
    print("INFO: Browsing through directories to swap columns")

    pattern = '\\.conllu$'
    input_path_name = input_folder.name
    files = search_files_pattern(input_folder, pattern)

    swap_columns(files, input_path_name, column_from, column_to, output_folder)


def swap_columns(files: List[Path], input_path_name: str, column_from: int, column_to: int, output_path: Path) -> None:
    print("INFO: Swapping columns")

    for file in files:
        file_folder_name = file.parent.name
        if file_folder_name != input_path_name:
            file_folder = output_path.joinpath(file_folder_name)
            file_folder.mkdir(parents=True, exist_ok=True)
            output_file = file_folder.joinpath(file.name)
        else:
            output_file = output_path.joinpath(file.name)
        swap(file, column_from, column_to, output_file)


def swap(file: Path, column_from: int, column_to: int, output_file: Path) -> None:
    with open(file, 'rt', encoding='UTF-8', errors="replace") as actual_file, open(output_file, 'wt', encoding='UTF-8',
                                                                                   errors="replace") as new_file:
        for line in actual_file:
            if not line.startswith("#"):
                if line != "\n":
                    line = line.replace("\n", "")
                    tuples = line.split("\t")
                    tuples[column_from], tuples[column_to] = tuples[column_to], tuples[column_from]
                    new_line = '\t'.join(tuples) + '\n'
                    new_file.write(new_line)
                else:
                    new_file.write('\n')
            else:
                new_file.write(line)
