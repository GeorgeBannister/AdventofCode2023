#!/usr/bin/env python3

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Literal
import re
from copy import deepcopy
import functools
import operator


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int


@dataclass
class Workflow:
    value: Literal["x"] | Literal["m"] | Literal["a"] | Literal["s"]
    comp: Literal["<"] | Literal[">"]
    comp_value: int | str
    true_path: str | bool

    def do_cmp(self, compare_to: Part) -> bool:
        command = f"compare_to.{self.value} {self.comp} {self.comp_value}"
        return eval(command)


test_inp = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""

nums_reg = re.compile(r"\d+")


def parse_input(inp: str) -> tuple[dict[str, list[Workflow]], list[Part]]:
    workflow_s, part_s = inp.split("\n\n")

    workflows = {}

    for line in workflow_s.splitlines():
        name, rest = line.split("{")
        rest = rest.replace("}", "")
        acc = []
        commands = rest.split(",")
        for comm in commands:
            if ":" not in comm:
                if comm == "A":
                    acc.append(True)
                    continue
                if comm == "R":
                    acc.append(False)
                    continue
                acc.append(Workflow("x", ">", "-1", comm))
                continue

            lhs, rhs = comm.split(":")
            if rhs == "A":
                rhs = True
            if rhs == "R":
                rhs = False

            val = (
                "x" if "x" in lhs else "m" if "m" in lhs else "a" if "a" in lhs else "s"
            )

            cmp = ">" if ">" in lhs else "<"
            cmp_value = int(nums_reg.findall(lhs)[0])

            wf = Workflow(val, cmp, cmp_value, rhs)

            acc.append(wf)
        workflows[name] = acc

    parts = [
        Part(*[int(x) for x in nums_reg.findall(line)]) for line in part_s.splitlines()
    ]
    return (workflows, parts)


def solve_part_1(inp: str) -> int:
    workflows, parts = parse_input(inp)
    points_acc = 0

    for part in parts:
        found = False
        curr_name = "in"
        while not found:
            wf_ended = False
            for wf in workflows[curr_name]:
                if not wf_ended:
                    if wf is True:
                        points_acc += part.x + part.m + part.a + part.s
                        found = True
                        wf_ended = True
                        break
                    if wf is False:
                        found = True
                        wf_ended = True
                        break

                    if wf.do_cmp(part):
                        if wf.true_path is True:
                            points_acc += part.x + part.m + part.a + part.s
                            found = True
                            wf_ended = True
                            break
                        if wf.true_path is False:
                            found = True
                            wf_ended = True
                            break
                        curr_name = wf.true_path
                        wf_ended = True
                        break
    return points_acc


def mutate_cons(con_map: dict, wf: Workflow, inverse=False):
    if inverse:
        if wf.comp == "<":
            # Item.bla is greater than val
            con_map[wf.value][0] = max(con_map[wf.value][0], int(wf.comp_value) )
        else:  # ">"
            # Item.bla is smaller than val
            con_map[wf.value][1] = min(con_map[wf.value][1], int(wf.comp_value) )
    else:
        if wf.comp == "<":
            # Item.bla is smaller than val
            con_map[wf.value][1] = min(con_map[wf.value][1], int(wf.comp_value) - 1)
        else:  # ">"
            # Item.bla is greater than val
            con_map[wf.value][0] = max(con_map[wf.value][0], int(wf.comp_value) + 1)
    


def get_branches(workflows: dict[str, list[Workflow]]) -> int:
    # Smallest, Biggest
    cons = {
        "x": [1, 4000],
        "m": [1, 4000],
        "a": [1, 4000],
        "s": [1, 4000],
    }
    # Curr node, dict, idx
    stack: list[tuple[str, dict, int]] = [("in", cons, 0)]
    acc = 0
    while stack:
        curr_name, d, idx = stack.pop()
        curr_wf = workflows[curr_name][idx]


        if curr_wf is False:
            continue

        if curr_wf is True:
            acc += functools.reduce(operator.mul, [x[1] - x[0] + 1 for x in d.values()])
            continue

        new_map = deepcopy(d)
        mutate_cons(new_map, curr_wf)

        if curr_wf.true_path == "A" or curr_wf.true_path is True:
            acc += functools.reduce(operator.mul, [x[1] - x[0] + 1 for x in new_map.values()])

        elif curr_wf.true_path == "R" or curr_wf.true_path is False:
            pass

        else:
            stack.append((curr_wf.true_path, new_map, 0))

        if idx < len(workflows[curr_name]) - 1:
            new_map = deepcopy(d)
            mutate_cons(new_map, curr_wf, True)
            stack.append((curr_name, new_map, idx + 1))

    return acc


def solve_part_2(inp: str) -> int:
    # range (1, 4001)
    workflows, _ = parse_input(inp)
    score = get_branches(workflows)
    return score


if __name__ == "__main__":
    assert solve_part_1(test_inp) == 19114
    inp = sys.argv[1]
    print(f"{solve_part_1(inp) = }")
    assert solve_part_2(test_inp) == 167_409_079_868_000
    print(f"{solve_part_2(inp) = }")
