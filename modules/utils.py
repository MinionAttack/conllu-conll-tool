# -*- coding: utf-8 -*-

from pathlib import Path
from re import search
from typing import List


def search_files_pattern(input_folder: Path, pattern: str) -> List[Path]:
    files = []
    for item in input_folder.glob("*"):
        if item.is_dir() and not item.name.startswith('.'):
            for element in item.iterdir():
                if element.is_file() and search(pattern, element.name):
                    files.append(element)
        elif item.is_file() and not item.name.startswith('.') and search(pattern, item.name):
            files.append(item)
        else:
            continue

    return files


def search_files(input_path: Path) -> List[Path]:
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

    return files


def get_blocks_file(file: Path) -> List[str]:
    print(f"INFO: Reading {file} file")

    blocks = []
    block = ""
    with open(file, 'rt', encoding='UTF-8', errors="replace") as original:
        for line in original:
            if line == "\n":
                block += "\n"
                blocks.append(block)
                block = ""
            else:
                block += line

    return blocks
