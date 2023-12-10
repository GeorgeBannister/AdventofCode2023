#!/usr/bin/env python3

from __future__ import annotations

import sys
from dataclasses import dataclass
from copy import deepcopy
from pprint import pprint

test_inp = """-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""

test_inp_2 = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""

test_inp_3 = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""

test_inp_4 = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""


@dataclass(frozen=True)
class Coord:
    x: int
    y: int

    def __add__(self: Coord, other: Coord) -> Coord:
        return Coord(self.x + other.x, self.y + other.y)

    def enumerate_move_options(
        self: Coord, grid: dict[Coord, Pipe], explored: set[Coord]
    ) -> list[Coord]:
        acc = []
        # Left
        left_move = self + Coord(-1, 0)
        if (
            left_move in grid
            and left_move not in explored
            and grid[self].left
            and grid[left_move].right
        ):
            acc.append(left_move)
        # Right
        right_move = self + Coord(1, 0)
        if (
            right_move in grid
            and right_move not in explored
            and grid[self].right
            and grid[right_move].left
        ):
            acc.append(right_move)
        # Up
        up_move = self + Coord(0, -1)
        if (
            up_move in grid
            and up_move not in explored
            and grid[self].up
            and grid[up_move].down
        ):
            acc.append(up_move)
        # Down
        down_move = self + Coord(0, 1)
        if (
            down_move in grid
            and down_move not in explored
            and grid[self].down
            and grid[down_move].up
        ):
            acc.append(down_move)
        return acc

    def is_adjacent_to(self: Coord, other: Coord, grid: dict[Coord, Pipe]) -> bool:
        return other in self.enumerate_move_options(grid, set())


class Pipe:
    def __init__(self: Pipe, letter: str):
        self.up = False
        self.right = False
        self.down = False
        self.left = False
        self.is_start = False
        self.letter = letter
        match letter:
            case "|":
                self.up = True
                self.down = True
            case "-":
                self.right = True
                self.left = True
            case "L":
                self.up = True
                self.right = True
            case "J":
                self.up = True
                self.left = True
            case "7":
                self.left = True
                self.down = True
            case "F":
                self.down = True
                self.right = True
            case ".":
                pass
            case "S":
                self.is_start = True
                self.up = True
                self.down = True
                self.left = True
                self.right = True


def pretty_print_grid(inp: str, highlights=None, highlights_2=None):
    new_inp = (
        inp.replace("|", "┃")
        .replace("-", "━")
        .replace("F", "┏")
        .replace("7", "┓")
        .replace("L", "┗")
        .replace("J", "┛")
    )
    for y, line in enumerate(new_inp.splitlines()):
        line_acc = ""
        for x, char in enumerate(line):
            coord = Coord(x, y)
            if coord in highlights:
                line_acc += "\033[0;31m"
            if coord in highlights_2:
                line_acc += "\033[0;32m"
            line_acc += char
            if coord in highlights or coord in highlights_2:
                line_acc += "\033[0m"
        line_acc += f" {y}"
        print(line_acc)


def parse_input(inp: str) -> dict[Coord, Pipe]:
    acc = {}
    for y, line in enumerate(inp.splitlines()):
        for x, char in enumerate(line):
            acc[Coord(x, y)] = Pipe(char)
    return acc


def get_loop_path_rec(
    curr_path: list[Coord], target: Coord, grid: dict[Coord, Pipe]
) -> list[Coord] | None:
    if len(curr_path) > 3 and curr_path[-1].is_adjacent_to(target, grid):
        return curr_path
    options = curr_path[-1].enumerate_move_options(grid, set(curr_path))
    if len(options) == 0:
        return None

    for opt in options:
        path = get_loop_path_rec([*curr_path, opt], target, grid)
        if path is not None:
            return path
    return None


def get_loop_path(grid: dict[Coord, Pipe]) -> list[Coord]:
    start_coord = None
    for node in grid:
        if grid[node].is_start:
            start_coord = node

    path = get_loop_path_rec([start_coord], start_coord, grid)
    return path


def solve_part_1(inp: str) -> int:
    grid: dict[Coord, Pipe] = parse_input(inp)
    path = get_loop_path(grid)
    return len(path) // 2


def solve_part_2(inp: str) -> int:
    grid: dict[Coord, Pipe] = parse_input(inp)
    loop_coords = set(get_loop_path(grid))
    move_left = Coord(-1, 0)
    trapped_cnt = 0
    trapped_set = set()
    for possibly_trapped_cell in grid:
        if possibly_trapped_cell in loop_coords:
            continue
        pos: Coord = possibly_trapped_cell
        am_trapped = False
        last_flipping_cell = None
        while pos.x >= 1:
            pos = pos + move_left
            if pos in loop_coords:
                letter = grid[pos].letter
                if letter == "|":
                    am_trapped = not am_trapped
                elif letter == "L":
                    if last_flipping_cell == "7":
                        am_trapped = not am_trapped
                    last_flipping_cell = "L"
                elif letter == "7":
                    last_flipping_cell = "7"
                elif letter == "F":
                    if last_flipping_cell == "J":
                        am_trapped = not am_trapped
                    last_flipping_cell = "F"
                elif letter == "J":
                    last_flipping_cell = "J"
            else:
                last_flipping_cell = None

        if am_trapped:
            trapped_cnt += 1
            trapped_set.add(possibly_trapped_cell)
    pretty_print_grid(inp, loop_coords, trapped_set)
    print(f"{trapped_cnt = }")
    return trapped_cnt


if __name__ == "__main__":
    sys.setrecursionlimit(1000000)
    assert solve_part_1(test_inp) == 4
    assert solve_part_1(test_inp_2) == 8
    assert solve_part_2(test_inp_3) == 8
    assert solve_part_2(test_inp_4) == 10
    inp = sys.argv[1]
    print(f"{solve_part_1(inp) = }")
    print(f"{solve_part_2(inp) = }")
