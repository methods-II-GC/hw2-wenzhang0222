#!/usr/bin/env python
"""a Python command-line tool that reads in tagging data and randomly splits it into training, development and test
data """


import argparse
from typing import Iterator, List
from random import shuffle, seed


def read_tags(path: str) -> Iterator[List[List[str]]]:
    with open(path, "r") as source:
        lines = []
        for line in source:
            line = line.rstrip()
            if line:  # Line is contentful.
                lines.append(line.split())
            else:  # Line is blank.
                yield lines.copy()
                lines.clear()
    # Just in case someone forgets to put a blank line at the end...
    if lines:
        yield lines

def write_tags(path: str, data: List[List[List[str]]]) -> None:
    with open(path, "w") as source:
        for sentence in data:
            for row in sentence:
                for element in row:
                    source.write(element)
                    source.write(" ")
                source.write("\n")
    source.close()
            
        

def main(args: argparse.Namespace) -> None:
    # Set random seed
    seed(args.seed)
    # Read tagging data
    corpus = list(read_tags(args.input))
    # Randomization
    shuffle(corpus)
    # Splitting
    length = len(corpus)
    training_data = corpus[:int(0.8*length)]#the last element is not included when splitting list
    development_data = corpus[int(0.8*length):int(0.9*length)]
    testing_data = corpus[int(0.9*length):]
    # Write data to the path
    write_tags(args.train, training_data)
    write_tags(args.dev, development_data)
    write_tags(args.test, testing_data)
    
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split tagging data into train, development, test data")
    parser.add_argument("input", help="input data", type=str)
    parser.add_argument("train", help="train path that train dataset will be put", type=str)
    parser.add_argument("dev", help="dev path that development dataset will be put", type=str)
    parser.add_argument("test", help="test path that test dataset will be put", type=str)
    parser.add_argument("--seed", help="Random seed", type=int, required=True)
    main(parser.parse_args())
