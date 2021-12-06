#!/bin/env python3
"""
Advent Of Code 2021 Day 5
"""

import sys
import time
import collections


def count_fish(input_file: str, num_days: int) -> int:
    num_by_age = collections.deque([0] * 9, maxlen=9)
    with open(input_file) as f:
        for age_str in next(f).split(','):
            num_by_age[int(age_str)] += 1

    for _ in range(num_days):
        popping = num_by_age.popleft()
        num_by_age[6] += popping
        num_by_age.append(popping)

    return sum(num_by_age)


def p2(input_file: str) -> int:
    return count_fish(input_file, 256)


def p1(input_file: str) -> int:
    return count_fish(input_file, 80)


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1(cli_args[0]))
    print(p2(cli_args[0]))
    stop = time.perf_counter()
    print(f"Elapsed: {stop - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))