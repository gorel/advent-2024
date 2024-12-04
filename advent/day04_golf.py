# /usr/bin/env python3

from __future__ import annotations

from advent.base import BaseSolver, Solution
from advent.graph import Direction, Grid


class Solver(BaseSolver):
    @classmethod
    def day(cls) -> int:
        return 4

    def solve(self) -> Solution:
        g = Grid.from_lines(self.lines)

        yield sum(
            all(g.at0(p2) == "XMAS"[i] for i, p2 in enumerate(p.walk(dir, len("XMAS"))))
            for p, _ in g.where("X")
            for dir in Direction
        )

        yield sum(
            {c, g.at0(p + Direction.UPLEFT), g.at0(p + Direction.DOWNRIGHT)}
            == {c, g.at0(p + Direction.UPRIGHT), g.at0(p + Direction.DOWNLEFT)}
            == set("MAS")
            for p, c in g.where("A")
        )


Solver.run()
