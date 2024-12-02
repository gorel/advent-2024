# /usr/bin/env python3

from __future__ import annotations

from advent.base import BaseSolver, Solution


def test(ints: list[int]) -> bool:
    prev_inc = None
    cur = ints[0]
    for i in range(1, len(ints)):
        prev = ints[i - 1]
        cur = ints[i]
        dir = 1 if cur > prev else -1
        if (
            cur == prev
            or (prev_inc is not None and dir != prev_inc)
            or abs(cur - prev) > 3
        ):
            return False
        prev_inc = dir
    return True


class Solver(BaseSolver):
    def solve(self) -> Solution:
        part1 = 0
        part2 = 0

        for line in self.lines:
            ints = [int(x) for x in line.split()]
            if test(ints):
                part1 += 1
                part2 += 1
            else:
                for i in range(len(ints)):
                    new_ints = ints[:i] + ints[i + 1 :]
                    if test(new_ints):
                        part2 += 1
                        break

        yield part1
        yield part2


Solver.run()
