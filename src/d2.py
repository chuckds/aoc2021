#!/bin/env python3
"""
Advent Of Code 2021 Day 2
"""

import sys
import time


def p1p2(input_file: str) -> tuple[int, int]:
    horiz: int = 0
    depth: int = 0
    aim: int = 0

    with open(input_file) as f:
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

    print(f"{horiz=}, {depth=}, {aim=}")
    return (horiz * aim, horiz * depth)


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1p2(cli_args[0]))
    stop = time.perf_counter()
    print(f"Elapsed: {stop - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))