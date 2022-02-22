#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Any, List

from modules import column_inserter, columns_generator, column_remover, columns_swapper, empty_nodes, remove_pos, ud_enhancer
from modules import combiner, splitter, converter, cleaner, filler, embeddings_generator, calculate_ttest, extractor


def main() -> None:
    parser = ArgumentParser(description='Convert CoNLL-U files to CoNLL files')
    subparsers = parser.add_subparsers(title='Commands', dest='command')

    input_help = "Input file(s) folder"
    output_help = "Output file(s) folder"
    dimension_help = "Vector dimension size"

    # Convert
    subparser = subparsers.add_parser('convert', help='Convert from CoNLL-U format to CoNLL format.')
    subparser.add_argument('--input', type=str, required=True, help=input_help)
    subparser.add_argument('--output', type=str, required=True, help=output_help)
    # Combine
    subparser = subparsers.add_parser('combine', help='Combine multiple files from one phase (train, validation or test) into one file.')
    subparser.add_argument('--input', type=str, required=True, help=input_help)
    subparser.add_argument('--output', type=str, required=True, help=output_help)
    subparser.add_argument('--type', choices=['train', 'dev', 'test'], required=True, help='The type of files to combine')
    # Split
    subparser = subparsers.add_parser('split', help='In case there is no validation file (dev), the training file (train) is split in '
                                                    'two with a random 80-20 ratio.')
    subparser.add_argument('--input', type=str, required=True, help=input_help)
    subparser.add_argument('--output', type=str, required=True, help=output_help)
    # Clean
    subparser = subparsers.add_parser('clean', help='Cleans up an embedding file by removing the first line with the number of words and '
                                                    'the vector size.')
    subparser.add_argument('--input', type=str, required=True, help=input_help)
    subparser.add_argument('--output', type=str, required=True, help=output_help)
    # Fill in
    subparser = subparsers.add_parser('fill', help='Add a label (with the given name) for unknown words with random values, using a '
                                                   'fixed seed for the given dimension.')
    subparser.add_argument('--input', type=str, required=True, help=input_help)
    subparser.add_argument('--label', type=str, required=True, help='Name of the label to be inserted')
    subparser.add_argument('--dimension', type=int, required=True, help=dimension_help)
    subparser.add_argument('--position', type=int, help='Indicates the position in which to insert the label')
    # Generate
    subparser = subparsers.add_parser('generate', help='Generates a random embeddings file with the specified dimension from the '
                                                       'training and validation file.')
    subparser.add_argument('--input', type=str, required=True, help=input_help)
    subparser.add_argument('--output', type=str, required=True, help=output_help)
    subparser.add_argument('--dimension', type=int, required=True, help=dimension_help)
    # Add columns
    subparser = subparsers.add_parser('columns', help='Adds the required number of columns to the end of each line of a CoNLL file to '
                                                      'match the CoNLL-U format of 10 tab-separated columns.')
    subparser.add_argument('--input', type=str, required=True, help=input_help)
    subparser.add_argument('--output', type=str, required=True, help=output_help)
    # Remove POS
    subparser = subparsers.add_parser('remove-pos', help='Removes POS information on every line of a sentence. The content is replaced by '
                                                         'a _.')
    subparser.add_argument('--input', type=str, required=True, help=input_help)
    subparser.add_argument('--output', type=str, required=True, help=output_help)
    # T-Test
    subparser = subparsers.add_parser('ttest', help='Calculate the T-test for the means of two independent samples of scores.')
    subparser.add_argument('--gold_a', type=str, required=True, help="Folder with the original CoNLL test files for the parser A")
    subparser.add_argument('--predicted_a', type=str, required=True, help="Folder with CoNLL test files predicted by a model of parser A")
    subparser.add_argument('--gold_b', type=str, required=True, help="Folder with the original CoNLL test files for the parser B")
    subparser.add_argument('--predicted_b', type=str, required=True, help="Folder with CoNLL test files predicted by a model of parser B")
    # Swap
    subparser = subparsers.add_parser('swap', help='Swaps the position of two given columns.')
    subparser.add_argument('--input', type=str, required=True, help=input_help)
    subparser.add_argument('--output', type=str, required=True, help=output_help)
    subparser.add_argument('--from_position', type=int, required=True, help='Column to be swapped, starting from number zero.')
    subparser.add_argument('--to_position', type=int, required=True, help='Column to swap with, starting from number zero.')
    # Remove column
    subparser = subparsers.add_parser('remove-column', help='Deletes the column at the given position, starting from number zero.')
    subparser.add_argument('--input', type=str, required=True, help=input_help)
    subparser.add_argument('--output', type=str, required=True, help=output_help)
    subparser.add_argument('--position', type=int, required=True, help='Column to be removed, starting from number zero.')
    # Add column
    subparser = subparsers.add_parser('add-column', help='Adds the column at the given position, starting from number zero, with the '
                                                         'specified content.')
    subparser.add_argument('--input', type=str, required=True, help=input_help)
    subparser.add_argument('--output', type=str, required=True, help=output_help)
    subparser.add_argument('--position', type=int, required=True, help='Column to be added, starting from number zero.')
    subparser.add_argument('--content', type=str, required=True, help='Content of the column to be added.')
    # Remove empty nodes
    subparser = subparsers.add_parser('empty-nodes', help='Remove sentences containing empty nodes in XX.1 format which can cause '
                                                          'problems with some parsers.')
    subparser.add_argument('--input', type=str, required=True, help=input_help)
    subparser.add_argument('--output', type=str, required=True, help=output_help)
    # Enhanced Universal Dependencies
    subparser = subparsers.add_parser('enhanced-ud', help='Converts a file without EUD annotation to a file with EUD annotation. This is '
                                                          'done by filling column 8 with the contents of column 6 and 7 separated by a '
                                                          'colon.')
    subparser.add_argument('--keep', action='store_true', help='If the column already contains a value, keep it.')
    subparser.add_argument('--input', type=str, required=True, help=input_help)
    subparser.add_argument('--output', type=str, required=True, help=output_help)
    # Extract
    subparser = subparsers.add_parser('extract', help='Extracts the indicated percentage of phrases into a new file.')
    subparser.add_argument('--input', type=str, required=True, help=input_help)
    subparser.add_argument('--output', type=str, required=True, help=output_help)
    subparser.add_argument('--percentages', type=int, nargs='+', required=True, help="Percentage of sentences to be extracted")

    arguments = parser.parse_args()
    if arguments.command:
        process_arguments(arguments)
    else:
        parser.print_help()


