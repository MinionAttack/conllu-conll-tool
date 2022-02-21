# -*- coding: utf-8 -*-

from pathlib import Path
from shutil import copyfile
from tempfile import NamedTemporaryFile
from typing import List, Any

import numpy as numpy

from .utils import search_files


def validate_parameters(tag_name: str) -> bool:
    print("INFO: Validating parameters")

    return tag_name.isalpha()


def walk_directories(input_path: Path, label: str, dimension: int, position: Any) -> None:
    print("INFO: Browsing through directories to fill in")

    files = search_files(input_path)
    fill_files(files, label, dimension, position)


def fill_files(files: List[Path], label: str, dimension: int, position: Any) -> None:
    print("INFO: Filling in the files")

    for file in files:
        has_unknown_tag = check_unknown_tag(file, label, position)
        if not has_unknown_tag:
            fill_file(file, label, dimension, position)
        else:
            print(f"INFO: {file} file already has the {label} tag, skipping")


def check_unknown_tag(input_file, tag_name, position: Any) -> bool:
    print(f"INFO: Checking if {input_file} file already has the {tag_name} tag")

    exists = False
    line_number = 1
    with open(input_file, 'rt', encoding='UTF-8', errors="replace") as file:
        for line in file:
            pieces = line.split()
            if len(pieces) > 0:
                word = pieces[0]
                if (word == tag_name and position is None) or (word == tag_name and line_number <= position):
                    exists = True
                    break
                else:
                    line_number += 1
            else:
                continue

    return exists


def fill_file(input_file: Path, label: str, dimension: int, position: Any) -> None:
    print(f"INFO: Filling in {input_file} file with {label} tag for {dimension} dimension(s)")

    vector_values = generate_vector(dimension)
    joined_values = ' '.join("%1.6f" % vector_value for vector_value in vector_values)

    if len(vector_values) > 0:
        print(f"INFO: Writing data to file")
        line = f"{label} {joined_values}"
        if position is None:
            add_end_file(input_file, line)
        else:
            add_specific_position(input_file, line, position)


def generate_vector(dimension: int) -> Any:
    print(f"INFO: Generating vector of random numbers with a dimension of {dimension}")

    low_side = -(1 / (2 * dimension))
    high_side = 1 / (2 * dimension)
    # Fixed seed to be able to reproduce the experiments
    random_generator = numpy.random.default_rng(42)
    values = random_generator.uniform(low_side, high_side, dimension)

    return values


def add_end_file(input_file: Path, line: str) -> None:
    with open(input_file, 'at', encoding='UTF-8', errors="replace") as file:
        file.write(line)


# https://stackoverflow.com/a/62366144/3522933
def add_specific_position(input_file: Path, line: str, position: int) -> None:
    with open(input_file, 'rt', encoding='UTF-8', errors="replace") as file:
        destination = NamedTemporaryFile(mode="wt", dir=str(input_file.parent))
        lineno = 1

        while lineno < position:
            destination.file.write(file.readline())
            lineno += 1

        # Insert the new data.
        destination.file.write(f"{line}\n")

        # Write the rest in chunks.
        while True:
            data = file.read(1024)
            if not data:
                break
            destination.file.write(data)
    # Finish writing data.
    destination.flush()
    # Overwrite the original file's contents with that of the temporary file.
    # This uses a memory-optimised copy operation starting from Python 3.8.
    copyfile(destination.name, str(input_file))
    # Delete the temporary file.
    destination.close()
