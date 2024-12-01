# /usr/bin/env python3

from __future__ import annotations

import collections

from advent.base import BaseSolver, Solution


class Solver(BaseSolver):
    def solve(self) -> Solution:
        ls = []
        rs = []
        for line in self.lines:
            l, r = line.split()
            ls.append(int(l))
            rs.append(int(r))
        ls.sort()
        rs.sort()
        d = collections.Counter(rs)

        part1 = 0
        part2 = 0
        for i in range(len(ls)):
            part1 += abs(ls[i] - rs[i])
            part2 += d[ls[i]] * ls[i]

        yield part1
        yield part2


Solver.run()