def process_arguments(arguments: Namespace) -> None:
    print("INFO: Processing arguments")

    base_path = "output"

    command = arguments.command
    if command == "convert":
        input_folder = arguments.input
        output_folder = arguments.output
        converter_handler(base_path, input_folder, output_folder)
    elif command == "combine":
        input_folder = arguments.input
        output_folder = arguments.output
        file_type = arguments.type
        combiner_handler(base_path, input_folder, output_folder, file_type)
    elif command == "split":
        input_folder = arguments.input
        output_folder = arguments.output
        splitter_handler(base_path, input_folder, output_folder)
    elif command == "clean":
        input_folder = arguments.input
        output_folder = arguments.output
        cleaner_handler(base_path, input_folder, output_folder)
    elif command == "fill":
        input_folder = arguments.input
        label = arguments.label
        dimension = arguments.dimension
        position = arguments.position
        filler_handler(base_path, input_folder, label, dimension, position)
    elif command == "generate":
        input_folder = arguments.input
        output_folder = arguments.output
        dimension = arguments.dimension
        embeddings_generator_handler(base_path, input_folder, output_folder, dimension)
    elif command == "columns":
        input_folder = arguments.input
        output_folder = arguments.output
        columns_generator_handler(base_path, input_folder, output_folder)
    elif command == "remove-pos":
        input_folder = arguments.input
        output_folder = arguments.output
        remove_pos_handler(base_path, input_folder, output_folder)
    elif command == "ttest":
        gold_a_folder = arguments.gold_a
        predicted_a_folder = arguments.predicted_a
        gold_b_folder = arguments.gold_b
        predicted_b_folder = arguments.predicted_b
        ttest_handler(gold_a_folder, predicted_a_folder, gold_b_folder, predicted_b_folder)
    elif command == "swap":
        input_folder = arguments.input
        output_folder = arguments.output
        column_from = arguments.from_position
        column_to = arguments.to_position
        swap_handler(base_path, input_folder, output_folder, column_from, column_to)
    elif command == "remove-column":
        input_folder = arguments.input
        output_folder = arguments.output
        position = arguments.position
        remove_column_handler(base_path, input_folder, output_folder, position)
    elif command == "add-column":
        input_folder = arguments.input
        output_folder = arguments.output
        position = arguments.position
        content = arguments.content
        add_column_handler(base_path, input_folder, output_folder, position, content)
    elif command == "empty-nodes":
        input_folder = arguments.input
        output_folder = arguments.output
        empty_nodes_handler(base_path, input_folder, output_folder)
    elif command == "enhanced-ud":
        keep_content = arguments.keep
        input_folder = arguments.input
        output_folder = arguments.output
        enhanced_ud_handler(base_path, keep_content, input_folder, output_folder)
    elif command == "extract":
        input_folder = arguments.input
        output_folder = arguments.output
        percentages = arguments.percentages
        extract_handler(base_path, input_folder, output_folder, percentages)
    else:
        print(f"Error: Command {command} is not recognised")


