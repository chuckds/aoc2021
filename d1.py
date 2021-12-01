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
    with open(args.input) as f:
        f3depths = 0
        s3depths = 0
        t3depths = 0
        increasing = 0
        for i, depth in enumerate(f):
            m3 = i % 3
            depth = int(depth)
            if m3 == 0:
                s3depths += depth
                t3depths += depth
                if i > 2 and s3depths > f3depths:
                    increasing += 1
                f3depths = depth
            elif m3 == 1:
                t3depths += depth
                f3depths += depth
                if i > 3 and t3depths > s3depths:
                    increasing += 1
                s3depths = depth
            elif m3 == 2:
                f3depths += depth
                s3depths += depth
                if i > 4 and f3depths > t3depths:
                    increasing += 1
                t3depths = depth
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