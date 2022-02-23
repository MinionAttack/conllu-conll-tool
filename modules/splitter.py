# -*- coding: utf-8 -*-

from decimal import getcontext, ROUND_HALF_UP, Decimal
from pathlib import Path
from random import sample
from re import search
from typing import List, Tuple

from modules.utils import get_blocks_file


def walk_directories(input_path: Path, output_path: Path) -> None:
    print("INFO: Browsing through directories to split")

    input_path_name = input_path.name
    files = []

    for item in input_path.glob("*"):
        if item.is_dir() and not item.name.startswith('.'):
            for element in item.iterdir():
                if element.is_file() and valid_file_split(element.name):
                    files.append(element)
        elif item.is_file() and not item.name.startswith('.') and valid_file_split(item.name):
            files.append(item)
        else:
            continue

    split_training_files(files, input_path_name, output_path)


def valid_file_split(name: str) -> bool:
    pattern = '\\-train\\.conllu$'

    result = search(pattern, name)
    if result:
        return True
    else:
        return False


def split_training_files(files: List[Path], input_path_name: str, output_path: Path) -> None:
    print("INFO: Splitting the training files")

    for file in files:
        name = file.name
        file_folder_name = file.parent.name
        if file_folder_name != input_path_name:
            file_folder = output_path.joinpath(file_folder_name)
            file_folder.mkdir(parents=True, exist_ok=True)
            output_training_file = file_folder.joinpath(name)
            validation_name = name.replace("-train.", "-dev.")
            output_validation_file = file_folder.joinpath(validation_name)
        else:
            output_training_file = output_path.joinpath(name)
            validation_name = name.replace("-train.", "-dev.")
            output_validation_file = output_path.joinpath(validation_name)
        split_file(file, output_training_file, output_validation_file)


def split_file(training_file: Path, new_training_file: Path, validation_file: Path) -> None:
    print(f"INFO: Splitting {training_file} file")

    blocks = get_blocks_file(training_file)
    training_collection, validation_collection = select_random_blocks(blocks)
    if training_collection and validation_collection:
        write_split_data(new_training_file, training_collection)
        write_split_data(validation_file, validation_collection)


def select_random_blocks(blocks: List[str]) -> Tuple[List[str], List[str]]:
    print(f"INFO: Selecting random data")

    # The file is divided into a ratio of 80% training and 20% validation
    total_blocks = len(blocks)
    context = getcontext()
    context.rounding = ROUND_HALF_UP
    number_training_items = int(round(Decimal(0.8 * total_blocks), 0))
    try:
        training_collection = sample(blocks, number_training_items)
        validation_collection = [block for block in blocks if block not in training_collection]
    except ValueError:
        print(f"WARNING: The file does not contain enough sentences to make an 80-20 split, skipping")
        training_collection = []
        validation_collection = []

    return training_collection, validation_collection


def write_split_data(new_file: Path, data_collection: List[str]) -> None:
    print(f"INFO: Writing data to file {new_file}")

    with open(new_file, 'wt', encoding='UTF-8', errors="replace") as output:
        for block in data_collection:
            output.write(block)
