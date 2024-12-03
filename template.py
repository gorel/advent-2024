# /usr/bin/env python3

from __future__ import annotations

from advent.base import BaseSolver, Solution


class Solver(BaseSolver):
    def solve(self) -> Solution:
        part1 = 0
        for line in self.lines:
            ints = [int(x) for x in line.split()]

        yield part1
        yield None


Solver.run()
