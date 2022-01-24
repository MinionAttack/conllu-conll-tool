# -*- coding: utf-8 -*-

from pathlib import Path
from typing import List

from .utils import search_files


def walk_directories(input_path: Path, output_path: Path) -> None:
    print("INFO: Browsing through directories to remove POS")

    files = search_files(input_path)
    remove_pos_column(files, output_path)


def remove_pos_column(files: List[Path], output_path: Path) -> None:
    print("INFO: Removing POS information")

    for file in files:
        filename = file.name
        output_file = Path(output_path).joinpath(filename)
        with open(file, 'rt', encoding='UTF-8') as pos_file, open(output_file, 'wt', encoding='UTF-8') as no_pos_file:
            for line in pos_file:
                if not line.startswith("#"):
                    if line != "\n":
                        tuples = line.split("\t")
                        if len(tuples) == 10 and tuples[0] != '#' and '.' not in tuples[0] and '-' not in tuples[0]:
                            tuples[3] = '_'
                            no_pos_file.write('\t'.join(tuples))
                        else:
                            no_pos_file.write(line)
                    else:
                        no_pos_file.write("\n")
                else:
                    no_pos_file.write(line)
