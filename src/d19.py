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


from typing import NamedTuple, Sequence


Matrix = Sequence[Sequence[int]]


def get_rotation_matrix(yaw_deg: float, pitch_deg: float, roll_deg: float) -> Matrix:
    yaw, pitch, roll = map(math.radians, (yaw_deg, pitch_deg, roll_deg))
    res = [
        [math.cos(yaw) * math.cos(pitch), math.cos(yaw) * math.sin(pitch) * math.sin(roll) - math.sin(yaw) * math.cos(roll), math.cos(yaw) * math.sin(pitch) * math.cos(roll) + math.sin(yaw) * math.sin(roll)],
        [math.sin(yaw) * math.cos(pitch), math.sin(yaw) * math.sin(pitch) * math.sin(roll) + math.cos(yaw) * math.cos(roll), math.sin(yaw) * math.sin(pitch) * math.cos(roll) - math.cos(yaw) * math.sin(roll)],
        [-1 * math.sin(pitch), math.cos(pitch) * math.sin(roll), math.cos(pitch) * math.cos(roll)],
    ]
    return [list(map(int, row)) for row in res]


def get_90_rotations() -> set[Matrix]:
    rotations = (0, 90, 180, 270)
    matricies: set[Matrix] = set()
    for yaw, pitch, roll in itertools.product(rotations, repeat=3):
        matricies.add(tuple(tuple(row) for row in get_rotation_matrix(
            yaw, pitch, roll)))
    return matricies


def inverse_mat(mat: Matrix) -> Matrix:
    return [x for x in zip(*mat)]


class Coord(NamedTuple):
    x: int
    y: int
    z: int

    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def manhatten(self, other: Coord) -> int:
        return sum(abs(self_v - other_v) for self_v, other_v in zip(self, other))

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


def mat_mult(mat_a: Matrix, mat_b: Matrix) -> Matrix:
    return [[sum(a * b for a, b in zip(a_row, b_col))
             for b_col in zip(*mat_b)]
            for a_row in mat_a]


@dataclasses.dataclass
class Scanner:
    id: int
    beacons: list[Coord] = dataclasses.field(default_factory=list)
    translation_to: dict[int, tuple[Coord, Matrix]] = dataclasses.field(default_factory=dict)
    mag_to_beacons: dict[float, set[Coord]] = dataclasses.field(default_factory=lambda: collections.defaultdict(set))

    def calc_mags(self) -> None:
        for beacon1, beacon2 in itertools.combinations(self.beacons, 2):
            mag = (beacon1 - beacon2).magnitude()
            self.mag_to_beacons[mag].add(beacon1)
            self.mag_to_beacons[mag].add(beacon2)


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

    scanners_by_id = {scanner.id: scanner for scanner in scanners}
    for scanner in scanners:
        scanner.calc_mags()

    rotation_mats = get_90_rotations()
    for scanner1, scanner2 in itertools.combinations(scanners, 2):
        mags_in_common = set(scanner1.mag_to_beacons.keys()) & set(scanner2.mag_to_beacons.keys())
        for mag in mags_in_common:
            if len(scanner1.mag_to_beacons[mag]) == 2 and len(scanner2.mag_to_beacons[mag]) == 2:
                # Let's try and find s2 offset from s1
                s1bs = list(scanner1.mag_to_beacons[mag])
                s2bs = list(scanner2.mag_to_beacons[mag])

                matching_translations = []
                for rot_mat in rotation_mats:
                    # Two possible pairings: s1b1 maps to s2b1 and s1b2 to s2b2 or
                    #                        s1b1 maps to s2b2 and s1b2 to s2b1
                    # Try both
                    for s2bs_mapped in (s2bs, s2bs[::-1]):
                        offsets = set()
                        for s1_b, s2_b in zip(s1bs, s2bs_mapped):
                            # s1 = (rotation @ s2) + offset
                            # offset = s1 - (rotation @ s2)
                            rotated = rotate_vector(rot_mat, s2_b)
                            offsets.add(s1_b - rotated)
                        if len(offsets) == 1:
                            # Found the offset and rotation!
                            matching_translations.append((offsets.pop(), rot_mat))
                if len(matching_translations) == 1:
                    offset, rot = matching_translations[0]
                    inv_rot = inverse_mat(rot)
                    scanner2.translation_to[scanner1.id] = matching_translations[0]
                    scanner1.translation_to[scanner2.id] = (Coord(*[-1 * v for v in rotate_vector(inv_rot, offset)]), inv_rot)
                    break

    sc0_in_all = False
    while not sc0_in_all:
        sc0_in_all = True
        for scanner in scanners:
            new_translations = {}
            for s2_id, (offset, rot) in scanner.translation_to.items():
                s2 = scanners_by_id[s2_id]
                for s3_id, (offset2, rot2) in s2.translation_to.items():
                    if s3_id not in scanner.translation_to and s3_id not in new_translations:
                        new_translations[s3_id] = (offset2 + rotate_vector(rot2, offset), mat_mult(rot2, rot))
            scanner.translation_to.update(new_translations)
            sc0_in_all &= 0 in scanner.translation_to

    scanner0_points = set(scanners[0].beacons[:])
    for scanner in scanners[1:]:
        offset, rot = scanner.translation_to[0]
        scanner0_points.update({rotate_vector(rot, beacon) + offset
                                for beacon in scanner.beacons})

    manhattens = [sc1.translation_to[0][0].manhatten(sc2.translation_to[0][0])
                  for sc1, sc2 in itertools.combinations(scanners, 2)]

    return (len(scanner0_points), max(manhattens))


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1p2(cli_args[0]))
    print(f"Elapsed: {time.perf_counter() - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
