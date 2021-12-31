#!/bin/env python3
"""
Advent Of Code 2021 Day 22
"""
from __future__ import annotations

import sys
import math
import time
import itertools
import collections

from typing import NamedTuple, Iterable, Optional


class Range(NamedTuple):
    min: int
    max: int

    def length(self) -> int:
        return self.max - self.min + 1

    def merge(self, other: Range) -> Optional[Range]:
        if self.min == other.max + 1:
            return Range(other.min, self.max)
        elif self.max + 1 == other.min:
            return Range(self.min, other.max)
        return None

    def contains(self, other: Range) -> bool:
        return all(self.min <= value <= self.max for value in other)

    def is_disjoint(self, other: Range) -> bool:
        return self.min > other.max or self.max < other.min

    def subtract(self, other: Range) -> list[Range]:
        if self.is_disjoint(other):
            return [self]
        else:
            ranges = list(self.non_overlapping([self, other]))
            assert len(ranges) == 3
            # Middle one is the intersection which we don't want
            return [r for r in ranges[::2] if self.contains(r)]

    @classmethod
    def non_overlapping(cls, ranges: Iterable[Range]) -> Iterable[Range]:
        min_list, max_list = [], []
        for range in ranges:
            min_list.append(range.min)
            max_list.append(range.max)
        mins = collections.deque(sorted(
            collections.Counter(min_list).items()))
        maxs = collections.deque(sorted(
            collections.Counter(max_list).items()))

        last_min = None
        open_ranges = 0
        while maxs:
            if mins and mins[0][0] <= maxs[0][0]:
                new_min, count = mins.popleft()
                open_ranges += count
                if last_min is not None:
                    yield Range(last_min, new_min - 1)
                last_min = new_min
            else:
                assert last_min is not None
                new_max, count = maxs.popleft()
                open_ranges -= count
                yield Range(last_min, new_max)
                if open_ranges > 0:
                    last_min = new_max + 1
                else:
                    last_min = None


class Volume(NamedTuple):
    x: Range
    y: Range
    z: Range

    def is_valid(self) -> bool:
        return all(-50 <= val <= 50 for d_range in self for val in d_range)

    def merge(self, other: Volume) -> Optional[Volume]:
        new_ranges = []
        merged_range = None
        for self_range, other_range in zip(self, other):
            if self_range == other_range:
                new_ranges.append(self_range)
            elif merged_range is None:
                merged_range = self_range.merge(other_range)
                if merged_range is None:
                    # All ranges have to either be mergable or equal this is
                    # neither so this volume can't be merged
                    break
                else:
                    new_ranges.append(merged_range)
            else:
                break

        return Volume(*new_ranges) if len(new_ranges) == 3 else None

    def is_disjoint(self, other: Volume) -> bool:
        return any(self_range.is_disjoint(other_range)
                   for self_range, other_range in zip(self, other))

    def num_points_within(self) -> int:
        return math.prod(range.length() for range in self)

    def contains(self, other: Volume) -> bool:
        return all(self_range.contains(other_range)
                   for self_range, other_range in zip(self, other))

    def subtract(self, other: Volume) -> list[Volume]:
        if self.is_disjoint(other):
            return [self]
        elif other.contains(self):  # Handled by case below but this is quicker
            return []
        else:
            new_vols = [volume for volume in self.non_overlapping([self, other])
                        if self.contains(volume) and not other.contains(volume)]

            merged: Optional[Volume] = self
            while merged and len(new_vols) > 1:
                for vol_a, vol_b in itertools.combinations(new_vols, 2):
                    merged = vol_a.merge(vol_b)
                    if merged is not None:
                        new_vols = [v for v in new_vols if v not in (vol_a, vol_b)]
                        new_vols.append(merged)
                        break
            return new_vols

    @classmethod
    def non_overlapping(cls, volumes: Iterable[Volume]) -> Iterable[Volume]:
        for x_range in Range.non_overlapping(vol.x for vol in volumes):
            for y_range in Range.non_overlapping(vol.y for vol in volumes):
                for z_range in Range.non_overlapping(vol.z for vol in volumes):
                    yield Volume(x_range, y_range, z_range)


def add_vol_to_vols(to_add: Volume, vols: list[Volume], start_at: int = 0) -> list[Volume]:
    new_vols = []
    all_disjoint = True
    for vol_idx in range(start_at, len(vols)):
        vol = vols[vol_idx]
        if vol.contains(to_add):
            return []
        elif not vol.is_disjoint(to_add):
            all_disjoint = False
            for left_over_vol in to_add.subtract(vol):
                new_vols.extend(add_vol_to_vols(left_over_vol, vols, vol_idx + 1))
            break
    if all_disjoint:
        new_vols.append(to_add)

    return new_vols


def subtract_vol_from_vols(to_subtract: Volume, vols: list[Volume]) -> list[Volume]:
    new_vols = [vol.subtract(to_subtract) for vol in vols]
    return [vol for vol_sublist in new_vols for vol in vol_sublist]


def get_number_points_on(volumes: list[tuple[bool, Volume]]) -> int:
    on_vols: list[Volume] = []
    for turn_on, volume in volumes:
        if turn_on:
            on_vols.extend(add_vol_to_vols(volume, on_vols))
        else:
            on_vols = subtract_vol_from_vols(volume, on_vols)
    return sum(vol.num_points_within() for vol in on_vols)


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

    p1 = get_number_points_on([(turn_on, v)
                               for turn_on, v in volumes if v.is_valid()])
    p2 = get_number_points_on(volumes)
    return (p1, p2)


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1p2(cli_args[0]))
    print(f"Elapsed: {time.perf_counter() - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
