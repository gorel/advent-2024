# /usr/bin/env python3

from __future__ import annotations

import operator

from advent.base import BaseSolver, Solution

OPS = {
    1: [operator.add, operator.mul],
    2: [operator.add, operator.mul, lambda a, b: int(str(a) + str(b))],
}


def try_combos(
    target: int,
    arr: list[int],
    idx: int,
    cur: int,
    part2: bool = False,
) -> int | None:
    if idx >= len(arr) or cur > target:
        return cur if cur == target else None
    else:
        for op in OPS[2] if part2 else OPS[1]:
            new_cur = op(cur, arr[idx])
            res = try_combos(target, arr, idx + 1, new_cur, part2)
            if res is not None:
                return res
    return None


class Solver(BaseSolver):
    def solve(self) -> Solution:
        part1 = 0
        part2 = 0
        for line in self.lines:
            target, nums = line.split(":")
            nums = [int(x) for x in nums.split()]
            res = try_combos(int(target), nums, 1, nums[0])
            part1 += res if res is not None else 0
            res2 = res or try_combos(int(target), nums, 1, nums[0], part2=True)
            part2 += res2 if res2 is not None else 0

        yield part1
        yield part2


Solver.run()
