# -*- coding: utf-8 -*-

from pathlib import Path
from re import search
from typing import List

import numpy


def walk_directories(input_path: Path, output_path: Path, dimensions: int) -> None:
    print("INFO: Browsing through directories to generate")

    pattern = '\\-(train|dev)\\.conllu$'
    input_path_name = input_path.name
    files_to_generate = []
    files_root_folder = []

    for item in input_path.glob("*"):
        directory_group = []
        if item.is_dir() and not item.name.startswith('.'):
            for element in item.iterdir():
                if element.is_file() and search(pattern, element.name) is not None:
                    directory_group.append(element)
            if directory_group:
                files_to_generate.append(directory_group)
        elif item.is_file() and not item.name.startswith('.') and search(pattern, item.name) is not None:
            files_root_folder.append(item)
        else:
            continue
    if files_root_folder:
        files_to_generate.append(files_root_folder)

    generate_files(files_to_generate, dimensions, input_path_name, output_path)


def generate_files(file_groups: List[List[Path]], dimensions: int, input_folder_name: str, output_path: Path) -> None:
    print("INFO: Generating files")

    for file_group in file_groups:
        train_file = file_group[0]
        dev_file = file_group[1]

        raw_file_name = train_file.name
        pieces = raw_file_name.split("_")
        if len(pieces) > 0:
            language_abbreviation = pieces[0]
            output_file_name = f"{language_abbreviation}.vectors"
            raw_file_parent_name = file_group[0].parent.name

            if raw_file_parent_name != input_folder_name:
                file_folder = output_path.joinpath(raw_file_parent_name)
                file_folder.mkdir(parents=True, exist_ok=True)
                output_file = file_folder.joinpath(output_file_name)
            else:
                output_file = output_path.joinpath(output_file_name)

            words = get_words(train_file, dev_file)
            random_embeddings = generate_vectors(words, dimensions)
            write_embeddings(output_file, random_embeddings)
        else:
            print("WARNING: The format of the file name does not correspond to the one used by UD")


def get_words(train_file: Path, dev_file: Path) -> List[str]:
    print(f"INFO: Getting words from {train_file.name} file and {dev_file.name} file")

    train_words = read_file(train_file)
    dev_words = read_file(dev_file)
    unique_words = list(set(train_words + dev_words))

    return unique_words


def read_file(input_file: Path) -> List[str]:
    print(f"INFO: Reading {input_file.name} file")

    words = []
    with open(input_file, 'rt', encoding='UTF-8', errors="replace") as file:
        for line in file:
            pieces = line.split()
            if len(pieces) > 0:
                word = pieces[1]
                words.append(word)
            else:
                continue

    return words


def generate_vectors(words: List[str], dimension: int) -> List[str]:
    print(f"INFO: Generating a random vector with a dimension of {dimension} for each word")

    words_with_vectors = []
    for word in words:
        low_side = -(1 / (2 * dimension))
        high_side = 1 / (2 * dimension)
        # Fixed seed to be able to reproduce the experiments
        random_generator = numpy.random.default_rng(42)
        values = random_generator.uniform(low_side, high_side, dimension)
        result = f"{word} {' '.join('%1.6f' % value for value in values)} "
        words_with_vectors.append(result)

    return words_with_vectors


def write_embeddings(output_file: Path, random_embeddings: List[str]) -> None:
    print(f"INFO: Writing the random embeddings to the {output_file} file")

    with open(output_file, 'wt', encoding='UTF-8', errors="replace") as file:
        for random_embedding in random_embeddings:
            file.write(random_embedding)
            file.write("\n")
