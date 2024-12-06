# /usr/bin/env python3

from __future__ import annotations

from advent.base import BaseSolver, Solution
from advent.graph import Direction, Grid, Point


def is_looping(g: Grid, start: tuple[Point, Direction], obj: Point) -> bool:
    pos, dir = start
    seen = set()
    while g.inbounds(pos):
        if (pos, dir) in seen:
            return True
        seen.add((pos, dir))
        candidate = pos + dir
        if g.at0(candidate) == "#" or candidate == obj:
            dir = dir.clockwise
        else:
            pos = candidate
    return False


class Solver(BaseSolver):
    def solve(self) -> Solution:
        g = Grid([list(line) for line in self.lines])

        pos, _ = next(g.where("^"))
        dir = Direction.UP
        start = pos, dir

        seen = set()
        while g.inbounds(pos):
            if (pos, dir) in seen:
                break
            seen.add((pos, dir))
            candidate = pos + dir
            if g.at0(candidate) == "#":
                dir = dir.clockwise
            else:
                pos = candidate
        points = {p for p, _ in seen}
        yield len(points)

        part2 = 0
        for p in points - {pos}:
            if is_looping(g, start=start, obj=p):
                part2 += 1
        yield part2


Solver.run()
