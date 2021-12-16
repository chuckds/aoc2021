#!/bin/env python3
"""
Advent Of Code 2021 Day 5
"""

from __future__ import annotations

import sys
import time
import collections

from typing import Iterator


Point = collections.namedtuple('Point', ['x', 'y'])


def point_from_str(point_str: str) -> Point:
    return Point(int(point_str.split(',')[0]), int(point_str.split(',')[1]))


class Line:
    def __init__(self, start: Point, end: Point) -> None:
        self.start = start
        self.end = end
        self.delta_x = self.end.x - self.start.x
        self.delta_y = self.end.y - self.start.y
        self.is_45 = (self.delta_x and self.delta_y and
                      abs(self.delta_x) == abs(self.delta_y))

    def points_between(self) -> Iterator[Point]:
        if self.delta_x and self.delta_y and not self.is_45:
            # Diagonal not 45
            return

        num_steps = max(abs(self.delta_x), abs(self.delta_y))
        step_x = self.delta_x // num_steps
        step_y = self.delta_y // num_steps
        for i in range(num_steps + 1):
            yield Point(self.start.x + step_x * i, self.start.y + step_y * i)

    @classmethod
    def from_str(cls, line_str: str) -> Line:
        return cls(*[point_from_str(point_str)
                     for point_str in line_str.split(' -> ')])


def p1p2(input_file: str) -> tuple[int, int]:
    grid: dict[tuple[int, int], collections.Counter[str]] = \
                                   collections.defaultdict(collections.Counter)

    with open(input_file) as f:
        for line_str in f:
            line = Line.from_str(line_str)
            count = 'diag' if line.is_45 else 'h_and_v'
            for point in Line.from_str(line_str).points_between():
                grid[(point.x, point.y)].update({count: 1})

    results: list[int] = [0, 0]
    for counter in grid.values():
        if counter['h_and_v'] >= 2:
            results[0] += 1
            results[1] += 1
        elif (counter['h_and_v'] + counter['diag']) >= 2:
            results[1] += 1

    return (results[0], results[1])


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1p2(cli_args[0]))
    stop = time.perf_counter()
    print(f"Elapsed: {stop - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
