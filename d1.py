#!/bin/env python3
"""
Advent Of Code 2021 Day 1
"""

import sys
import argparse
import fileinput


def d1p1(args):
    with open(args.input) as f:
        last_depth = int(next(f))
        increasing = 0
        for depth in f:
            if int(depth) > last_depth:
                increasing += 1
            last_depth = int(depth)
    print(increasing)


def d1p2(args):
    WIN_SIZE = 3
    increasing = 0

    with open(args.input) as f:
        # Create a list to store the sums for each concurrent 'window'
        depths = [0] * WIN_SIZE
        for line_index, line in enumerate(f):
            depth = int(line)
            # This line marks the start of a fresh depth[window_i] sum
            # and the last value for depths[(window_i + 1) % WIN_SIZE] sum
            window_i = line_index % WIN_SIZE

            # For every window sum other than the one we completed on the last line
            # add depth
            for i in range(WIN_SIZE - 1):
                depths[(window_i + 1 + i) % WIN_SIZE] += depth

            # If enough lines have been read for the window sums to be complete
            # check if the sums are increasing
            if (line_index >= (WIN_SIZE + window_i) and
                depths[(window_i + 1) % WIN_SIZE] > depths[window_i]):
                increasing += 1
            depths[window_i] = depth

    print(increasing)


puzzles = {
    'd1p1' : d1p1,
    'd1p2' : d1p2,
}

def add_arguments(parser):
    parser.add_argument('-p', '--puzzle', help="Which puzzle to run", choices=puzzles.keys(), required=True)
    parser.add_argument('-i', '--input', help="Input file")


def main(cli_args):
    parser = argparse.ArgumentParser()
    add_arguments(parser)
    args = parser.parse_args(cli_args)

    puzzles[args.puzzle](args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))