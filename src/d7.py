#!/bin/env python3
"""
Advent Of Code 2021 Day 5
"""

import sys
import math
import time
import statistics
import collections


def calc_fuel_required(target_posn: int, horiz_positions: list[int], triangular_fuel: bool = False) -> int:
    if triangular_fuel:
        fuel_required = sum((abs(target_posn - horiz_position) * (abs(target_posn - horiz_position) + 1)) // 2
                            for horiz_position in horiz_positions)
    else:
        fuel_required = sum(abs(target_posn - horiz_position)
                            for horiz_position in horiz_positions)
    return fuel_required


def calc_fuel(input_file: str, triangular_fuel: bool = False) -> int:
    with open(input_file) as f:
        horiz_positions = [int(x_str) for x_str in next(f).split(',')]
    
    if triangular_fuel:
        mean = statistics.mean(horiz_positions)
        fuel_targets = [(calc_fuel_required(target, horiz_positions, triangular_fuel), target)
                        for target in range(math.floor(mean), math.ceil(mean) + 1)]
        fuel_required, best_position = min(fuel_targets, key=lambda x: x[0])
    else:
        best_position = int(statistics.median(horiz_positions))
        fuel_required = calc_fuel_required(best_position,
                                           horiz_positions, triangular_fuel)

    print(f"{fuel_required=} {best_position=}")
    return fuel_required


def p2(input_file: str) -> int:
    return calc_fuel(input_file, True)


def p1(input_file: str) -> int:
    return calc_fuel(input_file)


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1(cli_args[0]))
    print(p2(cli_args[0]))
    stop = time.perf_counter()
    print(f"Elapsed: {stop - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))