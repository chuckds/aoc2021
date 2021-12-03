#!/bin/env python3
"""
Advent Of Code 2021 Day 2
"""

import sys
import time


def calc_params(filename):
    horiz = 0
    depth = 0
    aim = 0
    with open(filename) as f:
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

    return horiz, depth, aim


def p2(input_file):
    horizontal, depth, aim = calc_params(input_file)
    print(f"{horizontal=}, {depth=}")
    return horizontal * depth


def p1(input_file):
    horizontal, _, depth = calc_params(input_file)
    print(f"{horizontal=}, {depth=}")
    return horizontal * depth


def main(cli_args):
    start = time.perf_counter()
    print(p1(cli_args[0]))
    print(p2(cli_args[0]))
    stop = time.perf_counter()
    print(f"Elapsed: {stop - start}s")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))