# -*- coding: utf-8 -*-

from pathlib import Path
from re import search, sub
from typing import Any, List


def walk_directories(input_path: Path, output_path: Path, type_files_join: Any) -> None:
    print("INFO: Browsing through directories to combine")

    input_path_name = input_path.name
    files_to_combine = []
    files_root_folder = []

    for item in input_path.glob("*"):
        directory_group = []
        if item.is_dir() and not item.name.startswith('.'):
            for element in item.iterdir():
                if element.is_file() and valid_file_combine(element.name, type_files_join):
                    directory_group.append(element)
            if directory_group:
                files_to_combine.append(directory_group)
        elif item.is_file() and not item.name.startswith('.') and valid_file_combine(item.name, type_files_join):
            files_root_folder.append(item)
        else:
            continue
    if files_root_folder:
        files_to_combine.append(files_root_folder)

    combine_files(type_files_join, files_to_combine, input_path_name, output_path)


def valid_file_combine(name: str, type_files_join) -> bool:
    pattern = f"\\-{type_files_join}\\-"

    result = search(pattern, name)
    if result:
        return True
    else:
        return False


def combine_files(type_files_join: str, file_groups: List[List[Path]], input_folder_name: str, output_path: Path) -> None:
    print(f"INFO: Combining {type_files_join} files")

    for file_group in file_groups:
        raw_file_name = file_group[0].name
        raw_file_name_suffix = file_group[0].suffix
        raw_file_parent_name = file_group[0].parent.name
        output_file_name = f"{raw_file_name[:-(len(raw_file_name_suffix) + 2)]}{raw_file_name_suffix}"

        if raw_file_parent_name != input_folder_name:
            file_folder = output_path.joinpath(raw_file_parent_name)
            file_folder.mkdir(parents=True, exist_ok=True)
            output_file = file_folder.joinpath(output_file_name)
        else:
            output_file = output_path.joinpath(output_file_name)

        with open(output_file, 'wt', encoding='UTF-8', errors="replace") as output_stream:
            for file in file_group:
                with open(file, 'rt', encoding='UTF-8', errors="replace") as input_stream:
                    original = input_stream.read()
                    removed_double_empty_lines = sub(r'[\r\n][\r\n]{2,}', '\n', original)
                    output_stream.write(removed_double_empty_lines)
        print(f"INFO: Files of type {type_files_join} have been correctly combined into {output_file}")
