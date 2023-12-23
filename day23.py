#!/usr/bin/env python3

from __future__ import annotations

import sys
from dataclasses import dataclass
import itertools

test_inp = """\
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""


@dataclass(frozen=True, slots=True)
class Coord:
    x: int
    y: int

    def __add__(self, other) -> Coord:
        return Coord(self.x + other.x, self.y + other.y)

    def list_neighbors(self) -> list[Coord]:
        return [
            self + x
            for x in [
                Coord(0, 1),
                Coord(0, -1),
                Coord(1, 0),
                Coord(-1, 0),
            ]
        ]


def parse_input(inp: str):
    empty_squares: set[Coord] = set()
    # Maps a cliff to the only square you can move to
    cliffs: dict[Coord, Coord] = {}
    for idy, line in enumerate(inp.splitlines()):
        for idx, char in enumerate(line):
            co = Coord(idx, idy)
            match char:
                case ".":
                    empty_squares.add(co)
                case "#":
                    pass
                case ">":
                    cliffs[co] = co + Coord(1, 0)
                case "v":
                    cliffs[co] = co + Coord(0, 1)
                case "<":
                    cliffs[co] = co + Coord(-1, 0)
                case "^":
                    cliffs[co] = co + Coord(0, -1)
    return (empty_squares, cliffs)


def solve_part_1(inp: str) -> int:
    empty_squares, cliffs = parse_input(inp)
    min_y = min([co.y for co in empty_squares])
    max_y = max([co.y for co in empty_squares])

    start: Coord = [co for co in empty_squares if co.y == min_y][0]
    end: Coord = [co for co in empty_squares if co.y == max_y][0]

    finishing_scores: list[int] = []
    queue: list[list[Coord]] = [[start]]

    while queue:
        curr_line: list[Coord] = queue.pop()
        curr_pos: Coord = curr_line[-1]

        if curr_pos == end:
            finishing_scores.append(len(curr_line) - 1)
            continue

        next_moves = None

        if curr_pos in cliffs:
            if cliffs[curr_pos] not in curr_line:
                next_moves = [cliffs[curr_pos]]
        else:
            next_moves = [
                x
                for x in curr_pos.list_neighbors()
                if (x in empty_squares or x in cliffs) and x not in curr_line
            ]

        if next_moves:
            for next_move in next_moves:
                queue.append([*curr_line, next_move])
    return max(finishing_scores)


def parse_input_2(inp: str):
    empty_squares: set[Coord] = set()
    graph: dict[tuple[Coord, Coord], int] = {}
    for idy, line in enumerate(inp.splitlines()):
        for idx, char in enumerate(line):
            co = Coord(idx, idy)
            match char:
                case "#":
                    pass
                case _:
                    empty_squares.add(co)

    min_y = min([co.y for co in empty_squares])
    max_y = max([co.y for co in empty_squares])

    start: Coord = [co for co in empty_squares if co.y == min_y][0]
    end: Coord = [co for co in empty_squares if co.y == max_y][0]

    directions = [
        Coord(-1, 0),
        Coord(1, 0),
        Coord(0, -1),
        Coord(0, 1),
    ]

    turns: set[Coord] = set()
    for co in empty_squares:
        up = co + Coord(0, -1)
        down = co + Coord(0, 1)
        left = co + Coord(-1, 0)
        right = co + Coord(1, 0)
        if (
            (up in empty_squares and right in empty_squares)
            or (right in empty_squares and down in empty_squares)
            or (down in empty_squares and left in empty_squares)
            or (left in empty_squares and up in empty_squares)
            or co == start
            or co == end
        ):
            turns.add(co)

    for span_start in turns:
        for d in directions:
            dist = 0
            shadow = span_start
            found_end = False

            while not found_end:
                shadow = shadow + d
                if shadow not in empty_squares:
                    break
                dist += 1
                if shadow in turns:
                    found_end = True
                    graph[(span_start, shadow)] = dist
                    graph[(shadow, span_start)] = dist

    junctions = set()
    for co in empty_squares:
        if len([c for c in co.list_neighbors() if c in empty_squares]) > 2:
            junctions.add(co)
    junctions.add(start)
    junctions.add(end)

    junction_graph = {}

    for jun in junctions:
        queue = [[jun]]
        while queue:
            n = queue.pop()
            last_node = n[-1]
            mov_opts = [x[1] for x in graph if x[0] == last_node and x[1] not in n]
            for opt in mov_opts:
                new_chain = [*n, opt]
                if opt in junctions:
                    junction_graph[(jun, opt)] = sum(
                        [graph[pair] for pair in itertools.pairwise(new_chain)]
                    )
                else:
                    queue.append(new_chain)

    return (junction_graph, start, end)


def solve_part_2(inp: str) -> int:
    graph, start, end = parse_input_2(inp)

    finishing_scores: set[int] = set()
    queue: list[list[Coord]] = [[start]]

    graph_keys: set = set(graph.keys())
    graph_map: dict[Coord, list[Coord]] = {}
    for pair in graph_keys:
        if pair[0] not in graph_map:
            graph_map[pair[0]] = [x[1] for x in graph_keys if x[0] == pair[0]]

    while queue:
        curr_line: list[Coord] = queue.pop()
        curr_pos: Coord = curr_line[-1]

        if curr_pos == end:
            finishing_scores.add(sum([graph[x] for x in itertools.pairwise(curr_line)]))
            continue

        next_moves = [x for x in graph_map[curr_pos] if x not in curr_line]

        if next_moves:
            for next_move in next_moves:
                queue.append([*curr_line, next_move])
    return max(finishing_scores)


if __name__ == "__main__":
    assert solve_part_1(test_inp) == 94
    inp = sys.argv[1]
    print(f"{solve_part_1(inp) = }")
    assert solve_part_2(test_inp) == 154
    print(f"{solve_part_2(inp) = }")
