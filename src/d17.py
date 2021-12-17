#!/bin/env python3
"""
Advent Of Code 2021 Day 17
"""

import sys
import math
import time

from typing import NamedTuple, cast, Iterable


class Point(NamedTuple):
    x: int
    y: int


def probe_posns(start: Point, v_init: Point, max_steps: int) -> Iterable[Point]:
    probe_posn = start
    v = v_init
    for _ in range(0, max_steps):
        probe_posn = Point(probe_posn.x + v.x, probe_posn.y + v.y)
        yield probe_posn
        v = Point((v.x - 1) if v.x else 0, v.y - 1)


def hits_target(velocity: Point, target_xs: tuple[int, int],
                target_ys: tuple[int, int], max_steps: int) -> bool:
    for probe_posn in probe_posns(Point(0, 0), velocity, max_steps):
        if (min(target_xs) <= probe_posn.x <= max(target_xs) and
            min(target_ys) <= probe_posn.y <= max(target_ys)):
            return True
        if max(target_xs) < probe_posn.x or min(target_ys) > probe_posn.y:
            # Overshoot
            return False
    return False


def p1p2(input_file: str) -> tuple[int, int]:
    with open(input_file) as f:
        xs_str, ys_str = next(f)[len("target area: "):].strip().split(', ')
        # Is there are way of doing this without the cast?
        xs = cast(tuple[int, int],
                  tuple(int(val) for val in xs_str[2:].split('..')[:2]))
        ys = cast(tuple[int, int],
                  tuple(int(val) for val in ys_str[2:].split('..')[:2]))

    # Vmax
    # - x - jump to the furthest edge of the target in one step
    # - y go as high as possible before dropping back down to target
    v_max = Point(max(xs), -1 * (min(ys) + 1))
    # Vmin
    # - x solve the quadratic
    # - y Jump there in one step - large negative
    v_min = Point(math.ceil((1 + math.sqrt(1 + 4 * min(xs))) / 2),
                  min(ys))
    max_steps = (2 * v_max.y) + 2
    vs_valid = [(x_vel, y_vel)
                for x_vel in range(v_min.x, v_max.x + 1)
                for y_vel in range(v_min.y, v_max.y + 1)
                if hits_target(Point(x_vel, y_vel), xs, ys, max_steps)]

    return ((v_max.y * (v_max.y + 1)) // 2, len(vs_valid))


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1p2(cli_args[0]))
    print(f"Elapsed: {time.perf_counter() - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
