#!/usr/bin/env python3

import sys
from dataclasses import dataclass

test_inp = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""


@dataclass
class Matrix:
    columns: list[list[bool]]
    rows: list[list[bool]]

    def flip(self, x: int, y: int) -> None:
        self.columns[x][y] = not self.columns[x][y]
        self.rows[y][x] = not self.rows[y][x]

    def get_score(self, exclude_score=None) -> int:
        # Try to find vertical line
        for x in range(1, len(self.columns)):
            lhs = self.columns[:x]
            lhs.reverse()
            rhs = self.columns[x:]
            have_found_conflict = False
            while lhs and rhs:
                if lhs.pop(0) != rhs.pop(0):
                    have_found_conflict = True

            if not have_found_conflict and x != exclude_score:
                return x

        # Try to find horizontal line

        for y in range(1, len(self.rows)):
            top_side = self.rows[:y]
            top_side.reverse()
            bottom_side = self.rows[y:]
            have_found_conflict = False
            while top_side and bottom_side:
                if top_side.pop(0) != bottom_side.pop(0):
                    have_found_conflict = True

            if not have_found_conflict and y * 100 != exclude_score:
                return y * 100

    def get_score_2(self) -> int:
        part_1_score = self.get_score()

        for idy in range(len(self.rows)):
            for idx in range(len(self.columns)):
                self.flip(idx, idy)
                score = self.get_score(exclude_score=part_1_score)
                if score and score != part_1_score:
                    return score
                self.flip(idx, idy)


def build_matrix(s: str) -> Matrix:
    lines = [[char == "#" for char in line] for line in s.splitlines()]
    cols = [[line[x] for line in lines] for x in range(len(lines[0]))]
    return Matrix(cols, lines)


def solve_part_1(inp: str) -> int:
    sub_inputs = inp.split("\n\n")
    acc = 0
    for sub in sub_inputs:
        score = build_matrix(sub).get_score()
        acc += score
    return acc


def solve_part_2(inp: str) -> int:
    sub_inputs = inp.split("\n\n")
    acc = 0
    for sub in sub_inputs:
        score = build_matrix(sub).get_score_2()
        acc += score
    return acc


if __name__ == "__main__":
    assert solve_part_1(test_inp) == 405
    assert solve_part_2(test_inp) == 400
    inp = sys.argv[1]
    print(f"{solve_part_1(inp) = }")
    print(f"{solve_part_2(inp) = }")
