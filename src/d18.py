#!/bin/env python3
"""
Advent Of Code 2021 Day 18
"""
from __future__ import annotations

import sys
import time
import dataclasses

from typing import Union, Any, Optional, Iterable


@dataclasses.dataclass
class SnailfishNumber:
    parent: Optional[SnailfishNumber]
    l: Union[int, SnailfishNumber]
    r: Union[int, SnailfishNumber]

    def __post_init__(self) -> None:
        if isinstance(self.l, SnailfishNumber):
            self.l.parent = self
        if isinstance(self.r, SnailfishNumber):
            self.r.parent = self

    def reduce(self) -> None:
        reduce = True
        while reduce:
            if not self.explode():
                reduce = self.split()

    def explode(self) -> bool:
        child_to_explode = next(self.get_too_deep(), None)  # type: ignore
        if child_to_explode is None:
            return False
        assert isinstance(child_to_explode.l, int)
        assert isinstance(child_to_explode.r, int)
        assert child_to_explode.parent is not None

        left_sfn, left_idx = child_to_explode.number_to_left()
        if left_sfn:
            if left_idx == 0:
                assert isinstance(left_sfn.l, int)
                left_sfn.l += child_to_explode.l
            else:
                assert isinstance(left_sfn.r, int)
                left_sfn.r += child_to_explode.l
        right_sfn, right_idx = child_to_explode.number_to_right()
        if right_sfn:
            if right_idx == 0:
                assert isinstance(right_sfn.l, int)
                right_sfn.l += child_to_explode.r
            else:
                assert isinstance(right_sfn.r, int)
                right_sfn.r += child_to_explode.r

        # Now zero out this exploded SFN
        if child_to_explode.parent.l is child_to_explode:
            child_to_explode.parent.l = 0
        else:
            assert child_to_explode.parent.r is child_to_explode
            child_to_explode.parent.r = 0
        return True

    def linearize(self) -> Iterable[tuple[int, SnailfishNumber, int]]:
        for idx, child in enumerate((self.l, self.r)):
            if isinstance(child, SnailfishNumber):
                yield from child.linearize()
            else:
                yield (child, self, idx)

    def get_too_deep(self, depth: int = 0) -> Iterable[SnailfishNumber]:
        if depth == 4:
            yield self
        else:
            for child in (self.l, self.r):
                if isinstance(child, SnailfishNumber):
                    yield from child.get_too_deep(depth + 1)

    def split(self) -> bool:
        did_split = False
        for number, sfn, idx in self.linearize():
            if number >= 10:
                new_sfn = SnailfishNumber(sfn, number // 2, number - (number // 2))
                if idx == 0:
                    sfn.l = new_sfn
                else:
                    sfn.r = new_sfn
                did_split = True
                break
        return did_split

    def magnitude(self) -> int:
        magnitude = 0
        for child, multiplier in zip((self.l, self.r), (3, 2)):
            if isinstance(child, SnailfishNumber):
                magnitude += multiplier * child.magnitude()
            else:
                magnitude += multiplier * child
        return magnitude

    def number_to_left(self) -> tuple[Optional[SnailfishNumber], int]:
        # Go up until a parent has a left that isn't the child
        parent, child = self.parent, self
        while parent is not None and parent.l is child:
            child = parent
            parent = parent.parent
        if parent is not None:
            if isinstance(parent.l, SnailfishNumber):
                return (parent.l.rightmost_number(), 1)
            else:
                return (parent, 0)
        else:
            return (None, 0)

    def number_to_right(self) -> tuple[Optional[SnailfishNumber], int]:
        # Go up until a parent has a right that isn't the child
        parent, child = self.parent, self
        while parent is not None and parent.r is child:
            child = parent
            parent = parent.parent
        if parent is not None:
            if isinstance(parent.r, SnailfishNumber):
                return (parent.r.leftmost_number(), 0)
            else:
                return (parent, 1)
        else:
            return (None, 0)

    def leftmost_number(self) -> SnailfishNumber:
        sfn = self
        while isinstance(sfn.l, SnailfishNumber):
            sfn = sfn.l
        return sfn

    def rightmost_number(self) -> SnailfishNumber:
        sfn = self
        while isinstance(sfn.r, SnailfishNumber):
            sfn = sfn.r
        return sfn

    def __add__(self, other: SnailfishNumber) -> SnailfishNumber:
        res = SnailfishNumber(None, self, other)
        res.reduce()
        return res

    def __repr__(self) -> str:
        return f"[{str(self.l)},{str(self.r)}]"

    @classmethod
    def from_list(cls, lists: list[Any]) -> SnailfishNumber:
        args: list[Union[int, SnailfishNumber]] = []
        for item in lists:
            if isinstance(item, int):
                args.append(item)
            else:
                args.append(SnailfishNumber.from_list(item))
        return SnailfishNumber(None, *args)


def p1p2(input_file: str) -> tuple[int, int]:
    with open(input_file) as f:
        number_lists = [eval(line.strip()) for line in f]

    snailfish_numbers = [SnailfishNumber.from_list(nl) for nl in number_lists]
    result = snailfish_numbers[0]
    for sfn in snailfish_numbers[1:]:
        result = result + sfn

    max_mag = 0
    for idx1, nl1 in enumerate(number_lists):
        for idx2, nl2 in enumerate(number_lists):
            if idx1 != idx2:
                res = SnailfishNumber.from_list(nl1) + SnailfishNumber.from_list(nl2)
                mag = res.magnitude()
                if mag > max_mag:
                    max_mag = mag

    return (result.magnitude(), max_mag)


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1p2(cli_args[0]))
    print(f"Elapsed: {time.perf_counter() - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
