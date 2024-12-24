# /usr/bin/env python3

from __future__ import annotations

import functools
from typing import Iterator

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
                path = "".join(
                    g.edges[edge[0], edge[1]]["dirs"][edge[0]] for edge in pg.edges()
                )
                # Check if the path contains a zigzag.
                # It zigzags if it contains more than two runs of characters.
                # For example: 7 -> 3 can be done with vv>> or >>vv
                # The paths v>>v and >vv> are also possible, but are inoptimal.
                # Since the paths are short, we can trade efficiency for brevity.
                # If we lstrip all the initial direction from the path, do we
                # still have more than 1 char in the path? If so, it zigzags.
                if len(set(path.lstrip(path[0]))) > 1:
                    continue
                paths.add(path)
            res[c0, c1] = paths
    return res


SHORTEST_PATHS = build_shortest_paths(
    build_graph(
        Grid([["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], ["", "0", "A"]])
    )
) | build_shortest_paths(build_graph(Grid([["", "^", "A"], ["<", "v", ">"]])))


##########################################
# Previous attempt - times out for part2 #
##########################################
"""
@functools.cache
def all_press_paths(target: str) -> set[str]:
    res = {""}
    cur = "A"
    for c in target:
        next_res = set()
        # For all current subpaths, append all next shortest paths
        for sp in SHORTEST_PATHS[cur, c]:
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
        res |= all_press_paths(target)
    else:
        for path in press_paths(target, indirection - 1):
            res |= all_press_paths(path)
    print(f"Solved for indirection {indirection}")
    return res
"""

###########################################################
# Below solution is based on                              #
# https://old.reddit.com/r/adventofcode/comments/1hjx0x4/ #
###########################################################


def subkeys(key: str) -> Iterator[str]:
    i = 0
    while i < len(key):
        j = key.index("A", i)
        yield key[i : j + 1]
        i = j + 1


def build_sequences(
    target: str,
    idx: int = 0,
    prev: str = "A",
    cur_path: str = "",
    res: set[str] | None = None,
) -> set[str]:
    if res is None:
        res = set()
    if idx == len(target):
        res.add(cur_path)
        return res
    try:
        for path in SHORTEST_PATHS[prev, target[idx]]:
            build_sequences(target, idx + 1, target[idx], cur_path + path + "A", res)
    except:
        breakpoint()
    return res


@functools.cache
def shortest_sequence(keys: str, depth: int) -> int:
    if depth == 0:
        return len(keys)
    total = 0
    for subkey in subkeys(keys):
        total += min(
            shortest_sequence(seq, depth - 1) for seq in build_sequences(subkey)
        )
    return total


class Solver(BaseSolver):
    def solve(self) -> Solution:
        part1 = 0
        part2 = 0
        for target in self.lines:
            val = int(target[:-1])
            sequences = build_sequences(target)
            part1 += val * min(shortest_sequence(seq, 2) for seq in sequences)
            part2 += val * min(shortest_sequence(seq, 25) for seq in sequences)
        yield part1
        yield part2


Solver.run()
