#!/bin/env python3
"""
Advent Of Code 2021 Day 23
"""

import sys
import time


def p1p2(input_file: str) -> tuple[int, int]:
    with open(input_file):
        pass
    return (0, 0)


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1p2(cli_args[0]))
    print(f"Elapsed: {time.perf_counter() - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
