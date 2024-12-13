# /usr/bin/env python3

from __future__ import annotations

import dataclasses

# import heapq - no longer needed since we moved to z3
import re

import z3

from advent.base import BaseSolver, Solution
from advent.graph import Point

A_COST = 3
B_COST = 1


@dataclasses.dataclass
class Scenario:
    a: Point
    b: Point
    prize: Point

    @classmethod
    def from_lines(cls, lines: list[str]) -> Scenario:
        """
        Button A: X+94, Y+34
        Button B: X+22, Y+67
        Prize: X=8400, Y=5400
        """
        a = re.match(r"Button A: X\+(\d+), Y\+(\d+)", lines[0])
        b = re.match(r"Button B: X\+(\d+), Y\+(\d+)", lines[1])
        prize = re.match(r"Prize: X=(\d+), Y=(\d+)", lines[2])
        assert a and b and prize
        a_pt = Point(int(a[1]), int(a[2]))
        b_pt = Point(int(b[1]), int(b[2]))
        prize_pt = Point(int(prize[1]), int(prize[2]))
        return cls(a=a_pt, b=b_pt, prize=prize_pt)

    def min_moves(self, part2: bool = False) -> int | None:
        if part2:
            self.prize = Point(
                self.prize.row + 10000000000000, self.prize.col + 10000000000000
            )

        """
        Find solution to minimize cost such that...
        prize_x = a_x * a_presses + b_x * b_presses
        prize_y = a_y * a_presses + b_y * b_presses
        cost = 3 * a_presses + b_presses
        """
        opt = z3.Optimize()

        a = z3.Int("a")
        b = z3.Int("b")

        opt.add(a >= 0)
        opt.add(b >= 0)
        opt.add(self.prize.row == self.a.row * a + self.b.row * b)
        opt.add(self.prize.col == self.a.col * a + self.b.col * b)

        cost = 3 * a + b
        opt.minimize(cost)

        """
        Original approach below to part1 which used a priority queue
        pq = [(0, Point(0, 0))]
        seen = {(0, Point(0, 0))}
        while pq:
            cost, pos = heapq.heappop(pq)
            if pos == self.prize:
                return cost
            a_pos = pos + self.a
            b_pos = pos + self.b
            if a_pos.row <= self.prize.row and a_pos.col <= self.prize.col:
                val = (cost + A_COST, a_pos)
                if val not in seen:
                    heapq.heappush(pq, val)
                    seen.add(val)
            if b_pos.row <= self.prize.row and b_pos.col <= self.prize.col:
                val = (cost + B_COST, b_pos)
                if val not in seen:
                    heapq.heappush(pq, val)
                    seen.add(val)
        return None
        """

        if opt.check() == z3.sat:
            min_cost = opt.model().evaluate(cost)
            assert isinstance(min_cost, z3.IntNumRef)
            return min_cost.as_long()
        else:
            return None


class Solver(BaseSolver):
    def solve(self) -> Solution:
        sections = self.data.split("\n\n")

        part1 = 0
        part2 = 0
        for section in sections:
            s = Scenario.from_lines(section.splitlines())
            part1 += s.min_moves() or 0
            part2 += s.min_moves(True) or 0

        yield part1
        yield part2


Solver.run()
