#!/bin/env python3
"""
Advent Of Code 2021 Day 1
"""

import sys
import argparse
import collections


def count_increasing_sliding_windows(filename, window_size):
    increasing = 0

    with open(filename) as f:
        depths = collections.deque(int(next(f))
                                   for _ in range(window_size))
        for line in f:
            depth = int(line)
            # The only elements two consecutive sliding windows differ by is
            # the first and last, so only these need to be compared to see
            # which window is bigger
            if depth > depths.popleft():
                increasing += 1
            depths.append(depth)

    return increasing


def d1p1(args):
    return count_increasing_sliding_windows(args.input, 1)


def d1p2(args):
    return count_increasing_sliding_windows(args.input, 3)


def add_arguments(parser):
    parser.add_argument('-i', '--input', help="Input file")


def main(cli_args):
    parser = argparse.ArgumentParser()
    add_arguments(parser)
    args = parser.parse_args(cli_args)

    print(d1p1(args))
    print(d1p2(args))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))