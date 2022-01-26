# -*- coding: utf-8 -*-

from pathlib import Path
from re import search
from typing import List

from modules.utils import search_files


def walk_directories(input_path: Path, output_path: Path, keep_content: bool) -> None:
    print("INFO: Browsing through directories to convert")

    input_path_name = input_path.name
    files = search_files(input_path)
    fill_enhanced_column(files, input_path_name, output_path, keep_content)


def fill_enhanced_column(files: List[Path], input_path_name: str, output_path: Path, keep_content: bool) -> None:
    print("INFO: Enhancing files")

    pattern = '\\-(train|test|dev)\\.conllu$'
    for file in files:
        name = file.name
        result = search(pattern, name)
        if result:
            file_folder_name = file.parent.name
            if file_folder_name != input_path_name:
                file_folder = output_path.joinpath(file_folder_name)
                file_folder.mkdir(parents=True, exist_ok=True)
                output_file = file_folder.joinpath(name)
            else:
                output_file = output_path.joinpath(name)
            enhance(file, output_file, keep_content)


def enhance(input_file: Path, output_file: Path, keep_content: bool) -> None:
    print(f"INFO: Enhancing sentences from {input_file} file to {output_file} file")

    with open(input_file, 'rt', encoding='UTF-8', errors="replace") as actual_file, open(output_file, 'wt', encoding='UTF-8',
                                                                                         errors="replace") as new_file:
        for line in actual_file:
            if not line.startswith("#"):
                if line != "\n":
                    line = line.replace("\n", "")
                    tuples = line.split("\t")
                    if tuples[8] != "_" and keep_content:
                        content = tuples[8]
                    else:
                        content = f"{tuples[6]}:{tuples[7]}"
                    tuples[8] = content
                    new_line = '\t'.join(tuples) + '\n'
                    new_file.write(new_line)
                else:
                    new_file.write('\n')
            else:
                new_file.write(line)
