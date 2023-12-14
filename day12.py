#!/usr/bin/env python3

import sys
import re
from dataclasses import dataclass
from functools import cache

test_inp = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

pos_int_reg = re.compile(r"\d+")
contiguous_broken_reg = re.compile(r"#+")
mario_reg = re.compile(r"[?]")


@dataclass(frozen=True)
class Row:
    springs: str
    groups: tuple[int]


@cache
def count_options(springs: str, groups: tuple[int]) -> int:
    if not groups or len(groups) == 0:
        if "#" in springs:
            return 0
        return 1

    if not springs or springs == "":
        return 0

    if len(springs) < groups[0]:
        return 0

    next_char = springs[0]
    acc = 0

    if next_char in (".", "?"):
        acc += count_options(springs[1:], groups)

    if next_char in ("#", "?"):
        target_len = groups[0]
        can_build_span = all([c in ("#", "?") for c in springs[:target_len]])

        if can_build_span:
            if len(springs) == target_len and len(groups) == 1:
                return 1

            if len(springs) == target_len:
                return 0

            if springs[target_len] != "#":
                acc += count_options(springs[target_len + 1 :], groups[1:])
    return acc


def solve_part_1(inp: str) -> int:
    rows = []
    acc = 0
    for line in inp.splitlines():
        lhs, rhs = line.split(" ")
        ints = [int(x) for x in pos_int_reg.findall(rhs)]
        rows.append(Row(lhs, tuple(ints)))

    for row in rows:
        ans = count_options(row.springs, row.groups)
        acc += ans
    return acc


def solve_part_2(inp: str) -> int:
    rows = []
    acc = 0
    for line in inp.splitlines():
        lhs, rhs = line.split(" ")
        ints = [int(x) for x in pos_int_reg.findall(rhs)]
        new_ints = tuple([*ints, *ints, *ints, *ints, *ints])
        new_lhs = f"{lhs}?{lhs}?{lhs}?{lhs}?{lhs}"
        rows.append(Row(new_lhs, new_ints))
    for row in rows:
        acc += count_options(row.springs, row.groups)
    return acc


if __name__ == "__main__":
    assert solve_part_1(test_inp) == 21
    assert solve_part_2(test_inp) == 525152
    inp = sys.argv[1]
    print(f"{solve_part_1(inp) = }")
    print(f"{solve_part_2(inp) = }")
