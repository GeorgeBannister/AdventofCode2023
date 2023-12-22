#!/usr/bin/env python3

from __future__ import annotations

import sys
from dataclasses import dataclass
import re

test_inp = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""


@dataclass(frozen=True)
class P3:
    x: int
    y: int
    z: int

    def __add__(self, other) -> P3:
        return P3(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )


@dataclass()
class Brick:
    points: list[P3]
    uid: int
    supporting: set[int]
    supported_by: set[int]

    def get_min_z(self: Brick) -> int:
        return min([x.z for x in self.points])


def parse_inp(inp: str) -> list[Brick]:
    nums_re = re.compile(r"\d+")
    bricks = []
    for idx, line in enumerate(inp.splitlines()):
        lhs, rhs = line.split("~")
        lhs_nums = [int(x) for x in nums_re.findall(lhs)]
        rhs_nums = [int(x) for x in nums_re.findall(rhs)]

        points = []

        for x in range(lhs_nums[0], rhs_nums[0] + 1):
            for y in range(lhs_nums[1], rhs_nums[1] + 1):
                for z in range(lhs_nums[2], rhs_nums[2] + 1):
                    points.append(P3(x, y, z))
        bricks.append(Brick(points, idx, set(), set()))

    return bricks


fall_delta = P3(0, 0, -1)


def evaluate_falling(bricks: list[Brick]) -> None:
    brick_has_moved = True

    while brick_has_moved:
        brick_has_moved = False
        for brick in bricks:
            shadow_points = [point + fall_delta for point in brick.points]
            if not any(
                [
                    point.z == 0 or point == other_point
                    for point in shadow_points
                    for brick2 in bricks
                    if brick2.uid != brick.uid
                    for other_point in brick2.points
                ]
            ):
                brick.points = shadow_points
                brick_has_moved = True


def populate_supporting(bricks: list[Brick]) -> None:
    for brick in bricks:
        shadow_points = [point + fall_delta for point in brick.points]
        for brick2 in [b for b in bricks if b.uid != brick.uid]:
            for point in brick2.points:
                if point in shadow_points:
                    brick2.supporting.add(brick.uid)


def populate_supported_by(bricks: list[Brick]) -> None:
    for brick in bricks:
        shadow_points = [point + fall_delta for point in brick.points]
        for brick2 in [b for b in bricks if b.uid != brick.uid]:
            for point in brick2.points:
                if point in shadow_points:
                    brick.supported_by.add(brick2.uid)


def solve_part_1(inp: str) -> int:
    bricks: list[Brick] = parse_inp(inp)
    bricks.sort(key=lambda x: x.get_min_z())
    evaluate_falling(bricks)
    populate_supporting(bricks)
    supported_by_multiple: set[int] = set()
    for brick in bricks:
        if len([x.uid for x in bricks if brick.uid in x.supporting]) > 1:
            supported_by_multiple.add(brick.uid)
    acc = 0
    for brick in bricks:
        if len(brick.supporting) == 0 or all(
            x in supported_by_multiple for x in brick.supporting
        ):
            acc += 1
    return acc


def solve_part_2(inp: str) -> int:
    bricks: list[Brick] = parse_inp(inp)
    bricks.sort(key=lambda x: x.get_min_z())
    evaluate_falling(bricks)
    populate_supporting(bricks)
    populate_supported_by(bricks)

    supported_by_multiple: set[int] = set()
    for brick in bricks:
        if len([x.uid for x in bricks if brick.uid in x.supporting]) > 1:
            supported_by_multiple.add(brick.uid)
    acc = 0

    def cnt_will_fall(brick: Brick) -> int:
        queue = []
        will_fall = [x for x in brick.supporting if x not in supported_by_multiple]
        gone: set[int] = set(will_fall)
        gone.add(brick.uid)
        queue.extend(will_fall)
        while queue:
            uid = queue.pop()
            queue_brick: Brick = [b for b in bricks if b.uid == uid][0]
            for supporting_uid in queue_brick.supporting:
                supporting_brick = [b for b in bricks if b.uid == supporting_uid][0]
                if all([support in gone for support in supporting_brick.supported_by]):
                    queue.append(supporting_uid)
                    gone.add(supporting_uid)
        return len(gone) - 1

    for brick in bricks:
        acc += cnt_will_fall(brick)
    return acc


if __name__ == "__main__":
    assert solve_part_1(test_inp) == 5
    inp = sys.argv[1]
    print(f"{solve_part_1(inp) = }")
    assert solve_part_2(test_inp) == 7
    print(f"{solve_part_2(inp) = }")
