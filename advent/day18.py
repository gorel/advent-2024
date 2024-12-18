# /usr/bin/env python3

from __future__ import annotations

import networkx as nx

from advent.base import BaseSolver, Solution


class Solver(BaseSolver):
    def build_graph(self, size: int, n: int) -> nx.Graph:
        points = set()
        for line in self.lines[:n]:
            x, y = line.split(",")
            points.add((int(x), int(y)))
        g = nx.Graph()
        for x in range(size):
            for y in range(size):
                if (x, y) in points:
                    continue
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    xx, yy = x + dx, y + dy
                    if 0 <= xx < size and 0 <= yy < size and (xx, yy) not in points:
                        g.add_edge((x, y), (xx, yy))
        return g

    def solve(self) -> Solution:
        size = 71 if self.is_real else 7
        n = 1024 if self.is_real else 12
        g = self.build_graph(size, n)
        yield len(nx.shortest_path(g, (0, 0), (size - 1, size - 1))) - 1

        lo = n
        hi = len(self.lines)
        while lo < hi:
            mid = (lo + hi) // 2
            g = self.build_graph(size, mid)
            try:
                nx.shortest_path(g, (0, 0), (size - 1, size - 1))
                lo = mid + 1
            except Exception:
                hi = mid
        yield self.lines[lo - 1]


Solver.run()