FOLDERS_ERROR_MESSAGE = "Error: Check that the arguments are folders and not files, and that the folders exist"
FOLDER_ERROR_MESSAGE = "Error: Check that the argument is a folder and not a file, and that the folder exists"


def converter_handler(base_path: str, input_folder: str, output_folder: str) -> None:
    input_path = Path(base_path).joinpath(input_folder)
    output_path = Path(base_path).joinpath(output_folder)

    if input_path.is_dir() and output_path.is_dir():
        converter.walk_directories(input_path, output_path)
    else:
        print(FOLDERS_ERROR_MESSAGE)


def combiner_handler(base_path: str, input_folder: str, output_folder: str, file_type: str) -> None:
    input_path = Path(base_path).joinpath(input_folder)
    output_path = Path(base_path).joinpath(output_folder)

    if input_path.is_dir() and output_path.is_dir():
        combiner.walk_directories(input_path, output_path, file_type)
    else:
        print(FOLDERS_ERROR_MESSAGE)


def splitter_handler(base_path: str, input_folder: str, output_folder: str) -> None:
    input_path = Path(base_path).joinpath(input_folder)
    output_path = Path(base_path).joinpath(output_folder)

    if input_path.is_dir() and output_path.is_dir():
        splitter.walk_directories(input_path, output_path)
    else:
        print(FOLDERS_ERROR_MESSAGE)


def cleaner_handler(base_path: str, input_folder: str, output_folder: str) -> None:
    input_path = Path(base_path).joinpath(input_folder)
    output_path = Path(base_path).joinpath(output_folder)

    if input_path.is_dir() and output_path.is_dir():
        cleaner.walk_directories(input_path, output_path)
    else:
        print(FOLDERS_ERROR_MESSAGE)


def filler_handler(base_path: str, input_folder: str, label: str, dimension: int, position: Any) -> None:
    input_path = Path(base_path).joinpath(input_folder)

    if input_path.is_dir():
        if filler.validate_parameters(label):
            filler.walk_directories(input_path, label, dimension, position)
        else:
            print("Error: The label may only contain letters")
    else:
        print(FOLDER_ERROR_MESSAGE)


def embeddings_generator_handler(base_path: str, input_folder: str, output_folder: str, dimension: int) -> None:
    input_path = Path(base_path).joinpath(input_folder)
    output_path = Path(base_path).joinpath(output_folder)

    if input_path.is_dir() and output_path.is_dir():
        embeddings_generator.walk_directories(input_path, output_path, dimension)
    else:
        print(FOLDERS_ERROR_MESSAGE)


