# /usr/bin/env python3

from __future__ import annotations

import collections

import itertools

from advent.base import BaseSolver, Solution
from advent.graph import Grid


class Solver(BaseSolver):
    def solve(self) -> Solution:
        g = Grid([list(line) for line in self.lines])
        antenna = collections.defaultdict(set)
        for p, c in g.where(lambda _, c: c != "."):
            antenna[c].add(p)

        antinodes = set()
        antinodes2 = set()
        # Now use point pairs to find antinodes
        for _, antennas in antenna.items():
            for p1, p2 in itertools.combinations(antennas, 2):
                antinodes2.add(p2)
                antinodes2.add(p1)
                drow, dcol = p1.row - p2.row, p1.col - p2.col
                a0 = p1 + (drow, dcol)
                a1 = p2 + (-drow, -dcol)
                if g.inbounds(a0):
                    antinodes.add(a0)
                    while g.inbounds(a0):
                        antinodes2.add(a0)
                        a0 += (drow, dcol)
                if g.inbounds(a1):
                    antinodes.add(a1)
                    while g.inbounds(a1):
                        antinodes2.add(a1)
                        a1 += (-drow, -dcol)

        yield len(antinodes)
        yield len(antinodes2)


Solver.run()
