# /usr/bin/env python3

from __future__ import annotations

from advent.base import BaseSolver, Solution
from advent.graph import Grid, Point


def score(g: Grid[int], cur: tuple[Point, int]) -> tuple[set[Point], int]:
    p, c = cur
    if c == 9:
        return {p}, 1

    res1 = set()
    res2 = 0
    for neighbor in p.adjacent():
        if g.inbounds(neighbor) and g.at(neighbor) == c + 1:
            s1, s2 = score(g, (neighbor, c + 1))
            res1 |= s1
            res2 += s2
    return res1, res2


class Solver(BaseSolver):
    def solve(self) -> Solution:
        part1, part2 = 0, 0
        for start in self.intgrid.where(0):
            s1, s2 = score(self.intgrid, start)
            part1 += len(s1)
            part2 += s2
        yield part1
        yield part2


Solver.run()
