# conllu-conll-tool

![build](https://img.shields.io/badge/build-passing-success) ![build](https://img.shields.io/badge/license-MIT-success) ![build](https://img.shields.io/badge/python-3.6%2B-blue) ![build](https://img.shields.io/badge/platform-linux--64-lightgrey) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=MinionAttack_conllu-conll-tool&metric=alert_status)](https://sonarcloud.io/dashboard?id=MinionAttack_conllu-conll-tool)

Table of contents.

1. [Summary](#summary)
2. [How to use](#how-to-use)
3. [Examples](#examples)
4. [Licensing agreement](#licensing-agreement)

## Summary

This is a tool to convert *CoNLL-U* format files to *CoNLL* format files and manipulate training, validation and test sets.

This script has nine features:

1. Convert files in *CoNLL-U* format to *CoNLL* format.
2. Combine several files of a given training phase into one file.
3. Split a training phase file into two files, one file for the training phase and one file for the validation phase.
4. Clean up an embeddings file to remove the first line containing the number of words and the size of the vector.
5. Add a tag with random values for a specific dimension for unknown words in the embedding file. A fixed seed is used to be able to
   reproduce the experiments.
6. Generate an embedding file with the words from the training file and the validation file with random values for a specific dimension. A
   fixed seed is used to be able to reproduce the experiments.
7. Adds the required number of columns to the end of each line of a *CoNLL* file to match the *CoNLL-U* format of 10 tab-separated columns.
8. Removes POS information on every line of a sentence. The content is replaced by a _.
9. Calculate the *T-test* for the means of two independent samples of scores.

**It is important to note that the script uses the _output_ folder as the base directory for both input and output files in some features.**

## How to use

Install the necessary dependencies listed in the `requirements.txt` file.

`$ pip3 install -r requirements.txt`

To run the script, from a terminal in the root directory, type:

`$ ./conllu-conll-tool.py`

This will show the usage:

```
usage: conllu-conll-tool.py [-h]
                            {convert,combine,split,clean,fill,generate,columns,remove,ttest}
                            ...

Convert CoNLL-U files to CoNLL files

optional arguments:
  -h, --help            show this help message and exit

Commands:
  {convert,combine,split,clean,fill,generate,columns,remove,ttest}
    convert             Convert from CoNLL-U format to CoNLL format.
    combine             Combine multiple files from one phase (train,
                        validation or test) into one file.
    split               In case there is no validation file (dev), the
                        training file (train) is split in two with a random
                        80-20 ratio.
    clean               Cleans up an embedding file by removing the first line
                        with the number of words and the vector size.
    fill                Add a label (with the given name) for unknown words
                        with random values, using a fixed seed for the given
                        dimension.
    generate            Generates a random embeddings file with the specified
                        dimension from the training and validation file.
    columns             Adds the required number of columns to the end of each
                        line of a CoNLL file to match the CoNLL-U format of 10
                        tab-separated columns.
    remove              Removes POS information on every line of a sentence.
                        The content is replaced by a _.
    ttest               Calculate the T-test for the means of two independent
                        samples of scores.
```

If you want to know how to use a specific command, for example the *clean* command, type:

`$ ./conllu-conll-tool.py clean --help`

And it will show the help:

```
usage: conllu-conll-tool.py clean [-h] --input INPUT --output OUTPUT

optional arguments:
  -h, --help       show this help message and exit
  --input INPUT    Input files folder
  --output OUTPUT  Output files folder
```

### Note

If you get an error that you do not have permissions to run the script, type:

`$ chmod u+x conllu-conll-tool.py`

Run the script again.

## Examples

### 1. Convert files

`$ ./conllu-conll-tool.py convert --input conllu --output conll`

- **input**: Directory (must have been created) inside the *output* folder where the *CoNLL-U* files to be converted are located.
    - You can put the files directly or if you want to convert several languages you can put the files in different folders (one for each  
      language), but be aware that the script does not process more than one level of subdirectories.
- **output**: Directory (must have been created) inside the *output* folder where the converted *CoNLL* files shall be created.

### 2. Combine files

`$ ./conllu-conll-tool.py combine --input conllu --output combined --type train`

- **input**: Directory (must have been created) inside the *output* folder where the *CoNLL-U* files to be combined are located.
    - You can put the files directly or if you want to combine several languages you can put the files in different folders (one for each  
      language), but be aware that the script does not process more than one level of subdirectories.
- **output**: Directory (must have been created) inside the *output* folder where the combined *CoNLL-U* files shall be created.
- **type**: The type of files to combine. This can be one of the following values: `train`, `dev` or `test`.

### 3. Split files

`$ ./conllu-conll-tool.py split --input conllu --output splitted`

- **input**: Directory (must have been created) inside the *output* folder where the *CoNLL-U* files to be splitted are located.
    - You can put the files directly or if you want to split several languages you can put the files in different folders (one for each  
      language), but be aware that the script does not process more than one level of subdirectories.
    - Unless the code is modified, the split is **80% for the training phase** and **20% for the validation phase**.
- **output**: Directory (must have been created) inside the *output* folder where the splitted (*train* and *dev*) *CoNLL-U* files shall  
  be created.

### 4. Clean up files

`$ ./conllu-conll-tool.py clean --input embeddings --output cleaned`

- **input**: Directory (must have been created) inside the *output* folder where the embedding files to be cleaned are located.
    - You can put the files directly or if you want to clean several languages you can put the files in different folders (one for each  
      language), but be aware that the script does not process more than one level of subdirectories.
- **output**: Directory (must have been created) inside the *output* folder where the cleaned embedding files shall be created.

### 5. Fill in files

`$ ./conllu-conll-tool.py fill --input embeddings --label unk --dimension 100`

- **input**: Directory (must have been created) inside the *output* folder where the embedding files to be filled in are located.
    - You can put the files directly or if you want to fill in several languages you can put the files in different folders (one for each  
      language), but be aware that the script does not process more than one level of subdirectories.
- **label**: Name of the tag to attach to the embeddings file.
- **dimension**: The vector dimensions for the tag.

### 6. Generate files

`$ ./conllu-conll-tool.py generate --input no_embeddings --output generated --dimension 100`

- **input**: Directory (must have been created) inside the *output* folder where the *CoNLL-U* files (*train* and *dev*) from which  
  the embeddings file will be generated are located.
    - You can put the files directly or if you want to generate several languages you can put the files in different folders (one for each  
      language), but be aware that the script does not process more than one level of subdirectories.
- **output**: Directory (must have been created) inside the *output* folder where the generated embeddings file shall be created.
- **dimension**: The vector dimensions for the tags.

### 7. Add columns

`$ ./conllu-conll-tool.py columns --input conll_columns --output conllu_columns`

- **input**: Directory (must have been created) inside the *output* folder where the *CoNLL* files are located.
    - You can put the files directly or if you want to add columns to several languages you can put the files in different folders (one for
      each language), but be aware that the script does not process more than one level of subdirectories.
- **output**: Directory (must have been created) within the output folder where the *CoNLL* files will be created with the *CoNLL-U*
  column format.

### 8. Remove POS

`$ ./conllu-conll-tool.py remove --input with_pos --output without_pos`

- **input**: Directory (must have been created) inside the *output* folder where the *CoNLL* files with the POS information are located.
    - You can put the files directly or if you want to add columns to several languages you can put the files in different folders (one for
      each language), but be aware that the script does not process more than one level of subdirectories.
- **output**: Directory (must have been created) within the output folder where the *CoNLL* files without the POS information will be
  created.

### 9. Calculate T-Test

`$ ./conllu-conll-tool.py ttest --gold_a parser_a/gold --predicted_a parser_a/predicted --gold_b parser_b/gold --predicted_b parser_b/predicted`

- **gold_a**: Directory where the *GOLD* (*TEST*) files of parser A are located.
    - You can put the files directly or if you want to analyse several languages you can put the files in different folders (one for each
      language), but be aware that the script does not process more than one level of subdirectories.
- **predicted_a**: Directory where the *PREDICTED* (*TEST*) files of parser A are located.
    - You can put the files directly or if you want to analyse several languages you can put the files in different folders (one for each
      language), but be aware that the script does not process more than one level of subdirectories.
- **gold_b**: Directory where the *GOLD* (*TEST*) files of parser B are located.
    - You can put the files directly or if you want to analyse several languages you can put the files in different folders (one for each
      language), but be aware that the script does not process more than one level of subdirectories.
- **predicted_b**: Directory where the *PREDICTED* (*TEST*) files of parser B are located.
    - You can put the files directly or if you want to analyse several languages you can put the files in different folders (one for each
      language), but be aware that the script does not process more than one level of subdirectories.

### Note

1. The *gold_x* directory and the *predicted_x* directory must have the same number of languages in order to perform the calculations.
2. The *predicted_x* directory and the *predicted_y* directory must have the same number of languages and in each language the same number
   of predicted files in order to perform the calculations.

## Licensing agreement

MIT License

Copyright (c) 2021 Iago Alonso Alonso

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "  
Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish,  
distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to
the  
following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF  
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR
ANY  
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE  
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
