#!/bin/env python3
"""
Advent Of Code 2021 Day 2
"""

import sys
import time
import argparse


def p2(args):
    horiz = 0
    depth = 0
    aim = 0
    with open(args.input) as f:
        for line in f:
            action, value = line.split()
            value = int(value)
            if action == 'forward':
                horiz += value
                depth += aim * value
            elif action == 'up':
                aim -= value
            elif action == 'down':
                aim += value

    print(f"Horizontal {horiz}, depth {depth}")
    return horiz * depth


def p1(args):
    horiz = 0
    depth = 0
    with open(args.input) as f:
        for line in f:
            action, value = line.split()
            value = int(value)
            if action == 'forward':
                horiz += value
            elif action == 'up':
                depth -= value
            elif action == 'down':
                depth += value

    print(f"Horizontal {horiz}, depth {depth}")
    return horiz * depth


def add_arguments(parser):
    parser.add_argument('-i', '--input', help="Input file")


def main(cli_args):
    parser = argparse.ArgumentParser()
    add_arguments(parser)
    args = parser.parse_args(cli_args)

    start = time.perf_counter()
    print(p1(args))
    print(p2(args))
    stop = time.perf_counter()
    print(f"Elapsed: {stop - start}s")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))