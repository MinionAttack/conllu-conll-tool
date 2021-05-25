#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from argparse import ArgumentParser, Namespace
from pathlib import Path

from modules import combiner, splitter, converter, cleaner, filler

BASE_PATH = "output"


def main():
    arguments_parser = ArgumentParser(description='Convert conllu files to conll files')
    arguments_parser.add_argument('--input', type=str, required=True, help='Input files folder')
    arguments_parser.add_argument('--output', type=str, default=None, required=False, help='Output files folder')
    arguments_parser.add_argument('--combine', choices=['train', 'dev', 'test'], default=None, required=False,
                                  help='Combine multiple files from one phase (train, validation or test) into one file')
    arguments_parser.add_argument('--split', type=bool, default=False, required=False,
                                  help='In case there is no validation file (dev), the training file (train) is split in two with a '
                                       'random 80-20 ratio')
    arguments_parser.add_argument('--clean', type=bool, default=False, required=False,
                                  help='Cleans up an embedding file by removing the first line with the number of words and the vector '
                                       'size')
    arguments_parser.add_argument('--unknown', nargs=2, required=False,
                                  help='Add a label (with the given name) for unknown words with random values, using a fixed seed for '
                                       'the given dimension.')

    arguments = arguments_parser.parse_args()
    process_arguments(arguments)


def process_arguments(arguments: Namespace) -> None:
    print("INFO: Processing arguments")

    input_folder = arguments.input
    output_folder = arguments.output
    join_files = arguments.combine
    split_train_file = arguments.split
    clean_embedding_file = arguments.clean
    unknown_values = arguments.unknown

    input_path = Path(BASE_PATH).joinpath(input_folder)
    if output_folder is not None:
        output_path = Path(BASE_PATH).joinpath(output_folder)

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
    elif unknown_values is not None:
        if filler.validate_parameters(unknown_values):
            filler.walk_directories(input_path, unknown_values)
        else:
            print("Error: Parameters not specified in the correct order or of the correct type")


if __name__ == "__main__":
    main()
