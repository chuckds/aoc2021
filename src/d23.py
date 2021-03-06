#!/bin/env python3
"""
Advent Of Code 2021 Day 23
"""
from __future__ import annotations

import sys
import time
import heapq
import functools
import collections

from typing import NamedTuple, Iterable


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
        return all(char in (chr(65 + room_idx), '.') for char in self.rooms[room_idx])

    @functools.cache
    def cost_to_finish(self) -> int:
        # Cost to get amphipods from hallway to the first spot in their rooms
        cost = 0
        for hallway_idx, amphipod in filter(lambda x: x[1] != '.', enumerate(self.hallway)):
            room_idx = ord(amphipod) - 65
            cost += (10 ** room_idx) * distances[hallway_idx][room_idx]
        correct_rooms: dict[int, int] = collections.defaultdict(int)
        for room_idx, amphipods_in_room in enumerate(self.rooms):
            visitor_in_room = False
            for char_idx, amphipod in reversed(list(enumerate(amphipods_in_room))):
                if amphipod != '.':
                    desired_room_idx = ord(amphipod) - 65
                    if desired_room_idx != room_idx:
                        visitor_in_room = True
                        cost += (10 ** desired_room_idx) * (char_idx + 2 + 2 * abs(room_idx - desired_room_idx))
                    elif visitor_in_room:
                        # This amphipod is blocking someone in, so cost peeking out of room and back in
                        cost += (10 ** desired_room_idx) * (char_idx + 4)
                    else:
                        # Right room don't move
                        correct_rooms[desired_room_idx] += 1
        # We now have the cost to get every amphipod to the first spot in their
        # room (or stay in their spot). Add the cost to get the rooms filled
        for room_idx, amphipods_in_room in enumerate(self.rooms):
            slots_to_fill = len(amphipods_in_room) - correct_rooms[room_idx]
            cost += (10 ** room_idx) * ((slots_to_fill * (slots_to_fill - 1)) // 2)
        return cost

    def moves(self) -> Iterable[tuple[AmphipodState, int]]:
        for hallway_idx, amphipod in filter(lambda x: x[1] != '.', enumerate(self.hallway)):
            # These can only move into the correct room if that room has a
            # space
            room_idx = ord(amphipod) - 65
            spot_in_room = self.rooms[room_idx].rfind('.')
            if (spot_in_room != -1 and self.room_has_no_visitors(room_idx) and
                self.reachable(hallway_idx, room_idx)):
                new_state, distance = self.move(room_idx, amphipod, spot_in_room, hallway_idx, '.')
                yield (new_state, distance * (10 ** room_idx))

        # For each room see which amphipods can move out
        for room_idx, amphipods_in_room in enumerate(self.rooms):
            for char_idx, amphipod in filter(lambda x: x[1] != '.', enumerate(amphipods_in_room)):
                desired_room_idx = ord(amphipod) - 65
                if room_idx != desired_room_idx or not self.room_has_no_visitors(room_idx):
                    # There's an amphipod in this room that shouldn't be here or
                    # it should be here but its blocking one in that shouldn't so move it
                    for hallway_idx, hallway_state in enumerate(self.hallway):
                        if hallway_state == '.' and self.reachable(hallway_idx, room_idx):
                            new_state, distance = self.move(room_idx, '.', char_idx, hallway_idx, amphipod)
                            yield (new_state, distance * (10 ** desired_room_idx))
                # Only the top amphipod can move so stop as soon as anyone
                # has
                break

    def move(self, room_idx: int, room_char: str, spot_in_room: int, hallway_idx: int, hallway_char: str) -> tuple[AmphipodState, int]:
        new_hallway = self.hallway[:hallway_idx] + (hallway_char,) + self.hallway[hallway_idx + 1:]
        new_room = self.rooms[room_idx][:spot_in_room] + room_char + self.rooms[room_idx][spot_in_room + 1:]
        new_rooms = self.rooms[:room_idx] + (new_room,) + self.rooms[room_idx + 1:]
        return (AmphipodState(new_hallway, new_rooms), distances[hallway_idx][room_idx] + spot_in_room)  # type: ignore


def lowest_cost_solution(rooms: list[list[str]]) -> int:
    init_state = AmphipodState(tuple('.' * 7), tuple(''.join(members) for members in zip(*rooms)))  # type: ignore
    destination_state = AmphipodState(tuple('.' * 7), ('A' * len(rooms), 'B' * len(rooms), 'C' * len(rooms), 'D' * len(rooms)))  # type: ignore

    reachable: dict[AmphipodState, int] = {init_state: init_state.cost_to_finish()}
    reachable_pq = [(init_state.cost_to_finish(), init_state)]
    heapq.heapify(reachable_pq)
    lowest_cost_known: set[AmphipodState] = set()
    result = 0
    while reachable:
        lowest_cost_so_far, ap_state = heapq.heappop(reachable_pq)
        if ap_state in lowest_cost_known:  # Stale entry on PQ
            continue
        del reachable[ap_state]
        lowest_cost_known.add(ap_state)
        if ap_state == destination_state:
            result = lowest_cost_so_far
            break
        for new_state, additional_cost in ap_state.moves():
            if new_state not in lowest_cost_known:
                new_cost_to_state = lowest_cost_so_far + additional_cost + new_state.cost_to_finish() - ap_state.cost_to_finish()
                cost_to_state_so_far = reachable.get(new_state, None)
                if (cost_to_state_so_far is None or
                    new_cost_to_state < cost_to_state_so_far):
                    # Not worth trying to 'update' any existing entry in the PQ
                    # just have handling for stale entries on the PQ
                    heapq.heappush(reachable_pq, (new_cost_to_state, new_state))
                    reachable[new_state] = new_cost_to_state

    return result


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
