# -*- coding: utf-8 -*-

from pathlib import Path
from re import search
from typing import List

from .utils import search_files


def walk_directories(input_path: Path, output_path: Path) -> None:
    print("INFO: Browsing through directories to convert")

    input_path_name = input_path.name
    files = search_files(input_path)
    convert_files(files, input_path_name, output_path)


def convert_files(files: List[Path], input_path_name: str, output_path: Path) -> None:
    print("INFO: Converting files")

    pattern = '\\-(train|test|dev)\\.conllu$'
    for file in files:
        name = file.name
        result = search(pattern, name)
        if result:
            output_name = name.replace("conllu", "conll")
            file_folder_name = file.parent.name
            if file_folder_name != input_path_name:
                file_folder = output_path.joinpath(file_folder_name)
                file_folder.mkdir(parents=True, exist_ok=True)
                output_file = file_folder.joinpath(output_name)
            else:
                output_file = output_path.joinpath(output_name)
            convert_file(file, output_file)


def convert_file(input_file: Path, output_file: Path) -> None:
    print(f"INFO: Converting {input_file} file to {output_file} file")

    with open(input_file, 'rt', encoding='UTF-8', errors="replace") as conllu, open(output_file, 'wt', encoding='UTF-8',
                                                                                    errors="replace") as conll:
        for line in conllu:
            if not line.startswith("#"):
                if line != "\n":
                    tuples = line.split("\t")
                    if len(tuples) == 10 and tuples[0] != '#' and '.' not in tuples[0] and '-' not in tuples[0]:
                        tuples[8] = tuples[9] = '_'
                        conll.write('\t'.join(tuples) + '\n')
                else:
                    conll.write('\n')
            else:
                conll.write(line)
