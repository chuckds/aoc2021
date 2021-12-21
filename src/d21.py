#!/bin/env python3
"""
Advent Of Code 2021 Day 21
"""
from __future__ import annotations

import sys
import time
import collections
import dataclasses

from typing import NamedTuple, Iterable


def three_dice() -> Iterable[int]:
    for die_roll1 in (1, 2, 3):
        for die_roll2 in (1, 2, 3):
            for die_roll3 in (1, 2, 3):
                yield die_roll1 + die_roll2 + die_roll3


class Play(NamedTuple):
    position: int
    score: int = 0

    def with_roll(self, dice_roll: int) -> Play:
        new_pos = ((self.position - 1 + dice_roll) % 10) + 1
        return Play(new_pos, self.score + new_pos)


def p2(input_file: str) -> int:
    with open(input_file) as f:
        players = [Play(int(line.strip().split()[-1])) for line in f]

    game_state_counts = collections.defaultdict(int)
    game_state_counts[players[0], players[1]] = 1
    p1_wins = 0
    dice_sums = collections.Counter(three_dice())
    while game_state_counts:
        next_round: collections.defaultdict[tuple[Play, Play], int] = collections.defaultdict(int)
        for (play1, play2), count in game_state_counts.items():
            for p1_dice, p1_dice_count in dice_sums.items():
                p1_new = play1.with_roll(p1_dice)
                if p1_new.score >= 21:
                    p1_wins += count * p1_dice_count
                else:
                    for p2_dice, p2_dice_count in dice_sums.items():
                        p2_new = play2.with_roll(p2_dice)
                        if p2_new.score < 21:
                            next_round[(p1_new, p2_new)] += count * p2_dice_count * p1_dice_count
        game_state_counts = next_round

    return p1_wins


@dataclasses.dataclass
class Player:
    position: int
    score: int = 0


def p1(input_file: str) -> int:
    with open(input_file) as f:
        players = [Player(int(line.strip().split()[-1])) for line in f]

    die = iter(range(1, 1001))
    while all(player.score < 1000 for player in players):
        for player in players:
            player.position = ((player.position - 1 + next(die) + next(die) + next(die)) % 10) + 1
            player.score += player.position
            if player.score >= 1000:
                break

    loser_score = [player for player in players if player.score < 1000][0].score
    return loser_score * (next(die) - 1)


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1(cli_args[0]))
    print(p2(cli_args[0]))
    print(f"Elapsed: {time.perf_counter() - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