def columns_generator_handler(base_path: str, input_folder: str, output_folder: str) -> None:
    input_path = Path(base_path).joinpath(input_folder)
    output_path = Path(base_path).joinpath(output_folder)

    if input_path.is_dir() and output_path.is_dir():
        columns_generator.walk_directories(input_path, output_path)
    else:
        print(FOLDERS_ERROR_MESSAGE)


def remove_pos_handler(base_path: str, input_folder: str, output_folder: str) -> None:
    input_path = Path(base_path).joinpath(input_folder)
    output_path = Path(base_path).joinpath(output_folder)

    if input_path.is_dir() and output_path.is_dir():
        remove_pos.walk_directories(input_path, output_path)
    else:
        print(FOLDERS_ERROR_MESSAGE)


def ttest_handler(gold_a_folder: str, predicted_a_folder: str, gold_b_folder: str, predicted_b_folder: str) -> None:
    gold_a_path = Path.home().joinpath(gold_a_folder)
    predicted_a_path = Path.home().joinpath(predicted_a_folder)
    gold_b_path = Path.home().joinpath(gold_b_folder)
    predicted_b_path = Path.home().joinpath(predicted_b_folder)

    if gold_a_path.is_dir() and predicted_a_path.is_dir() and gold_b_path.is_dir() and predicted_b_path.is_dir():
        calculate_ttest.walk_directories(gold_a_path, predicted_a_path, gold_b_path, predicted_b_path)
    else:
        print(FOLDERS_ERROR_MESSAGE)


def swap_handler(base_path: str, input_folder: str, output_folder: str, column_from: int, column_to: int) -> None:
    input_path = Path(base_path).joinpath(input_folder)
    output_path = Path(base_path).joinpath(output_folder)

    if input_path.is_dir() and output_path.is_dir():
        columns_swapper.walk_directories(input_path, output_path, column_from, column_to)
    else:
        print(FOLDERS_ERROR_MESSAGE)


def remove_column_handler(base_path: str, input_folder: str, output_folder: str, position: int) -> None:
    input_path = Path(base_path).joinpath(input_folder)
    output_path = Path(base_path).joinpath(output_folder)

    if input_path.is_dir() and output_path.is_dir():
        column_remover.walk_directories(input_path, output_path, position)
    else:
        print(FOLDERS_ERROR_MESSAGE)


def add_column_handler(base_path: str, input_folder: str, output_folder: str, position: int, content: str) -> None:
    input_path = Path(base_path).joinpath(input_folder)
    output_path = Path(base_path).joinpath(output_folder)

    if input_path.is_dir() and output_path.is_dir():
        column_inserter.walk_directories(input_path, output_path, position, content)
    else:
        print(FOLDERS_ERROR_MESSAGE)


def empty_nodes_handler(base_path: str, input_folder: str, output_folder: str) -> None:
    input_path = Path(base_path).joinpath(input_folder)
    output_path = Path(base_path).joinpath(output_folder)

    if input_path.is_dir() and output_path.is_dir():
        empty_nodes.walk_directories(input_path, output_path)
    else:
        print(FOLDERS_ERROR_MESSAGE)


def enhanced_ud_handler(base_path: str, keep_content: bool, input_folder: str, output_folder: str) -> None:
    input_path = Path(base_path).joinpath(input_folder)
    output_path = Path(base_path).joinpath(output_folder)

    if input_path.is_dir() and output_path.is_dir():
        ud_enhancer.walk_directories(input_path, output_path, keep_content)
    else:
        print(FOLDERS_ERROR_MESSAGE)


def extract_handler(base_path: str, input_folder: str, output_folder: str, percentages: List[int]) -> None:
    input_path = Path(base_path).joinpath(input_folder)
    output_path = Path(base_path).joinpath(output_folder)

    if input_path.is_dir() and output_path.is_dir():
        extractor.walk_directories(input_path, output_path, percentages)
    else:
        print(FOLDERS_ERROR_MESSAGE)


if __name__ == "__main__":
    main()
