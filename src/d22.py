#!/bin/env python3
"""
Advent Of Code 2021 Day 22
"""
from __future__ import annotations

import sys
import math
import time
import itertools

from typing import NamedTuple


class Range(NamedTuple):
    min: int
    max: int

    def length(self) -> int:
        return self.max - self.min + 1

    def intersection(self, other: Range) -> Range:
        return Range(max(self.min, other.min), min(self.max, other.max))

    def is_disjoint(self, other: Range) -> bool:
        return self.min > other.max or self.max < other.min


class Volume(NamedTuple):
    x: Range
    y: Range
    z: Range

    def is_valid(self) -> bool:
        return all(-50 <= val <= 50 for d_range in self for val in d_range)

    def volume(self) -> int:
        return math.prod(range.length() for range in self)

    def intersection(self, other: Volume) -> Volume:
        return Volume(*[self_range.intersection(other_range)
                        for self_range, other_range in zip(self, other)])

    def is_disjoint(self, other: Volume) -> bool:
        return any(self_range.is_disjoint(other_range)
                   for self_range, other_range in zip(self, other))


def count_points_within(vols: list[Volume]) -> int:
    point_count = sum(v.volume() for v in vols)
    for vol_idx, vol in enumerate(vols):
        overlapping = [v.intersection(vol) for v in itertools.islice(vols, vol_idx) if not v.is_disjoint(vol)]
        point_count -= count_points_within(overlapping)
    return point_count


def get_number_points_on(volumes: list[tuple[bool, Volume]]) -> int:
    on_count = 0
    for vol_idx, (turn_on, vol) in enumerate(reversed(volumes)):
        if turn_on:
            overlapping = [v.intersection(vol) for _, v in
                           itertools.islice(reversed(volumes), vol_idx) if not v.is_disjoint(vol)]
            on_count += vol.volume() - count_points_within(overlapping)
    return on_count


def p1p2(input_file: str) -> tuple[int, int]:
    volumes: list[tuple[bool, Volume]] = []
    with open(input_file) as f:
        for line in f:
            action, coord_str = line.strip().split()
            dimention_ranges = []
            for dimention_str in coord_str.split(','):
                dimention_ranges.append(Range(*tuple(
                    int(val) for val in dimention_str[2:].split('..')[:2])))
            volumes.append((action == "on", Volume(*dimention_ranges)))

    p1 = get_number_points_on([(turn_on, v) for turn_on, v in volumes if v.is_valid()])
    p2 = get_number_points_on(volumes)
    return (p1, p2)


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1p2(cli_args[0]))
    print(f"Elapsed: {time.perf_counter() - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
