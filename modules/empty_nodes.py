# -*- coding: utf-8 -*-

from pathlib import Path
from re import search
from typing import List, TextIO

from modules.utils import search_files


def walk_directories(input_path: Path, output_path: Path) -> None:
    print("INFO: Browsing through directories to convert")

    input_path_name = input_path.name
    files = search_files(input_path)
    remove_empty_nodes(files, input_path_name, output_path)


def remove_empty_nodes(files: List[Path], input_path_name: str, output_path: Path) -> None:
    print("INFO: Converting files")

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
            remove(file, output_file)


def remove(input_file: Path, output_file: Path) -> None:
    print(f"INFO: Removing sentences with empty nodes from {input_file} file to {output_file} file")

    sentence_lines = []
    with open(input_file, 'rt', encoding='UTF-8', errors="replace") as dirty, open(output_file, 'wt', encoding='UTF-8',
                                                                                   errors="replace") as cleaned:
        for line in dirty:
            if line != "\n":
                sentence_lines.append(line)
            else:
                empty_nodes = detect_empty_nodes(sentence_lines)
                if not empty_nodes:
                    write_sentence(sentence_lines, cleaned, last_sentence=False)
                    sentence_lines = []
                else:
                    sentence_lines = []

    empty_nodes = detect_empty_nodes(sentence_lines)
    if not empty_nodes:
        with open(output_file, 'at', encoding='UTF-8', errors="replace") as cleaned:
            write_sentence(sentence_lines, cleaned, last_sentence=True)


def detect_empty_nodes(sentence_lines: List[str]) -> bool:
    for sentence_line in sentence_lines:
        if sentence_line.startswith("#"):
            continue
        else:
            tuples = sentence_line.split("\t")
            if "." in tuples[0]:
                return True
            else:
                continue

    return False


def write_sentence(sentence_lines: List[str], cleaned: TextIO, last_sentence: bool) -> None:
    for sentence_line in sentence_lines:
        cleaned.write(sentence_line)

    if not last_sentence:
        cleaned.write("\n")
