#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from pathlib import Path
from typing import Any

from modules import combiner, splitter, converter, cleaner

BASE_PATH = "output"


def main():
    arguments_parser = ArgumentParser(description='Convert conllu files to conll files')
    arguments_parser.add_argument('--input', type=str, required=True, help='Conllu files folder')
    arguments_parser.add_argument('--output', type=str, required=True, help='Conll files folder')
    arguments_parser.add_argument('--combine', choices=['train', 'dev', 'test'], default=None, required=False,
                                  help='Combine multiple files from one phase (train, validation or test) into one file')
    arguments_parser.add_argument('--split', type=bool, default=False, required=False,
                                  help='In case there is no validation file (dev), the training file (train) is split in two with a '
                                       'random 80-20 ratio')
    arguments_parser.add_argument('--clean', type=bool, default=False, required=False,
                                  help='Cleans up an embedding file by removing the first line with the number of words and the vector '
                                       'size')
    arguments = arguments_parser.parse_args()

    conllu_folder = Path(BASE_PATH).joinpath(arguments.input.strip())
    conll_folder = Path(BASE_PATH).joinpath(arguments.output.strip())
    type_to_combine = arguments.combine
    split_train_file = arguments.split
    clean_embedding_file = arguments.clean

    process_folders(conllu_folder, conll_folder, type_to_combine, split_train_file, clean_embedding_file)


def process_folders(input_path: Path, output_path: Path, join_files: Any, split_train_file: bool, clean_embedding_file: bool) -> None:
    print("INFO: Processing directories")

    if input_path.is_dir() and output_path.is_dir():
        if join_files is not None:
            combiner.walk_directories(input_path, output_path, join_files)
        elif split_train_file:
            splitter.walk_directories(input_path, output_path)
        elif clean_embedding_file:
            cleaner.walk_directories(input_path, output_path)
        else:
            converter.walk_directories(input_path, output_path)
    else:
        print("Error: Check that the arguments are folders and not files, and that the folders exist")


if __name__ == "__main__":
    main()
