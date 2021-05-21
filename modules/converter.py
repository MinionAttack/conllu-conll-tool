# -*- coding: utf-8 -*-

import re
from pathlib import Path
from typing import List


def walk_directories_convert(input_path: Path, output_path: Path) -> None:
    print("INFO: Browsing through directories to convert")

    input_path_name = input_path.name
    files = []

    for item in input_path.glob("*"):
        if item.is_dir() and not item.name.startswith('.'):
            for element in item.iterdir():
                if element.is_file():
                    files.append(element)
        elif item.is_file() and not item.name.startswith('.'):
            files.append(item)
        else:
            continue

    convert_files(files, input_path_name, output_path)


def convert_files(files: List[Path], input_path_name: str, output_path: Path) -> None:
    print("INFO: Converting files")

    pattern = '\\-(train|test|dev)\\.conllu$'
    for file in files:
        name = file.name
        result = re.search(pattern, name)
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


def convert_file(input_file, output_file) -> None:
    print(f"INFO: Converting {input_file} file to {output_file} file")

    with open(input_file, 'r') as conllu, open(output_file, 'w') as conll:
        lines = conllu.readlines()
        for line in lines:
            tuples = line.split()
            if len(tuples) == 10 and tuples[0] != '#' and '.' not in tuples[0] and '-' not in tuples[0]:
                tuples[8] = tuples[9] = '_'
                conll.write('\t'.join(tuples) + '\n')
            if len(tuples) == 0:
                conll.write('\n')
