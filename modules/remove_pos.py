# -*- coding: utf-8 -*-

from pathlib import Path
from typing import List


def walk_directories(input_path: Path, output_path: Path) -> None:
    print("INFO: Browsing through directories to remove POS")

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

    remove_pos_column(files, output_path)


def remove_pos_column(files: List[Path], output_path: Path) -> None:
    print("INFO: Removing POS information")

    for file in files:
        filename = file.name
        output_file = Path(output_path).joinpath(filename)
        with open(file, 'rt', encoding='UTF-8') as pos_file, open(output_file, 'wt', encoding='UTF-8') as no_pos_file:
            for line in pos_file:
                if line != "\n":
                    tuples = line.split("\t")
                    if len(tuples) == 10 and tuples[0] != '#' and '.' not in tuples[0] and '-' not in tuples[0]:
                        tuples[3] = '_'
                        no_pos_file.write('\t'.join(tuples))
                    else:
                        no_pos_file.write(line)
                else:
                    no_pos_file.write("\n")
