#!/usr/bin/env python3

import sys
import itertools
import math

test_inp = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""

test_inp_2 = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""


global_state = {True: 0, False: 0}


class FlipFlop:
    def __init__(self, outputs: list, name: str):
        self.is_on = False
        self.outputs = outputs
        self.name = name

    def receive(self, is_high: bool, caller_name: str, queue: list, gates):
        if not is_high:
            self.is_on = not self.is_on
            for node in self.outputs:
                if node in gates:
                    queue.append((node, self.is_on, self.name))
                global_state[self.is_on] += 1

    def __repr__(self) -> str:
        return f"{self.is_on = } | {self.outputs = } | {self.name = }"


class Conjunction:
    def __init__(self, outputs: list, name: str):
        self.outputs = outputs
        self.inputs = {}
        self.name = name

    def receive(self, is_high: bool, caller_name: str, queue: list, gates):
        self.inputs[caller_name] = is_high
        if all(self.inputs.values()):
            for node in self.outputs:
                if node in gates:
                    queue.append((node, False, self.name))
                global_state[False] += 1
        else:
            for node in self.outputs:
                if node in gates:
                    queue.append((node, True, self.name))
                global_state[True] += 1

    def __repr__(self) -> str:
        return f"{self.outputs = } | {self.inputs = } | {self.name = }"


class Other:
    def __init__(self, outputs: list, name: str):
        self.outputs = outputs
        self.name = name

    def receive(self, is_high: bool, caller_name: str, queue: list, gates):
        for node in self.outputs:
            if node in gates:
                queue.append((node, is_high, self.name))
            global_state[is_high] += 1

    def __repr__(self) -> str:
        return f"{self.outputs = } | {self.name = }"


def parse_input(inp: str):
    gates = {}

    for line in inp.splitlines():
        # ("&inv) , (a,b,c)"
        lhs, rhs = line.split(" -> ")
        outputs = rhs.replace(" ", "").split(",")
        if lhs == "broadcaster":
            gates["broadcaster"] = Other(outputs, lhs[1:])
        elif lhs[0] == "%":
            gates[lhs[1:]] = FlipFlop(outputs, lhs[1:])
        elif lhs[0] == "&":
            gates[lhs[1:]] = Conjunction(outputs, lhs[1:])

    for key in gates:
        if isinstance(gates[key], Conjunction):
            for key2 in gates:
                if key in gates[key2].outputs:
                    gates[key].inputs[key2] = False
    return gates


def solve_part_1(inp: str) -> int:
    global_state[True] = 0
    global_state[False] = 0
    queue = []
    gates = parse_input(inp)
    turn = 0
    while turn < 1000:
        global_state[False] += 1
        queue = [("broadcaster", False, None)]
        while queue:
            entry, is_high, caller_name = queue.pop(0)
            gates[entry].receive(is_high, caller_name, queue, gates)

        turn += 1
    return global_state[False] * global_state[True]


def solve_part_2(inp: str) -> int:
    global_state[True] = 0
    global_state[False] = 0
    queue = []
    gates = parse_input(inp)
    gates["rx"] = Other([], "rx")

    sgs = []
    lms = []
    dhs = []
    dbs = []

    turn = 1
    while turn < 100_000:
        queue = [("broadcaster", False, None)]
        while queue:
            entry, is_high, caller_name = queue.pop(0)

            if caller_name == "sg" and is_high:
                sgs.append(turn)
            if caller_name == "lm" and is_high:
                lms.append(turn)
            if caller_name == "dh" and is_high:
                dhs.append(turn)
            if caller_name == "db" and is_high:
                dbs.append(turn)
            gates[entry].receive(is_high, caller_name, queue, gates)
        turn += 1

    return math.lcm(
        [a[1] - a[0] for a in itertools.pairwise(sgs)][1],
        [a[1] - a[0] for a in itertools.pairwise(lms)][1],
        [a[1] - a[0] for a in itertools.pairwise(dhs)][1],
        [a[1] - a[0] for a in itertools.pairwise(dbs)][1],
    )


if __name__ == "__main__":
    assert solve_part_1(test_inp) == 32_000_000
    assert solve_part_1(test_inp_2) == 11_687_500
    inp: str = sys.argv[1]
    print(f"{solve_part_1(inp) = }")
    print(f"{solve_part_2(inp) = }")
