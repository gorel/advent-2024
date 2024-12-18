# /usr/bin/env python3

from __future__ import annotations

import networkx as nx

from advent.base import BaseSolver, Solution


class Solver(BaseSolver):
    def solve(self) -> Solution:
        g = nx.Graph()

        size = 71 if self.is_real else 7
        first = 1024 if self.is_real else 12
        points = set()
        for line in self.lines[:first]:
            x, y = line.split(",")
            points.add((int(x), int(y)))

        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for x in range(size):
            for y in range(size):
                if (x, y) in points:
                    continue
                for dx, dy in dirs:
                    xx, yy = x + dx, y + dy
                    if 0 <= xx < size and 0 <= yy < size and (xx, yy) not in points:
                        g.add_edge((x, y), (xx, yy))
        yield len(nx.shortest_path(g, (0, 0), (size - 1, size - 1))) - 1

        for line in self.lines[first:]:
            x, y = line.split(",")
            px, py = int(x), int(y)
            for dx, dy in dirs:
                xx, yy = px + dx, py + dy
                if 0 <= xx < size and 0 <= yy < size and (xx, yy) not in points:
                    if g.has_edge((px, py), (xx, yy)):
                        g.remove_edge((px, py), (xx, yy))
            try:
                nx.shortest_path(g, (0, 0), (size - 1, size - 1))
            except nx.NetworkXNoPath:
                yield line


Solver.run()
