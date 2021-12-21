#!/bin/env python3
"""
Advent Of Code 2021 Day 19
"""

from __future__ import annotations

import sys
import math
import time
import itertools
import dataclasses
import collections


from typing import NamedTuple, Optional, Sequence, Any, Iterable


Matrix = Sequence[Sequence[int]]


def get_rotation_matrix(yaw: float, pitch: float, roll: float) -> Matrix:
    res = [
        [math.cos(yaw) * math.cos(pitch), math.cos(yaw) * math.sin(pitch) * math.sin(roll) - math.sin(yaw) * math.cos(roll), math.cos(yaw) * math.sin(pitch) * math.cos(roll) + math.sin(yaw) * math.sin(roll)], 
        [math.sin(yaw) * math.cos(pitch), math.sin(yaw) * math.sin(pitch) * math.sin(roll) + math.cos(yaw) * math.cos(roll), math.sin(yaw) * math.sin(pitch) * math.cos(roll) - math.cos(yaw) * math.sin(roll)],
        [-1 * math.sin(pitch), math.cos(pitch) * math.sin(roll), math.cos(pitch) * math.cos(roll)],
    ]
    return [list(map(int, row)) for row in res]


def get_90_rotations() -> set[Matrix]:
    rotations = (0, 90, 180, 270)
    matricies = set()
    for yaw in rotations:
        for pitch in rotations:
            for roll in rotations:
                matricies.add(get_rotation_matrix(
                    math.radians(yaw), math.radians(pitch), math.radians(roll)))
    return matricies


def combinations(a_iter: Sequence[Any]) -> Iterable[tuple[Any, Any]]:
    for item_idx, item1 in enumerate(a_iter[:-1]):
        for item2 in a_iter[item_idx + 1:]:
            yield item1, item2


def triangular_num(n: int) -> int:
    return (n * (n + 1)) // 2


def inverse_triangular_num(n: int) -> int:
    sq = math.sqrt(8 * n + 1)
    assert sq == int(sq)
    answer = (int(sq) - 1) / 2
    assert answer == int(answer)
    return int(answer)


class Coord(NamedTuple):
    x: int
    y: int
    z: int

    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def __add__(self, other: Coord) -> Coord:  # type: ignore
        return Coord(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Coord) -> Coord:
        return Coord(self.x - other.x, self.y - other.y, self.z - other.z)


def rotate_vector(rot_mat: Matrix, vector: Coord) -> Coord:
    coords = []
    for row in rot_mat:
        coords.append(sum(rot_val * vec_val
                          for rot_val, vec_val in zip(row, vector)))
    return Coord(*coords)


@dataclasses.dataclass
class Scanner:
    id: int
    beacons: list[Coord] = dataclasses.field(default_factory=list)
    offsets_from: dict[int, tuple[Coord,Matrix]] = dataclasses.field(default_factory=dict)
    mag_to_beacons: Optional[dict[float, set[Coord]]] = None
    beacon_to_mag: Optional[dict[Coord, dict[float, Coord]]] = None
    translated_beacons: set[Coord] = dataclasses.field(default_factory=set)

    def calc_mags(self) -> None:
        self.mag_to_beacons = collections.defaultdict(set)
        self.beacon_to_mag = collections.defaultdict(dict)
        for beacon1, beacon2 in itertools.combinations(self.beacons, 2):
            mag = (beacon1 - beacon2).magnitude()
            self.mag_to_beacons[mag].add(beacon1)
            self.mag_to_beacons[mag].add(beacon2)
            self.beacon_to_mag[beacon1][mag] = beacon2
            self.beacon_to_mag[beacon2][mag] = beacon1


def p1p2(input_file: str) -> tuple[int, int]:
    scanners: list[Scanner] = []
    with open(input_file) as f:
        for line in f:
            if line.startswith('---'):
                scanner_id = line.strip().removeprefix('--- scanner ').removesuffix(' ---')
                scanners.append(Scanner(int(scanner_id)))
            else:
                line = line.strip()
                if line:
                    scanners[-1].beacons.append(Coord(*[int(c) for c in line.split(',')]))

    rotation_mats = get_90_rotations()
    all_points = set()
    for scanner in scanners:
        scanner.calc_mags()
        all_points.update({(scanner.id, beacon) for beacon in scanner.beacons})

    unique_points = all_points
    for scanner1, scanner2 in combinations(scanners):
        # Do theses scans have at least 12 beacons in common?
        # 12 beacons have triangular_num(12 - 1) (66) paths between them so
        # scanners would need at have at lease this many magnitudes in common
        mags_in_common = set(scanner1.mag_to_beacons.keys()) & set(scanner2.mag_to_beacons.keys())
        s2_beacons_in_common = set()
        for mag in mags_in_common:
            s2_beacons_in_common.update(scanner2.mag_to_beacons[mag])
            if len(scanner1.mag_to_beacons[mag]) == 2 and len(scanner2.mag_to_beacons[mag]) == 2:
                # Let's try and find s2 offset from s1
                s1bs = list(scanner1.mag_to_beacons[mag])
                s2bs = list(scanner2.mag_to_beacons[mag])

                founds = []
                for rot_mat in rotation_mats:
                    # Two possible pairings: s1b1 maps to s2b1 and s1b2 to s2b2 or
                    #                        s1b1 maps to s2b2 and s1b2 to s2b1
                    # Try both
                    for s2bs in (s2bs, s2bs[::-1]):
                        offsets = set()
                        for s1_b, s2_b in zip(s1bs, s2bs):
                            rotated = rotate_vector(rot_mat, s2_b)
                            offsets.add(s1_b - rotated)
                        if len(offsets) == 1:
                            # Found the offset and rotation!
                            founds.append((offsets.pop(), rot_mat))
                if len(founds) == 1:
                    # WHoop only one
                    print(f"hllow!: {scanner1.id} {scanner2.id} {founds=}")
                    scanner2.offsets_from[scanner1.id] = founds[0]
                    break

        offset, rotation = scanner2.offsets_from.get(scanner1.id, (None, None))
        if offset:
            # Translate s2 beacons to s1
            if not scanner1.translated_beacons:
                # Add s1's own beacons to the set first
                scanner1.translated_beacons.update(scanner1.beacons)
            s2_translated = {rotate_vector(rotation, beacon) + offset
                             for beacon in scanner2.beacons}
            overlap = scanner1.translated_beacons & s2_translated
            print(f"{len(overlap)=}")
            scanner1.translated_beacons.update(s2_translated)

        unique_points.difference_update({(scanner2.id, beacon) for beacon in s2_beacons_in_common})

    return (len(unique_points), 0)


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1p2(cli_args[0]))
    print(f"Elapsed: {time.perf_counter() - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
