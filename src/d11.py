#!/bin/env python3
"""
Advent Of Code 2021 Day 11
"""

import sys
import time

from typing import Iterator


def adjacent_values(row: int, col: int,
                    grid_size: int) -> Iterator[tuple[int, int]]:
    for vert_delta in (-1, 0, 1):
        for horiz_delta in (-1, 0, 1):
            if vert_delta or horiz_delta:
                new_row = row + vert_delta
                new_col = col + horiz_delta
                if (new_row >= 0 and new_col >= 0 and
                    new_row < grid_size and new_col < grid_size):
                    yield new_row, new_col


def count_flashes(grid: list[list[int]],
                  grid_size: int) -> set[tuple[int, int]]:
    flashed_coords: set[tuple[int, int]] = set()
    last_set_size = -1
    while last_set_size != len(flashed_coords):
        last_set_size = len(flashed_coords)
        for row_num, row in enumerate(grid):
            for col_num in range(grid_size):
                if row[col_num] > 9:
                    flashed_coords.add((row_num, col_num))
                    row[col_num] = -10000
                    for adj_row, adj_col in adjacent_values(row_num, col_num,
                                                            grid_size):
                        grid[adj_row][adj_col] += 1
    return flashed_coords


def p1p2(input_file: str) -> tuple[int, int]:
    grid_size = 10
    num_part_1_steps = 100
    part1_num_flashes = 0
    step_num_all_flash = 0
    total_flashes = 0

    with open(input_file) as f:
        grid = [[int(char) for char in line] for line in f.read().splitlines()]

    step_num = 0
    while not step_num_all_flash:
        step_num += 1
        for row in grid:
            for col_num in range(grid_size):
                row[col_num] += 1

        flashed_coords = count_flashes(grid, grid_size)
        total_flashes += len(flashed_coords)
        if step_num == num_part_1_steps:
            part1_num_flashes = total_flashes
        if len(flashed_coords) == grid_size ** 2:
            # Everyone flashed
            step_num_all_flash = step_num
        for row_num, col_num in flashed_coords:
            grid[row_num][col_num] = 0

    return (part1_num_flashes, step_num_all_flash)


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1p2(cli_args[0]))
    stop = time.perf_counter()
    print(f"Elapsed: {stop - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))