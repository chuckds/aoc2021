#!/bin/env python3
"""
Advent Of Code 2021 Day 7
"""

import sys
import math
import time
import statistics


def calc_triangular_fuel(target_posn: int, horiz_posns: list[int]) -> int:
    return sum((abs(target_posn - horiz_posn) * (abs(target_posn - horiz_posn) + 1)) // 2
               for horiz_posn in horiz_posns)


def p1p2(input_file: str) -> tuple[int, int]:
    with open(input_file) as f:
        horiz_positions = [int(x_str) for x_str in next(f).split(',')]
    
    best_position = int(statistics.median(horiz_positions))
    p1_fuel_required = sum(abs(best_position - horiz_position)
                           for horiz_position in horiz_positions)
    print(f"p1 {p1_fuel_required=} {best_position=}")

    # Best position is either mean rounded up or down, try both pick best
    mean = statistics.mean(horiz_positions)
    fuel_targets = [(calc_triangular_fuel(target, horiz_positions), target)
                    for target in range(math.floor(mean), math.ceil(mean) + 1)]
    fuel_required, best_position = min(fuel_targets, key=lambda x: x[0])
    print(f"p2 {fuel_required=} {best_position=}")

    return (p1_fuel_required, fuel_required)


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1p2(cli_args[0]))
    stop = time.perf_counter()
    print(f"Elapsed: {stop - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))