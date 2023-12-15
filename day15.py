#!/usr/bin/env python3

import sys
from dataclasses import dataclass

test_inp = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""


@dataclass()
class Lens:
    label: str
    focal_length: int


def my_hash(inp: str) -> int:
    acc = 0
    for c in inp:
        acc += ord(c)
        acc *= 17
        acc %= 256
    return acc


def solve_part_1(inp: str) -> int:
    in_no_nl = inp.replace("\n", "")
    acc = 0
    for term in in_no_nl.split(","):
        acc += my_hash(term)
    return acc


def drop_if_exists(map: dict, hash_num: int, label: str):
    if hash_num not in map:
        return

    for idx, val in enumerate(map[hash_num]):
        if val.label == label:
            map[hash_num].pop(idx)


def update_or_push(map: dict, hash_num: int, label: str, new_fl: int):
    if hash_num not in map:
        map[hash_num] = []

    my_len = len(map[hash_num])
    for idx in range(my_len):
        if map[hash_num][idx].label == label:
            map[hash_num][idx].focal_length = new_fl
            return

    map[hash_num].append(Lens(label, new_fl))
    return


def solve_part_2(inp: str) -> int:
    in_no_nl = inp.replace("\n", "")

    boxes: dict[int, list[Lens]] = {}

    for term in in_no_nl.split(","):
        if "-" in term:
            label, _ = term.split("-")
            h = my_hash(label)
            drop_if_exists(boxes, h, label)
        else:  # "="
            label, rhs = term.split("=")
            h = my_hash(label)
            update_or_push(
                boxes,
                h,
                label,
                int(rhs),
            )
    acc = 0

    for key in boxes:
        for idx, val in enumerate(boxes[key]):
            acc += (key + 1) * (idx + 1) * val.focal_length

    return acc


if __name__ == "__main__":
    assert my_hash("HASH") == 52
    assert solve_part_1(test_inp) == 1320
    assert solve_part_2(test_inp) == 145
    inp = sys.argv[1]
    print(f"{solve_part_1(inp) = }")
    print(f"{solve_part_2(inp) = }")
