# -*- coding: utf-8 -*-

from pathlib import Path


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


def clean_files(files, input_path_name, output_path) -> None:
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


def clean_file(input_file, output_file) -> None:
    print(f"INFO: Cleaning {input_file} file to {output_file} file")

    with open(input_file, 'r') as dirty, open(output_file, 'w') as clean:
        for line in dirty:
            tuples = line.split()
            if len(tuples) == 2 and is_a_number(tuples[0]) and is_a_number(tuples[1]):
                continue
            else:
                clean.write(line)


def is_a_number(number: str) -> bool:
    try:
        int(number)
        return True
    except ValueError:
        return False
