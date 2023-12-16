#!/usr/bin/env python3

from __future__ import annotations

from enum import Enum
import sys
from dataclasses import dataclass

test_inp = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""


@dataclass(frozen=True)
class Coord:
    x: int
    y: int

    def __add__(self, other) -> Coord:
        return Coord(self.x + other.x, self.y + other.y)


class Direction(Enum):
    up = 0
    down = 1
    left = 2
    right = 3


up_delta = Coord(0, -1)
down_delta = Coord(0, 1)
left_delta = Coord(-1, 0)
right_delta = Coord(1, 0)


def light_move_rec(
    touched: set(Coord),
    grid: dict[Coord, str],
    curr_pos: Coord,
    direction: Direction.up | Direction.down | Direction.left | Direction.right,
    memo: set,
) -> None:
    touched.add(curr_pos)
    if (curr_pos, direction) in memo:
        return
    memo.add((curr_pos, direction))

    shadow = None
    match direction:
        case Direction.up:
            shadow = curr_pos + up_delta
        case Direction.down:
            shadow = curr_pos + down_delta
        case Direction.left:
            shadow = curr_pos + left_delta
        case Direction.right:
            shadow = curr_pos + right_delta
    if shadow not in grid:
        return
    curr_pos = shadow
    match grid[curr_pos]:
        case ".":
            return light_move_rec(touched, grid, curr_pos, direction, memo)
        case "/":
            match direction:
                case Direction.up:
                    return light_move_rec(
                        touched, grid, curr_pos, Direction.right, memo
                    )
                case Direction.down:
                    return light_move_rec(touched, grid, curr_pos, Direction.left, memo)
                case Direction.left:
                    return light_move_rec(touched, grid, curr_pos, Direction.down, memo)
                case Direction.right:
                    return light_move_rec(touched, grid, curr_pos, Direction.up, memo)
        case "\\":
            match direction:
                case Direction.up:
                    return light_move_rec(touched, grid, curr_pos, Direction.left, memo)
                case Direction.down:
                    return light_move_rec(
                        touched, grid, curr_pos, Direction.right, memo
                    )
                case Direction.left:
                    return light_move_rec(touched, grid, curr_pos, Direction.up, memo)
                case Direction.right:
                    return light_move_rec(touched, grid, curr_pos, Direction.down, memo)
        case "-":
            match direction:
                case Direction.up:
                    light_move_rec(touched, grid, curr_pos, Direction.left, memo)
                    return light_move_rec(
                        touched, grid, curr_pos, Direction.right, memo
                    )
                case Direction.down:
                    light_move_rec(touched, grid, curr_pos, Direction.left, memo)
                    return light_move_rec(
                        touched, grid, curr_pos, Direction.right, memo
                    )
                case Direction.left:
                    return light_move_rec(touched, grid, curr_pos, direction, memo)
                case Direction.right:
                    return light_move_rec(touched, grid, curr_pos, direction, memo)
        case "|":
            match direction:
                case Direction.up:
                    return light_move_rec(touched, grid, curr_pos, direction, memo)
                case Direction.down:
                    return light_move_rec(touched, grid, curr_pos, direction, memo)
                case Direction.left:
                    light_move_rec(touched, grid, curr_pos, Direction.up, memo)
                    return light_move_rec(touched, grid, curr_pos, Direction.down, memo)
                case Direction.right:
                    light_move_rec(touched, grid, curr_pos, Direction.up, memo)
                    return light_move_rec(touched, grid, curr_pos, Direction.down, memo)


def parse_inp(inp: str) -> dict[Coord, str]:
    grid = {}
    for idy, line in enumerate(inp.splitlines()):
        for idx, char in enumerate(line):
            grid[Coord(idx, idy)] = char
    return grid


def solve_part_1(inp: str) -> int:
    grid = parse_inp(inp)
    touched = set()
    curr_pos = Coord(-1, 0)
    light_move_rec(touched, grid, curr_pos, Direction.right, set())
    return len(touched) - 1


def solve_part_2(inp: str) -> int:
    grid = parse_inp(inp)
    acc = []
    min_x = 0
    min_y = 0
    max_x = max([co.x for co in grid])
    max_y = max([co.x for co in grid])
    for co in grid:
        if co.x == min_x:
            touched = set()
            light_move_rec(touched, grid, co + left_delta, Direction.right, set())
            acc.append(len(touched) - 1)
        if co.x == max_x:
            touched = set()
            light_move_rec(touched, grid, co + right_delta, Direction.left, set())
            acc.append(len(touched) - 1)
        if co.y == min_y:
            touched = set()
            light_move_rec(touched, grid, co + up_delta, Direction.down, set())
            acc.append(len(touched) - 1)
        if co.y == max_y:
            touched = set()
            light_move_rec(touched, grid, co + down_delta, Direction.up, set())
            acc.append(len(touched) - 1)
    return max(acc)


if __name__ == "__main__":
    sys.setrecursionlimit(1_000_000)
    assert solve_part_1(test_inp) == 46
    with open("day16.inp", "r") as fp:
        inp = fp.read()
        print(f"{solve_part_1(inp) = }")
        assert solve_part_2(test_inp) == 51
        print(f"{solve_part_2(inp) = }")
