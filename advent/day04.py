# /usr/bin/env python3

from __future__ import annotations

from advent.base import BaseSolver, Solution
from advent.graph import Direction, Grid


class Solver(BaseSolver):
    def solve(self) -> Solution:
        g = Grid(g=[[c for c in line] for line in self.lines])

        part1 = 0
        for p, c in g:
            if c == "X":
                for dir in Direction:
                    m_pt = p + dir
                    a_pt = m_pt + dir
                    s_pt = a_pt + dir
                    if g.at0(m_pt) == "M" and g.at0(a_pt) == "A" and g.at0(s_pt) == "S":
                        part1 += 1

        part2 = 0
        for p, c in g:
            if c == "A":
                ulc = g.at0(p + Direction.UPLEFT)
                urc = g.at0(p + Direction.UPRIGHT)
                dlc = g.at0(p + Direction.DOWNLEFT)
                drc = g.at0(p + Direction.DOWNRIGHT)
                # Find M->S going up or down on each diagonal
                if ((ulc == "M" and drc == "S") or (ulc == "S" and drc == "M")) and (
                    (urc == "M" and dlc == "S") or (urc == "S" and dlc == "M")
                ):
                    part2 += 1

        yield part1
        yield part2


Solver.run()
