#!/bin/env python3
"""
Advent Of Code 2021 Day 22
"""

import sys
import time

from typing import NamedTuple, Iterable


class Volume(NamedTuple):
    turn_on: bool
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    z_min: int
    z_max: int

    def is_valid(self) -> bool:
        return all(-50 <= val <= 50 for val in self[1:])

    def coords(self) -> Iterable[tuple[int, int, int]]:
        for x in range(self.x_min, self.x_max + 1):
            for y in range(self.y_min, self.y_max + 1):
                for z in range(self.z_min, self.z_max + 1):
                    yield (x, y, z)


def p1p2(input_file: str) -> tuple[int, int]:
    volumes: list[Volume] = []
    with open(input_file) as f:
        for line in f:
            action, coord_str = line.strip().split()
            coords = []
            for dimention_str in coord_str.split(','):
                coords.extend(list(int(val) for val in dimention_str[2:].split('..')[:2]))
            volumes.append(Volume(action == "on", *coords))

    volumes = [v for v in volumes if v.is_valid()]
    on_points: set[tuple[int, int, int]] = set()
    for v in volumes:
        if v.turn_on:
            on_points.update(v.coords())
        else:
            on_points.difference_update(v.coords())

    return (len(on_points), 0)


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1p2(cli_args[0]))
    print(f"Elapsed: {time.perf_counter() - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
