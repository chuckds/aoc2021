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
        self.x_size = 0
        self.y_size = 0
        self.rows: dict[int, set[int]] = collections.defaultdict(set)
        self.cols: dict[int, set[int]] = collections.defaultdict(set)

    def add_dot(self, x: int, y: int) -> None:
        self.rows[y].add(x)
        self.cols[x].add(y)
        self.x_size = max(self.x_size, x + 1)
        self.y_size = max(self.y_size, y + 1)

    def merge_line_into(self, a_line: int, dest_line: int, up: bool = True) -> None:
        if up:
            merging, update = self.rows, self.cols
        else:
            merging, update = self.cols, self.rows

        for new_dot in merging[a_line] - merging[dest_line]:
            merging[dest_line].add(new_dot)
            update[new_dot].add(dest_line)

    def fold_up(self, val: int) -> None:
        for fold_line, into_line in zip(range(val + 1, self.y_size), range(val - 1, -1, -1)):
            self.merge_line_into(fold_line, into_line)
        self.y_size = val

    def fold_left(self, val: int) -> None:
        for fold_line, into_line in zip(range(val + 1, self.x_size), range(val - 1, -1, -1)):
            self.merge_line_into(fold_line, into_line, False)
        self.x_size = val

    def fold(self, dimension: str, val: int) -> None:
        if dimension == 'x':
            self.fold_left(val)
        else:
            self.fold_up(val)

    def num_dots(self) -> int:
        num_dots = 0
        for row_y, row in self.rows.items():
            if row_y < self.y_size:
                num_dots += sum(1 for d in row if d < self.x_size)
        return num_dots

    def __str__(self) -> str:
        result = ""
        for y in range(0, self.y_size):
            for x in range(0, self.x_size):
                if x in self.rows.get(y, set()):
                    result += "#"
                else:
                    result += "."
            result += "\n"
        return result


def parse_input(input_file: str) -> tuple[Grid, list[FoldType]]:
    folds = []
    grid = Grid()
    in_fold_section = False
    with open(input_file) as f:
        for line in f:
            line = line.strip()
            if in_fold_section:
                _, _, fold_line = line.split(' ')
                dimension, value = fold_line.split('=')
                folds.append((dimension, int(value)))
            elif not line:
                # Blank line that sepearated the dot section from the fold section
                in_fold_section = True
            else:
                # Still in the dot section
                x, y = line.split(',')
                grid.add_dot(int(x), int(y))
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