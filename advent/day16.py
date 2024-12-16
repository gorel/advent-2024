# /usr/bin/env python3

from __future__ import annotations

import heapq

from advent.base import BaseSolver, Solution
from advent.graph import Direction, Point


class Solver(BaseSolver):
    def explore(self) -> dict[tuple[Point, Direction], int]:
        start, _ = next(self.grid.where("S"))
        pq = [(0, start, Direction.RIGHT)]
        min_cost = {}

        while pq:
            cost, pos, dir = heapq.heappop(pq)
            if cost > min_cost.get((pos, dir), float("inf")):
                continue
            min_cost[pos, dir] = cost

            # Add turns
            for d2 in [dir.counter_clockwise, dir.clockwise]:
                if cost + 1000 < min_cost.get((pos, d2), float("inf")):
                    min_cost[pos, d2] = cost + 1000
                    heapq.heappush(pq, (cost + 1000, pos, d2))
            # Add forward movement
            forward_pos = pos + dir
            if self.grid[forward_pos] != "#":
                if cost + 1 < min_cost.get((forward_pos, dir), float("inf")):
                    min_cost[forward_pos, dir] = cost + 1
                    heapq.heappush(pq, (cost + 1, forward_pos, dir))
        return min_cost

    def backtrack(
        self,
        pos: Point,
        dir: Direction,
        min_cost: dict[tuple[Point, Direction], int],
        cur_cost: int,
        res: set[Point] | None = None,
    ) -> set[Point]:
        res = res or set()
        # Walk "backwards"
        back_pos = pos - dir
        if min_cost.get((back_pos, dir), float("inf")) == cur_cost - 1:
            res.add(back_pos)
            res |= self.backtrack(back_pos, dir, min_cost, cur_cost - 1, res)
        # Turn left/right (same as before since their inverse is the same)
        for d2 in [dir.counter_clockwise, dir.clockwise]:
            if min_cost.get((pos, d2), float("inf")) == cur_cost - 1000:
                res |= self.backtrack(pos, d2, min_cost, cur_cost - 1000, res)
        return res

    def solve(self) -> Solution:
        end, _ = next(self.grid.where("E"))
        min_cost = self.explore()
        paths = [(end, d) for d in Direction if (end, d) in min_cost]
        min_to_end = min(min_cost[p] for p in paths)
        yield min_to_end

        # Move backwards from the end to find all viable spots
        part2 = {end}
        for pos, dir in paths:
            if min_cost[pos, dir] == min_to_end:
                part2 |= self.backtrack(pos, dir, min_cost, min_to_end)
        yield len(part2)


Solver.run()
