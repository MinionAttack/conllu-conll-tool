# -*- coding: utf-8 -*-

from pathlib import Path
from typing import List, Any

import numpy as numpy


def validate_parameters(parameters: List[str]) -> bool:
    print("INFO: Validating parameters")

    tag_name = parameters[0]
    dimensions = parameters[1]

    return tag_name.isalpha() and dimensions.isdecimal()


def walk_directories(input_path: Path, fill_values: List[str]) -> None:
    print("INFO: Browsing through directories to fill in")

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

    fill_files(files, fill_values)


def fill_files(files: List[Path], fill_values: List[str]) -> None:
    print("INFO: Filling in the files")

    tag_name = fill_values[0]
    for file in files:
        has_unknown_tag = check_unknown_tag(file, tag_name)
        if not has_unknown_tag:
            fill_file(file, fill_values)
        else:
            print(f"INFO: {file} file already has the {tag_name} tag, skipping")


def check_unknown_tag(input_file, tag_name) -> bool:
    print(f"INFO: Checking if {input_file} file already has the {tag_name} tag")

    exists = False
    with open(input_file, 'r', encoding='iso-8859-1') as file:
        try:
            for line in file:
                pieces = line.split()
                if len(pieces) > 0:
                    word = pieces[0]
                    if word == tag_name:
                        exists = True
                        break
                    else:
                        continue
                else:
                    continue
        except UnicodeDecodeError as error:
            print(f"ERROR: Unable to get words from {input_file} file, {error.encoding} - {error.reason}")

    return exists


def fill_file(input_file: Path, fill_values: List[str]) -> None:
    print(f"INFO: Filling in {input_file} file with {fill_values[0]} tag for {fill_values[1]} dimension(s)")

    tag_name = fill_values[0]
    dimensions = fill_values[1]
    vector_values = generate_vector(dimensions)
    joined_values = ' '.join("%1.6f" % vector_value for vector_value in vector_values)

    if len(vector_values) > 0:
        print(f"INFO: Writing data to file")
        # UD embeddings are in iso-8859-1 (latin1)
        with open(input_file, 'a', encoding='iso-8859-1') as file:
            try:
                line = f"{tag_name} {joined_values}"
                file.write(line)
            except UnicodeDecodeError as error:
                print(f"ERROR: Unable to fill in {input_file} file, {error.encoding} - {error.reason}")


def generate_vector(dimension: str) -> Any:
    print(f"INFO: Generating vector of random numbers with a dimension of {dimension}")

    if is_a_number(dimension):
        dimension = int(dimension)
        low_side = -(1 / (2 * dimension))
        high_side = 1 / (2 * dimension)
        # Fixed seed to be able to reproduce the experiments
        random_generator = numpy.random.default_rng(42)
        values = random_generator.uniform(low_side, high_side, dimension)

        return values
    else:
        print(f"ERROR: The dimension argument is not a valid number")
        return []


def is_a_number(number: str) -> bool:
    try:
        int(number)
        return True
    except ValueError:
        return False
