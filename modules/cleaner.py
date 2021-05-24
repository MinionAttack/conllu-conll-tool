# -*- coding: utf-8 -*-

from pathlib import Path
from typing import List


def walk_directories(input_path: Path, output_path: Path) -> None:
    print("INFO: Browsing through directories to clean")

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

    clean_files(files, input_path_name, output_path)


def clean_files(files: List[Path], input_path_name: str, output_path: Path) -> None:
    print("INFO: Cleaning files")

    for file in files:
        name = file.name
        file_folder_name = file.parent.name
        if file_folder_name != input_path_name:
            file_folder = output_path.joinpath(file_folder_name)
            file_folder.mkdir(parents=True, exist_ok=True)
            output_file = file_folder.joinpath(name)
        else:
            output_file = output_path.joinpath(name)
        clean_file(file, output_file)


def clean_file(input_file: Path, output_file: Path) -> None:
    print(f"INFO: Cleaning {input_file} file to {output_file} file")

    # UD embeddings are in iso-8859-1 (latin1)
    with open(input_file, 'r', encoding='iso-8859-1') as dirty, open(output_file, 'w', encoding='iso-8859-1') as clean:
        try:
            for line in dirty:
                tuples = line.split()
                if len(tuples) == 2 and is_a_number(tuples[0]) and is_a_number(tuples[1]):
                    continue
                else:
                    clean.write(line)
        except UnicodeDecodeError as error:
            print(f"ERROR: Unable to clean {input_file} file, {error.encoding} - {error.reason}")


def is_a_number(number: str) -> bool:
    try:
        int(number)
        return True
    except ValueError:
        return False
