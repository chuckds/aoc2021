#!/bin/env python3
"""
Advent Of Code 2021 Day 6
"""

import sys
import time
import collections


def p1p2(input_file: str) -> tuple[int, int]:
    num_by_days_to_pop = collections.deque([0] * 9, maxlen=9)
    with open(input_file) as f:
        for days_to_pop_str in next(f).split(','):
            num_by_days_to_pop[int(days_to_pop_str)] += 1

    part1_res: int = 0
    for day_num in range(256):
        popping = num_by_days_to_pop.popleft()
        # Reset days-to-pop to 6 for those that just have popped
        num_by_days_to_pop[6] += popping
        # Add the new kids with days-to-pop of 8
        num_by_days_to_pop.append(popping)
        if day_num == 79:
            part1_res = sum(num_by_days_to_pop)

    return (part1_res, sum(num_by_days_to_pop))


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1p2(cli_args[0]))
    stop = time.perf_counter()
    print(f"Elapsed: {stop - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))