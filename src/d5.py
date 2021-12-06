#!/bin/env python3
"""
Advent Of Code 2021 Day 5
"""

from __future__ import annotations

import sys
import time
import collections
import dataclasses
from typing import Iterator


@dataclasses.dataclass
class Point:
    x: int
    y: int

    @classmethod
    def from_str(cls, point_str: str) -> Point:
        return cls(int(point_str.split(',')[0]), int(point_str.split(',')[1]))


@dataclasses.dataclass
class Line:
    start: Point
    end: Point

    def points_between(self, allow_45: bool = False) -> Iterator[Point]:
        delta_x = self.end.x - self.start.x
        delta_y = self.end.y - self.start.y

        if delta_x and delta_y and (not allow_45 or (abs(delta_x) != abs(delta_y))):
            # Diagonal but not 45 degrees
            return
        
        num_steps = max(abs(delta_x), abs(delta_y))
        step_x = delta_x // num_steps
        step_y = delta_y // num_steps
        for i in range(num_steps + 1):
            yield Point(self.start.x + step_x * i, self.start.y + step_y * i)

    @classmethod
    def from_str(cls, line_str: str) -> Line:
        return cls(*[Point.from_str(point_str) for point_str in line_str.split(' -> ')])


def safe_point(input_file: str, allow_45: bool = False) -> int:
    grid: dict[tuple[int, int], int] = collections.defaultdict(int)

    with open(input_file) as f:
        for line_str in f:
            for point in Line.from_str(line_str).points_between(allow_45):
                grid[(point.x, point.y)] += 1

    return sum(1 for count in grid.values() if count >= 2)


def p2(input_file: str) -> int:
    return safe_point(input_file, True)


def p1(input_file: str) -> int:
    return safe_point(input_file, False)


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1(cli_args[0]))
    print(p2(cli_args[0]))
    stop = time.perf_counter()
    print(f"Elapsed: {stop - start}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))