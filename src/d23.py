#!/bin/env python3
"""
Advent Of Code 2021 Day 23
"""
from __future__ import annotations

import sys
import time

from typing import NamedTuple, Iterable, Optional


room_map = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
}


room_to_amphi = {v: k for k, v in room_map.items()}


distances = [  # hallway then room
    [3, 5, 7, 9],
    [2, 4, 6, 8],
    [2, 2, 4, 6],
    [4, 2, 2, 4],
    [6, 4, 2, 2],
    [8, 6, 4, 2],
    [9, 7, 5, 3],
]


class AmphipodState(NamedTuple):
    hallway: tuple[str, str, str, str, str, str, str]
    rooms: tuple[str, str, str, str]

    def reachable(self, hallway_posn: int, room: int) -> bool:
        if hallway_posn < room + 2:
            # Moving to the right to get there (hallway -> room)
            return all(self.hallway[idx] == '.' for idx in range(hallway_posn + 1, room + 2))
        else:
            # Moving to the left to get there (hallway -> room)
            return all(self.hallway[idx] == '.' for idx in range(room + 2, hallway_posn))

    def room_has_no_visitors(self, room_idx: int) -> bool:
        return all(char in (room_to_amphi[room_idx], '.') for char in self.rooms[room_idx])

    def moves(self) -> Iterable[tuple[AmphipodState, int]]:
        for hallway_idx, amphipod in enumerate(self.hallway):
            if amphipod != '.':
                # These can only move into the correct room if that room has a
                # space
                room_idx = room_map[amphipod]
                spot_in_room = self.rooms[room_idx].rfind('.')
                if (spot_in_room != -1 and self.room_has_no_visitors(room_idx) and
                    self.reachable(hallway_idx, room_idx)):
                    new_state, distance = self.move(room_idx, amphipod, spot_in_room, hallway_idx, '.')
                    yield (new_state, distance * (10 ** room_idx))

        # For each room see which amphipods can move out
        for room_idx, amphipods_in_room in enumerate(self.rooms):
            for char_idx, amphipod in enumerate(amphipods_in_room):
                if amphipod != '.':
                    desired_room_idx = room_map[amphipod]
                    if room_idx != desired_room_idx or not self.room_has_no_visitors(room_idx):
                        # There's an amphipod in this room that shouldn't be here or
                        # it should be here but its blocking one in that shouldn't so move it
                        for hallway_idx, hallway_state in enumerate(self.hallway):
                            if hallway_state == '.' and self.reachable(hallway_idx, room_idx):
                                new_state, distance = self.move(room_idx, '.', char_idx, hallway_idx, amphipod)
                                yield (new_state, distance * (10 ** room_map[amphipod]))
                    # Only the top amphipod can move so stop as soon as anyone
                    # has
                    break

    def move(self, room_idx: int, room_char: str, spot_in_room: int, hallway_idx: int, hallway_char: str) -> tuple[AmphipodState, int]:
        new_hallway = self.hallway[:hallway_idx] + (hallway_char,) + self.hallway[hallway_idx + 1:]
        new_room = self.rooms[room_idx][:spot_in_room] + room_char + self.rooms[room_idx][spot_in_room + 1:]
        new_rooms = self.rooms[:room_idx] + (new_room,) + self.rooms[room_idx + 1:]
        return (AmphipodState(new_hallway, new_rooms), distances[hallway_idx][room_idx] + spot_in_room)  # type: ignore

    def __str__(self) -> str:
        res = ("#" * 13 + f"\n#{self.hallway[0]}{self.hallway[1]}.{self.hallway[2]}.{self.hallway[3]}.{self.hallway[4]}.{self.hallway[5]}{self.hallway[6]}#\n" +
               f"###{self.rooms[0][0]}#{self.rooms[1][0]}#{self.rooms[2][0]}#{self.rooms[3][0]}###\n")
        for room_idx in range(1, len(self.rooms[0])):
            res += f"  #{self.rooms[0][room_idx]}#{self.rooms[1][room_idx]}#{self.rooms[2][room_idx]}#{self.rooms[3][room_idx]}#\n"
        res += f"  {'#' * 9}  "
        return res


def lowest_cost_solution(rooms: list[list[str]]) -> int:
    init_state = AmphipodState(tuple('.' * 7), tuple(''.join(members) for members in zip(*rooms)))  # type: ignore
    destination_state = AmphipodState(tuple('.' * 7), ('A' * len(rooms), 'B' * len(rooms), 'C' * len(rooms), 'D' * len(rooms)))  # type: ignore
    print(f"{init_state}\n{destination_state}")

    reachable: dict[AmphipodState, tuple[int, Optional[AmphipodState]]] = {init_state: (0, None)}
    lowest_cost_known: dict[AmphipodState, tuple[int, Optional[AmphipodState]]] = {}
    while reachable:
        ap_state, (lowest_cost_so_far, previous_state) = min(reachable.items(), key=lambda x: x[1][0])
        del reachable[ap_state]
        lowest_cost_known[ap_state] = (lowest_cost_so_far, previous_state)
        if ap_state == destination_state:
            break
        for new_state, additional_cost in ap_state.moves():
            if new_state not in lowest_cost_known:
                new_cost_to_state = lowest_cost_so_far + additional_cost
                cost_to_state_so_far, _ = reachable.get(new_state, (None, None))
                if (cost_to_state_so_far is None or
                    new_cost_to_state < cost_to_state_so_far):
                    reachable[new_state] = (new_cost_to_state, ap_state)

    path = [(destination_state, 0)]
    next_state = destination_state
    while next_state:
        lowest_cost_so_far, next_state = lowest_cost_known[next_state]  # type: ignore
        path.append((next_state, lowest_cost_so_far))
    for state, cost in reversed(path):
        print(f"{state}\n{cost}")

    return lowest_cost_known[destination_state][0]


def p1p2(input_file: str) -> tuple[int, int]:
    with open(input_file) as f:
        rooms = []
        for line in f:
            amphipods = [char for char in line.strip() if char not in ('.', '#')]
            if amphipods:
                rooms.append(amphipods)
    p1 = lowest_cost_solution(rooms)
    new_rooms = []
    for line in "#D#C#B#A#\n#D#B#A#C#".splitlines():
        new_rooms.append([char for char in line.strip() if char not in ('.', '#')])
    p2 = lowest_cost_solution(rooms[:-1] + new_rooms + [rooms[-1]])
    return (p1, p2)


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1p2(cli_args[0]))
    print(f"Elapsed: {time.perf_counter() - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
