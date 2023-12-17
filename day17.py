#!/usr/bin/env python3

from __future__ import annotations

import sys
from collections import deque

test_inp = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""

test_inp_2 = """111111111111
999999999991
999999999991
999999999991
999999999991"""

up = 0
down = 1
left = 2
right = 3


up_delta = (0, -1)
down_delta = (0, 1)
left_delta = (-1, 0)
right_delta = (1, 0)


enum_can_move = {
    up: (right, left),
    down: (right, left),
    left: (down, up),
    right: (down, up),
}

get_move_delta = {
    up: up_delta,
    down: down_delta,
    left: left_delta,
    right: right_delta,
}


def parse_input(inp: str) -> dict[tuple, int]:
    acc = {}
    for idy, line in enumerate(inp.splitlines()):
        for idx, char in enumerate(line):
            acc[(idx, idy)] = int(char)
    return acc


def get_score(
    grid: dict[tuple, int],
    target: tuple,
    acc_map: dict[tuple, int],
) -> None:
    start = (0, 0)
    # Pos, direction, steps in direction, acc cost
    queue = deque([(start, right, 0, 0)])

    while queue:
        pos, direction, steps_in_dir, acc_cost = queue.pop()
        if pos == target:
            continue
        for dir in enum_can_move[direction]:
            delta = get_move_delta[dir]
            shadow = (pos[0] + delta[0], pos[1] + delta[1])
            if shadow in grid:
                new_cost = acc_cost + grid[shadow]
                tup = (shadow, dir, 1)
                if new_cost < acc_map[tup]:
                    acc_map[tup] = new_cost
                    if dir in (right, down):
                        queue.append((shadow, dir, 1, new_cost))
                    else:
                        queue.appendleft((shadow, dir, 1, new_cost))

        if steps_in_dir < 3:
            delta = get_move_delta[direction]
            shadow = (pos[0] + delta[0], pos[1] + delta[1])
            if shadow in grid:
                new_cost = acc_cost + grid[shadow]
                tup = (shadow, direction, steps_in_dir + 1)
                if new_cost < acc_map[tup]:
                    acc_map[tup] = new_cost
                    if direction in (right, down):
                        queue.append((shadow, direction, steps_in_dir + 1, new_cost))
                    else:
                        queue.appendleft(
                            (shadow, direction, steps_in_dir + 1, new_cost)
                        )


def get_score_2(
    grid: dict[tuple, int],
    target: tuple,
    acc_map: dict[tuple, int],
) -> None:
    start = (0, 0)
    # Pos, direction, steps in direction, acc cost
    queue = deque([(start, right, 0, 0), (start, down, 0, 0)])

    while queue:
        pos, direction, steps_in_dir, acc_cost = queue.pop()
        if pos == target:
            continue
        if steps_in_dir > 3:
            for dir in enum_can_move[direction]:
                delta = get_move_delta[dir]
                shadow = (pos[0] + delta[0], pos[1] + delta[1])
                if shadow in grid:
                    new_cost = acc_cost + grid[shadow]
                    tup = (shadow, dir, 1)
                    if new_cost < acc_map[tup]:
                        acc_map[tup] = new_cost
                        if dir in (right, down):
                            queue.append((shadow, dir, 1, new_cost))
                        else:
                            queue.appendleft((shadow, dir, 1, new_cost))

        if steps_in_dir < 10:
            delta = get_move_delta[direction]
            shadow = (pos[0] + delta[0], pos[1] + delta[1])
            if shadow in grid:
                new_cost = acc_cost + grid[shadow]
                tup = (shadow, direction, steps_in_dir + 1)
                if new_cost < acc_map[tup]:
                    acc_map[tup] = new_cost
                    if direction in (right, down):
                        queue.append((shadow, direction, steps_in_dir + 1, new_cost))
                    else:
                        queue.appendleft(
                            (shadow, direction, steps_in_dir + 1, new_cost)
                        )


def solve_part_1(inp: str) -> int:
    grid = parse_input(inp)

    max_x = max([co[0] for co in grid])
    max_y = max([co[1] for co in grid])
    target = (max_x, max_y)
    acc_map = {((0, 0), right, 0): -1}
    for coord in grid:
        for dir in [up, down, left, right]:
            for x in range(1, 4):
                acc_map[(coord, dir, x)] = 999999999

    get_score(grid, target, acc_map)
    winner = min(
        [
            acc_map[(target, dir, x)]
            for dir in [up, down, left, right]
            for x in range(1, 4)
        ]
    )
    return winner


def solve_part_2(inp: str) -> int:
    grid = parse_input(inp)

    max_x = max([co[0] for co in grid])
    max_y = max([co[1] for co in grid])
    target = (max_x, max_y)
    acc_map = {((0, 0), right, 0): 9999999999, ((0, 0), down, 0): 99999999}
    for coord in grid:
        for dir in [up, down, left, right]:
            for x in range(1, 11):
                acc_map[(coord, dir, x)] = 999999999

    get_score_2(grid, target, acc_map)
    winner = min(
        [
            acc_map[(target, dir, x)]
            for dir in [up, down, left, right]
            for x in range(4, 11)
        ]
    )
    return winner


if __name__ == "__main__":
    assert solve_part_1(test_inp) == 102
    inp = sys.argv[1]
    print(f"{solve_part_1(inp) = }")
    assert solve_part_2(test_inp) == 94
    assert solve_part_2(test_inp_2) == 71
    print(f"{solve_part_2(inp) = }")
