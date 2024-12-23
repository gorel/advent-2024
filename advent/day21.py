# /usr/bin/env python3

from __future__ import annotations

import functools
import re

import networkx as nx

from advent.base import BaseSolver, Solution
from advent.graph import Direction, Grid


ShortestPaths = dict[tuple[str, str], set[str]]


def dirstring(d: Direction) -> str:
    match d:
        case Direction.UP:
            return "^"
        case Direction.DOWN:
            return "v"
        case Direction.LEFT:
            return "<"
        case Direction.RIGHT:
            return ">"
        case _:
            raise ValueError(f"Invalid direction {d}")


def build_graph(g: Grid[str]) -> nx.Graph:
    res = nx.Graph()
    for p, c in g:
        for adj, dir in p.adjacent_with_dirs():
            if not g.inbounds(adj) or c == "" or g.at(adj) == "":
                continue
            adjc, adjdir = g.at(adj), dir.opposite
            res.add_edge(c, adjc, dirs={c: dirstring(dir), adjc: dirstring(adjdir)})
    return res


def build_shortest_paths(g: nx.Graph) -> ShortestPaths:
    res = {}
    for c0 in g.nodes:
        res[c0, c0] = {""}
        for c1 in g.nodes:
            if c0 == c1:
                continue
            paths = set()
            for sp in nx.all_shortest_paths(g, c0, c1):
                pg = nx.path_graph(sp)
                traversal = "".join(
                    g.edges[edge[0], edge[1]]["dirs"][edge[0]] for edge in pg.edges()
                )
                # Check if the path contains a zigzag
                if re.match(r"([<>^v])(?!\1)[<>^v]\1", traversal):
                    continue
                paths.add(traversal)
            res[c0, c1] = paths
    return res


@functools.cache
def all_press_paths(target: str, indirection: int) -> set[str]:
    paths = KEYPAD if indirection == 0 else DIRPAD
    res = {""}
    cur = "A"
    for c in target:
        next_res = set()
        # For all current subpaths, append all next shortest paths
        for sp in paths[cur, c]:
            for r in res:
                # Remember we have to hit A to accept the input
                next_res.add(r + sp + "A")
        res = next_res
        cur = c
    return res


@functools.cache
def press_paths(target: str, indirection: int) -> set[str]:
    res = set()
    if indirection == 0:
        res |= all_press_paths(target, 0)
    else:
        for path in press_paths(target, indirection - 1):
            res |= all_press_paths(path, indirection)
    print(f"Solved for indirection {indirection}")
    return res


KEYPAD = build_shortest_paths(
    build_graph(
        Grid([["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], ["", "0", "A"]])
    )
)
DIRPAD = build_shortest_paths(build_graph(Grid([["", "^", "A"], ["<", "v", ">"]])))


class Solver(BaseSolver):
    def solve(self) -> Solution:
        part1 = 0
        part2 = 0
        for line in self.lines:
            part1 += int(line[:-1]) * len(min(press_paths(line, 2), key=len))
            part2 += int(line[:-1]) * len(min(press_paths(line, 25), key=len))

        yield part1
        yield part2


Solver.run()
