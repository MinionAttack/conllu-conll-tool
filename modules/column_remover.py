# -*- coding: utf-8 -*-

from pathlib import Path
from typing import List

from .utils import search_files_pattern


def walk_directories(input_folder: Path, output_folder: Path, position: int) -> None:
    print("INFO: Browsing through directories to remove column")

    pattern = '\\.conllu$'
    input_path_name = input_folder.name
    files = search_files_pattern(input_folder, pattern)

    remove_column(files, input_path_name, position, output_folder)


def remove_column(files: List[Path], input_path_name: str, position: int, output_path: Path) -> None:
    print("INFO: Removing column")

    for file in files:
        file_folder_name = file.parent.name
        if file_folder_name != input_path_name:
            file_folder = output_path.joinpath(file_folder_name)
            file_folder.mkdir(parents=True, exist_ok=True)
            output_file = file_folder.joinpath(file.name)
        else:
            output_file = output_path.joinpath(file.name)
        remove(file, position, output_file)


def remove(file: Path, position: int, output_file: Path) -> None:
    with open(file, 'rt', encoding='UTF-8', errors="replace") as actual_file, open(output_file, 'wt', encoding='UTF-8',
                                                                                   errors="replace") as new_file:
        for line in actual_file:
            if not line.startswith("#"):
                if line != "\n":
                    line = line.replace("\n", "")
                    tuples = line.split("\t")
                    del tuples[position]
                    new_line = '\t'.join(tuples) + '\n'
                    new_file.write(new_line)
                else:
                    new_file.write('\n')
            else:
                new_file.write(line)
