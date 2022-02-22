# -*- coding: utf-8 -*-

from decimal import getcontext, ROUND_HALF_UP, Decimal
from pathlib import Path
from random import sample
from typing import List

from modules.utils import get_blocks_file


def walk_directories(input_path: Path, output_path: Path, percentages: List[int]) -> None:
    print("INFO: Browsing through directories to extract")

    input_path_name = input_path.name
    files = []

    for item in input_path.glob("*"):
        if item.is_dir() and not item.name.startswith('.'):
            for element in item.iterdir():
                if element.is_file() and element.suffix == ".conllu":
                    files.append(element)
        elif item.is_file() and not item.name.startswith('.') and item.suffix == ".conllu":
            files.append(item)
        else:
            continue

    extract_sentences(files, input_path_name, output_path, percentages)


def extract_sentences(files: List[Path], input_path_name: str, output_path: Path, percentages: List[int]) -> None:
    print("INFO: Extracting sentences from file")

    for file in files:
        for percentage in percentages:
            name = f"{file.stem}-{percentage}{file.suffix}"
            file_folder_name = file.parent.name
            if file_folder_name != input_path_name:
                file_folder = output_path.joinpath(file_folder_name)
                file_folder.mkdir(parents=True, exist_ok=True)
                output_file = file_folder.joinpath(name)
            else:
                output_file = output_path.joinpath(name)
            extract(file, output_file, percentage)


def extract(original_file: Path, output_file: Path, percentage: int) -> None:
    blocks = get_blocks_file(original_file)
    sentences = select_random_blocks(blocks, percentage)
    if sentences:
        write_sentences(output_file, sentences)


def select_random_blocks(blocks: List[str], percentage: int) -> List[str]:
    print(f"INFO: Selecting {percentage}% of random data")

    total_blocks = len(blocks)
    context = getcontext()
    context.rounding = ROUND_HALF_UP
    number_items = int(round(Decimal((percentage / 100) * total_blocks), 0))
    try:
        sentences = sample(blocks, number_items)
    except ValueError:
        print(f"WARNING: The file does not contain enough sentences to select a {percentage}%, skipping")
        sentences = []

    return sentences


def write_sentences(output_file: Path, sentences: List[str]) -> None:
    print(f"INFO: Writing data to file {output_file}")

    with open(output_file, 'wt', encoding='UTF-8', errors="replace") as output:
        for block in sentences:
            output.write(block)
