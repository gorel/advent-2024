# /usr/bin/env python3

from __future__ import annotations

import networkx as nx

from advent.base import BaseSolver, Solution


class Solver(BaseSolver):
    def solve(self) -> Solution:
        g = nx.Graph([line.split("-") for line in self.lines])  # pyright: ignore
        yield sum(
            len(clique) == 3 and any(pc.startswith("t") for pc in clique)
            for clique in nx.enumerate_all_cliques(g)
        )
        yield ",".join(sorted(max(nx.find_cliques(g), key=len)))


Solver.run()
