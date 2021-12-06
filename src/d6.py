#!/bin/env python3
"""
Advent Of Code 2021 Day 5
"""

from __future__ import annotations

import sys
import time
import collections


def count_fish(input_file: str, num_days: int) -> int:
    num_by_age: dict[int, int] = collections.defaultdict(int)
    with open(input_file) as f:
        for age_str in next(f).split(','):
            num_by_age[int(age_str)] += 1

    for day in range(num_days):
        popping = num_by_age.pop(0, 0)
        new_by_age: dict[int, int] = collections.defaultdict(int)
        for age, count in num_by_age.items():
            new_by_age[age - 1] = count

        new_by_age[6] += popping # Reset the timer on those popped
        new_by_age[8] += popping # Add the poppped 'children'
        num_by_age = new_by_age

    return sum(count for count in num_by_age.values())


def p2(input_file: str) -> int:
    return count_fish(input_file, 256)


def p1(input_file: str) -> int:
    return count_fish(input_file, 80)


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1(cli_args[0]))
    print(p2(cli_args[0]))
    stop = time.perf_counter()
    print(f"Elapsed: {stop - start}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))