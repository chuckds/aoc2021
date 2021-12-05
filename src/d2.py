#!/bin/env python3
"""
Advent Of Code 2021 Day 2
"""

import sys
import time


def calc_params(filename: str) -> tuple[int, int, int]:
    horiz: int = 0
    depth: int = 0
    aim: int = 0
    with open(filename) as f:
        for line in f:
            action, value_str = line.split()
            value = int(value_str)
            if action == 'forward':
                horiz += value
                depth += aim * value
            elif action == 'up':
                aim -= value
            elif action == 'down':
                aim += value

    return horiz, depth, aim


def p2(input_file: str) -> int:
    horizontal, depth, aim = calc_params(input_file)
    print(f"{horizontal=}, {depth=}")
    return horizontal * depth


def p1(input_file: str) -> int:
    horizontal, _, depth = calc_params(input_file)
    print(f"{horizontal=}, {depth=}")
    return horizontal * depth


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1(cli_args[0]))
    print(p2(cli_args[0]))
    stop = time.perf_counter()
    print(f"Elapsed: {stop - start}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))