# /usr/bin/env python3

from __future__ import annotations

import tqdm

from advent.base import BaseSolver, Solution
from advent.graph import Direction, Point


class Solver(BaseSolver):
    def flood(self, p: Point, c: str, seen: set[Point] | None = None) -> set[Point]:
        seen = seen or set()
        seen.add(p)
        for adj in p.adjacent():
            if adj not in seen and self.grid.inbounds(adj) and self.grid.at(adj) == c:
                self.flood(adj, c, seen)
        return seen

    def solve(self) -> Solution:
        seen = set()

        part1 = 0
        part2 = 0
        for p, c in tqdm.tqdm(self.grid, total=self.grid.rows * self.grid.cols):
            if p in seen:
                continue

            points = self.flood(p, c, set())
            outline = set()
            perimeter = 0
            for p in points:
                for adj, d in p.adjacent8_with_dirs():
                    if adj not in points:
                        # Only for the outline do we include the diagonal points.
                        # If we count them in the perimeter, we'd overcount.
                        outline.add(adj)
                        if d in Direction.cardinal():
                            perimeter += 1

            corners = 0
            for p in outline:
                for adj, d in p.adjacent_with_dirs():
                    # For each point *adjacent* to every point in the outline, if...
                    # - the adjacent point is also in the outline
                    # - looking clockwise from the outline point, the next point is in the outline, too
                    # - the point 45 degrees clockwise from the outline point is in the points set
                    # ...then we have found an *exterior* corner.
                    if (
                        adj in outline
                        and (p + d.clockwise) in outline
                        and (p + d.clockwise45) in points
                    ):
                        corners += 1
                    # In addition to the above, if...
                    # - the adjacent point is in the points set
                    # - looking clockwise from the outline point, the next point is in the points set, too
                    # ...then we have found an *interior* corner.
                    if adj in points and (p + d.clockwise) in points:
                        corners += 1

            part1 += perimeter * len(points)
            part2 += corners * len(points)
            seen |= points

        yield part1
        yield part2


Solver.run()
