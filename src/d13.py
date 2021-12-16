#!/bin/env python3
"""
Advent Of Code 2021 Day 13
"""

from __future__ import annotations

import sys
import time
import collections

FoldType = tuple[str, int]


class Grid:
    def __init__(self) -> None:
        self.size = [0, 0]
        self.rows: dict[int, set[int]] = collections.defaultdict(set)
        self.cols: dict[int, set[int]] = collections.defaultdict(set)

    def add_dot(self, x: int, y: int) -> None:
        self.rows[y].add(x)
        self.cols[x].add(y)
        self.size = [max(self.size[0], x + 1), max(self.size[1], y + 1)]

    def fold(self, dimension: str, val: int) -> None:
        is_fold_up = dimension == 'y'
        if is_fold_up:
            size_index = 1
            merging, update = self.rows, self.cols
        else:
            size_index = 0
            merging, update = self.cols, self.rows

        for fold_line, into_line in zip(range(val + 1, self.size[size_index]),
                                        range(val - 1, -1, -1)):
            for new_dot in merging[fold_line] - merging[into_line]:
                merging[into_line].add(new_dot)
                update[new_dot].add(into_line)
        self.size[size_index] = val

    def num_dots(self) -> int:
        num_dots = 0
        for row_y, row in self.rows.items():
            if row_y < self.size[1]:
                num_dots += sum(1 for d in row if d < self.size[0])
        return num_dots

    def __str__(self) -> str:
        lines = [''.join(['#' if x in self.rows.get(y, set()) else '.'
                          for x in range(0, self.size[0])])
                 for y in range(0, self.size[1])]
        return "\n".join(lines)


def parse_input(input_file: str) -> tuple[Grid, list[FoldType]]:
    folds = []
    grid = Grid()
    with open(input_file) as f:
        for line in f:
            line = line.strip()
            if line:
                x, y = line.split(',')
                grid.add_dot(int(x), int(y))
            else:
                # Blank line separates the dot section from the fold section
                break
        for line in f:
            _, _, fold_line = line.strip().split(' ')
            dimension, value = fold_line.split('=')
            folds.append((dimension, int(value)))
    return (grid, folds)


def p1p2(input_file: str) -> tuple[int, str]:
    grid, folds = parse_input(input_file)

    grid.fold(folds[0][0], folds[0][1])
    part_1 = grid.num_dots()
    for fold_dimension, fold_value in folds[1:]:
        grid.fold(fold_dimension, fold_value)

    return (part_1, str(grid))


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1p2(cli_args[0]))
    stop = time.perf_counter()
    print(f"Elapsed: {stop - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
