#!/bin/env python3
"""
Advent Of Code 2021 Day 9
"""

from __future__ import annotations

import sys
import math
import time

from typing import Iterator, Sequence


def adjacent_values(lines: Sequence[str], line_num: int, column: int) -> Iterator[tuple[str, int, int]]:
    for vert_delta, horiz_delta in ((-1, 0), (0, -1), (0, 1), (1, 0)):
        yield lines[line_num + vert_delta][column + horiz_delta], line_num + vert_delta, column + horiz_delta


def get_line_low_points(lines: Sequence[str], line_num: int, width: int) -> list[tuple[int, int, int]]:
    low_points = []
    for column in range(1, width + 1):
        value_being_checked = lines[line_num][column]
        if all(value_being_checked < adj_value for adj_value, _, _ in adjacent_values(lines, line_num, column)):
            low_points.append((int(value_being_checked), line_num, column))
    return low_points


def get_basin_size(lines: Sequence[str], start_line: int, start_column: int) -> int:
    # A list of points in this basin - starts with the low point
    basin_points = [(start_line, start_column)]
    # Have a set form so we can check if a point has already been 'visited'
    basin_point_set = set(basin_points)

    # Go through each point and check if there are adjacent points to add to the basin
    for line_num, column_num in basin_points:
        check_value = lines[line_num][column_num]
        for adj_value, adj_line_num, adj_column_num in adjacent_values(lines, line_num, column_num):
            if adj_value != '9' and check_value < adj_value and (adj_line_num, adj_column_num) not in basin_point_set:
                basin_points.append((adj_line_num, adj_column_num))
                basin_point_set.add((adj_line_num, adj_column_num))

    return len(basin_points)


def p1p2(input_file: str) -> tuple[int, int]:
    # Read all the lines but padd with 9's to make the boundaries easier
    lines = []
    with open(input_file) as f:
        first_line = next(f).strip()
        width = len(first_line)
        lines.append('9' * (width + 2))
        lines.append('9' + first_line + '9')
        lines.extend(['9' + line + '9' for line in f.read().splitlines()])
    lines.append('9' * (width + 2))

    # Now find the low points or centre of basins
    basins = []
    for line_num in range(1, len(lines) - 1):
        basins.extend(get_line_low_points(lines, line_num, width))
    
    # Get the sizes of each basin
    basin_sizes = []
    for basin_val, line_num, column_num in basins:
        basin_sizes.append(get_basin_size(lines, line_num, column_num))

    print(f"{basins=} {basin_sizes=}")
    return (sum(lp[0] for lp in basins) + len(basins),
            math.prod(sorted(basin_sizes, reverse=True)[:3]))


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1p2(cli_args[0]))
    stop = time.perf_counter()
    print(f"Elapsed: {stop - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))