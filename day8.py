#!/usr/bin/env python3

import sys
from dataclasses import dataclass
import re
from itertools import cycle
import math

test_inp = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""


test_inp_2 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""


@dataclass(frozen=True)
class Fork:
    left: str
    right: str


def parse_input(inp: str) -> tuple[str, dict[str, Fork]]:
    capital_letters_reg = re.compile(r"[A-Z0-9]+")
    lines = inp.splitlines()
    rl_str = lines[0]
    fork_map = {}
    for line in lines[2:]:
        letter_groups = capital_letters_reg.findall(line)
        fork_map[letter_groups[0]] = Fork(letter_groups[1], letter_groups[2])
    return (rl_str, fork_map)


def solve_part_1(inp: str) -> int:
    rl_str, fork_map = parse_input(inp)
    steps_taken = 0
    current = "AAA"
    for l_or_r in cycle(rl_str):
        steps_taken += 1
        if l_or_r == "L":
            current = fork_map[current].left
        else:
            current = fork_map[current].right
        if current == "ZZZ":
            return steps_taken


def solve_part_2(inp: str) -> int:
    rl_str, fork_map = parse_input(inp)
    current_nodes = [node for node in fork_map if node.endswith("A")]
    acc = []
    for node in current_nodes:
        steps_taken = 0
        for l_or_r in cycle(rl_str):
            steps_taken += 1
            if l_or_r == "L":
                node = fork_map[node].left
            else:
                node = fork_map[node].right
            if node.endswith("Z"):
                acc.append(steps_taken)
                break
    return math.lcm(*acc)

if __name__ == "__main__":
    assert solve_part_1(test_inp) == 2
    assert solve_part_2(test_inp_2) == 6
    inp = sys.argv[1]
    print(f"{solve_part_1(inp) = }")
    print(f"{solve_part_2(inp) = }")
