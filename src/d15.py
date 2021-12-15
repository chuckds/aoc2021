#!/bin/env python3
"""
Advent Of Code 2021 Day 15
"""

from __future__ import annotations

import sys
import time
import collections

from typing import Iterable


Point = collections.namedtuple('Point', ['x', 'y'])


def neighbours(point: Point, size: Point) -> Iterable[Point]:
    for x_delta, y_delta in ((-1, 0), (0, 1), (1, 0), (0, -1)):
        new_x, new_y  = point.x + x_delta, point.y + y_delta
        if 0 <= new_x < size.x and 0 <= new_y < size.y:
            yield Point(new_x, new_y)


def lowest_risk_get(rows: list[list[int]], size: Point) -> int:
    destination = Point(size.x - 1, size.y - 1)
    reachable_positions: dict[Point, int] = {Point(0, 0) : 0}
    lowest_risk_known: dict[Point, int] = {}
    while reachable_positions:
        lowest_risk_reachable_point, lowest_risk_value = sorted(reachable_positions.items(), key=lambda x: x[1])[0]
        if lowest_risk_reachable_point == destination:
            lowest_risk_to_dest = lowest_risk_value
            break
        del reachable_positions[lowest_risk_reachable_point]
        lowest_risk_known[lowest_risk_reachable_point] = lowest_risk_value
        for point in neighbours(lowest_risk_reachable_point, size):
            if point not in lowest_risk_known:
                risk_to_point = lowest_risk_value + rows[point.y][point.x]
                current_lowest_risk_to_point = reachable_positions.get(point, None)
                if (current_lowest_risk_to_point is None or
                    risk_to_point < current_lowest_risk_to_point):
                    # First time we can reach this point or better risk score
                    # than how we could reach it before
                    reachable_positions[point] = risk_to_point
    return lowest_risk_to_dest


def p1p2(input_file: str) -> tuple[int, int]:
    rows = []
    with open(input_file) as f:
        for line in f:
            rows.append([int(char) for char in line.strip()])

    size = Point(len(rows[0]), len(rows))
    p1_lowest_risk = lowest_risk_get(rows, size)

    # p2
    new_size = Point(size.x * 5, size.y * 5)
    new_rows = []
    # Extend across
    for row in rows:
        new_row = row * 5
        for x in range(size.x):
            for repeat in range(1, 5):
                new_row[x + (repeat * size.x)] = ((row[x] + repeat - 1) % 9) + 1
        new_rows.append(new_row)
    # Now extend down
    for repeat in range(1, 5):
        for y in range(size.y):
            new_row = new_rows[y][:]
            for x in range(new_size.x):
                new_row[x] = ((new_rows[y][x] + repeat - 1) % 9) + 1
            new_rows.append(new_row)
    p2_lowest_risk = lowest_risk_get(new_rows, new_size)

    return (p1_lowest_risk, p2_lowest_risk)


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1p2(cli_args[0]))
    stop = time.perf_counter()
    print(f"Elapsed: {stop - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))