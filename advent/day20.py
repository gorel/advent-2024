# /usr/bin/env python3

from __future__ import annotations

from typing import cast

import networkx as nx

from advent.base import BaseSolver, Solution
from advent.graph import Grid, Point


class Solver(BaseSolver):
    def solve(self) -> Solution:
        target = 100 if self.is_real else 50

        g = Grid([list(row) for row in self.lines])
        start, _ = next(g.where("S"))
        end, _ = next(g.where("E"))
        path = cast(list[Point], nx.shortest_path(g.to_nx_graph(), start, end))

        part1 = 0
        part2 = 0
        for i in range(len(path) - 1):
            p = path[i]
            # Try every point ahead of this one on the path
            for j in range(i + 1, len(path)):
                p2 = path[j]
                old_length = j - i
                new_length = p.manhattan_dist(p2)
                time_saved = old_length - new_length
                if time_saved >= target:
                    if new_length <= 2:
                        part1 += 1
                    if new_length <= 20:
                        part2 += 1

        yield part1
        yield part2


Solver.run()
