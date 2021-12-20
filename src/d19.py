#!/bin/env python3
"""
Advent Of Code 2021 Day 19
"""

from __future__ import annotations

import sys
import math
import time
import dataclasses
import collections


from typing import NamedTuple, Optional, Sequence, Any, Iterable


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

    def __sub__(self, other: Coord) -> Coord:
        return Coord(self.x - other.x, self.y - other.y, self.z - other.z)


@dataclasses.dataclass
class Scanner:
    id: int
    beacons: list[Coord] = dataclasses.field(default_factory=list)
    mag_to_beacons: Optional[dict[float, set[Coord]]] = None
    beacon_to_mag: Optional[dict[Coord, dict[float, Coord]]] = None

    def calc_mags(self) -> None:
        self.mag_to_beacons = collections.defaultdict(set)
        self.beacon_to_mag = collections.defaultdict(dict)
        for beacon1, beacon2 in combinations(self.beacons):
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

        #print(f"{scanner1.id=} {scanner2.id=} {len(mags_in_common)}")
        s1_beacons_in_common = set()
        s2_beacons_in_common = set()
        for mag in mags_in_common:
            s1_beacons_in_common.update(scanner1.mag_to_beacons[mag])
            s2_beacons_in_common.update(scanner2.mag_to_beacons[mag])
        #if mags_in_common:
            #print(f"{len(s1_beacons_in_common)=} {s1_beacons_in_common=}")
            #print(f"{len(s2_beacons_in_common)=} {s2_beacons_in_common=}")
        unique_points.difference_update({(scanner2.id, beacon) for beacon in s2_beacons_in_common})
        if len(mags_in_common) >= 66:
            # Something
            pass

    #print(f"{len(unique_points)=}")
    # Assume magnitude of vectors between points are unique and that no
    # scanner detection cube overlaps just 1 beacon with the rest
    #seen_mags = collections.defaultdict(set)
    #for scanner in scanners:
    #    for mag in scanner.mag_to_beacons:
    #        seen_mags[mag].add(scanner.id)

    return (len(unique_points), 0)


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1p2(cli_args[0]))
    print(f"Elapsed: {time.perf_counter() - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
