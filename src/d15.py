#!/bin/env python3
"""
Advent Of Code 2021 Day 15
"""

from __future__ import annotations

import sys
import time
import heapq
import collections

from typing import Iterable


Point = collections.namedtuple('Point', ['x', 'y'])


def neighbours(point: Point, size: Point) -> Iterable[Point]:
    for x_delta, y_delta in ((-1, 0), (0, 1), (1, 0), (0, -1)):
        new_x, new_y = point.x + x_delta, point.y + y_delta
        if 0 <= new_x < size.x and 0 <= new_y < size.y:
            yield Point(new_x, new_y)


def lowest_risk_get(rows: list[list[int]], size: Point) -> int:
    start = Point(0, 0)
    dest = Point(size.x - 1, size.y - 1)

    reachable_heapq: list[tuple[int, Point]] = []
    heapq.heappush(reachable_heapq, (0, start))
    lowest_risk_known: set[Point] = set([start])
    while reachable_heapq:
        risk, low_risk_point = heapq.heappop(reachable_heapq)
        if low_risk_point == dest:
            lowest_risk_to_dest = risk
            break
        for point in neighbours(low_risk_point, size):
            if point not in lowest_risk_known:
                # The first time we can reach a point will be the lowest risk
                # route to that point since all routes into a point incur the
                # same risk (not true of general path finding in graphs)
                # - ty to Jackson for pointing this out.
                lowest_risk_known.add(point)
                heapq.heappush(reachable_heapq,
                               (risk + rows[point.y][point.x], point))

    return lowest_risk_to_dest


def p1p2(input_file: str) -> tuple[int, int]:
    p1_rows, p2_rows = [], []
    with open(input_file) as f:
        for line in f:
            p1_rows.append([int(char) for char in line.strip()])

    p1_size = Point(len(p1_rows[0]), len(p1_rows))
    p2_size = Point(p1_size.x * 5, p1_size.y * 5)
    # Extend across
    for row in p1_rows:
        new_row = row * 5
        for x in range(p1_size.x):
            for repeat in range(1, 5):
                index = x + (repeat * p1_size.x)
                new_row[index] = ((row[x] + repeat - 1) % 9) + 1
        p2_rows.append(new_row)
    # Now extend down
    for repeat in range(1, 5):
        for y in range(p1_size.y):
            new_row = p2_rows[y][:]
            for x in range(p2_size.x):
                new_row[x] = ((p2_rows[y][x] + repeat - 1) % 9) + 1
            p2_rows.append(new_row)

    return (lowest_risk_get(p1_rows, p1_size),
            lowest_risk_get(p2_rows, p2_size))


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1p2(cli_args[0]))
    stop = time.perf_counter()
    print(f"Elapsed: {stop - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
