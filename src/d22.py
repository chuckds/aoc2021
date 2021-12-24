#!/bin/env python3
"""
Advent Of Code 2021 Day 22
"""
from __future__ import annotations

import sys
import math
import time
import collections

from typing import NamedTuple, Iterable


class Range(NamedTuple):
    min: int
    max: int

    def length(self) -> int:
        return self.max - self.min + 1

    def contains(self, other: Range) -> bool:
        return all(self.min <= value <= self.max for value in other)

    def is_disjoint(self, other: Range) -> bool:
        return self.min > other.max or self.max < other.min

    def intersection(self, other: Range) -> Range:
        return Range(max(self.min, other.min), min(self.max, other.max))

    def add(self, other: Range) -> list[Range]:
        if self.is_disjoint(other):
            return [self, other]
        else:
            # Overlap
            return [Range(min(self.min, other.min), max(self.max, other.max))]

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

    def is_disjoint(self, other: Volume) -> bool:
        return any(self_range.is_disjoint(other_range)
                   for self_range, other_range in zip(self, other))

    def num_points_within(self) -> int:
        return math.prod(range.length() for range in self)

    def contains(self, other: Volume) -> bool:
        return all(self_range.contains(other_range)
                   for self_range, other_range in zip(self, other))

    def intersection(self, other: Volume) -> Volume:
        return Volume(*[self_range.intersection(other_range)
                        for self_range, other_range in zip(self, other)])

    def add(self, other: Volume) -> list[Volume]:
        if self.contains(other):
            return [self]
        elif other.contains(self):
            return [other]
        elif self.is_disjoint(other):
            return [self, other]
        else:
            return [volume for volume in self.non_overlapping([self, other])
                    if self.contains(volume) or other.contains(volume)]

    def subtract(self, other: Volume) -> list[Volume]:
        if self.is_disjoint(other):
            return [self]
        elif other.contains(self):  # Handled by case below but this is quicker
            return []
        else:
            return [volume for volume in self.non_overlapping([self, other])
                    if self.contains(volume) and not other.contains(volume)]

    @classmethod
    def non_overlapping(cls, volumes: Iterable[Volume]) -> Iterable[Volume]:
        for x_range in Range.non_overlapping(vol.x for vol in volumes):
            for y_range in Range.non_overlapping(vol.y for vol in volumes):
                for z_range in Range.non_overlapping(vol.z for vol in volumes):
                    yield Volume(x_range, y_range, z_range)

    def coords(self) -> Iterable[tuple[int, int, int]]:
        for x in range(self.x.min, self.x.max + 1):
            for y in range(self.y.min, self.y.max + 1):
                for z in range(self.z.min, self.z.max + 1):
                    yield (x, y, z)


def p1p2_getex3(input_file: str) -> tuple[int, int]:
    volumes: list[tuple[bool, Volume]] = []
    with open(input_file) as f:
        for line in f:
            action, coord_str = line.strip().split()
            dimention_ranges = []
            for dimention_str in coord_str.split(','):
                dimention_ranges.append(Range(*tuple(int(val) for val in dimention_str[2:].split('..')[:2])))
            volumes.append((action == "on", Volume(*dimention_ranges)))

    rev_volumes = list(reversed(volumes))
    num_points_on = 0
    for test_volume in Volume.non_overlapping([v for _, v in volumes]):
        for turn_on, volume in rev_volumes:
            if volume.contains(test_volume):
                if turn_on:
                    num_points_on += test_volume.num_points_within()
                # Stop at the first volume that contains this test
                # volume since we're iterating over the volumes in reverse
                break

    on_points: set[tuple[int, int, int]] = set()
    for turn_on, volume in [(to, v) for to, v in volumes if v.is_valid()]:
        if turn_on:
            on_points.update(volume.coords())
        else:
            on_points.difference_update(volume.coords())

    return (len(on_points), num_points_on)


def add_vol_to_vols(to_add: Volume, vols: list[Volume]) -> tuple[list[Volume], list[Volume]]:
    print(f"Adding {to_add} {len(vols)=}")
    new_vols = []
    all_dj = True
    for vol_idx, vol in enumerate(vols):
        if vol.is_disjoint(to_add):
            new_vols.append(vol)
        elif vol.contains(to_add):
            return vols[:]
        else:
            all_dj = False
            new_vols.append(vol)
            left_over_vols = [v for v in vol.add(to_add) if not vol.contains(v)]
            for left_over_vol in left_over_vols:
                new_vols.extend(add_vol_to_vols(left_over_vol, vols[vol_idx + 1:]))
    if all_dj:
        new_vols.append(to_add)

    return new_vols


def subtract_vol_from_vols(to_subtract: Volume, vols: list[Volume]) -> list[Volume]:
    print(f"Sub {to_subtract} {len(vols)=}")
    new_vols = []
    for vol in vols:
        if vol.is_disjoint(to_subtract):
            new_vols.append(vol)
        elif to_subtract.contains(vol):
            # Wipe this volume from the list
            pass
        else:
            new_vols.extend(vol.subtract(to_subtract))

    return new_vols


def add_vol_to_vols_i(to_add: Volume, vols: list[Volume]) -> tuple[list[Volume], list[Volume]]:
    print(f"Adding {to_add} {len(vols)=}")
    new_vols = []
    intersections = []
    for vol in vols:
        if vol.is_disjoint(to_add):
            new_vols.append(vol)
        elif vol.contains(to_add):
            return vols[:], []
        else:
            new_vols.append(vol)
            # Keep track of the intersections since these need to be removed
            # to avoid double counting
            intersections.append(vol.intersection(to_add))
    new_vols.append(to_add)

    return new_vols, intersections


def subtract_vol_from_vols_i(to_subtract: Volume, vols: list[Volume]) -> tuple[list[Volume], list[Volume]]:
    print(f"Sub {to_subtract} {len(vols)=}")
    new_vols = []
    intersections = []
    for vol in vols:
        if vol.is_disjoint(to_subtract):
            new_vols.append(vol)
        elif to_subtract.contains(vol):
            # Wipe this volume from the list
            pass
        else:
            new_vols.append(vol)
            intersections.append(vol.intersection(to_subtract))

    return new_vols, intersections


def p1p2(input_file: str) -> tuple[int, int]:
    volumes: list[tuple[bool, Volume]] = []
    with open(input_file) as f:
        for line in f:
            action, coord_str = line.strip().split()
            dimention_ranges = []
            for dimention_str in coord_str.split(','):
                dimention_ranges.append(Range(*tuple(int(val) for val in dimention_str[2:].split('..')[:2])))
            volumes.append((action == "on", Volume(*dimention_ranges)))

    on_vols: list[Volume] = []
    for turn_on, volume in volumes:
        if turn_on:
            on_vols = add_vol_to_vols(volume, on_vols)
        else:
            on_vols = subtract_vol_from_vols(volume, on_vols)
    print(on_vols)
    num_points_on = sum(vol.num_points_within() for vol in on_vols)

    on_points: set[tuple[int, int, int]] = set()
    for turn_on, volume in [(to, v) for to, v in volumes if v.is_valid()]:
        if turn_on:
            on_points.update(volume.coords())
        else:
            on_points.difference_update(volume.coords())

    return (len(on_points), num_points_on)


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1p2(cli_args[0]))
    print(f"Elapsed: {time.perf_counter() - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
