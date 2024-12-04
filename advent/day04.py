# /usr/bin/env python3

from __future__ import annotations

from advent.base import BaseSolver, Solution
from advent.graph import Direction, Grid


class Solver(BaseSolver):
    def solve(self) -> Solution:
        g = Grid.from_lines(self.lines)

        part1 = 0
        for p, _ in g.where("X"):
            for dir in Direction:
                if all(
                    g.at0(p2) == "XMAS"[i]
                    for i, p2 in enumerate(p.walk(dir, len("XMAS")))
                ):
                    part1 += 1
        yield part1

        part2 = 0
        for p, c in g.where("A"):
            diag1 = {c, g.at0(p + Direction.UPLEFT), g.at0(p + Direction.DOWNRIGHT)}
            diag2 = {c, g.at0(p + Direction.UPRIGHT), g.at0(p + Direction.DOWNLEFT)}
            if diag1 == set("MAS") and diag2 == set("MAS"):
                part2 += 1
        yield part2


Solver.run()
