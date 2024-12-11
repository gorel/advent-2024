# /usr/bin/env python3

from __future__ import annotations

import functools

from advent.base import BaseSolver, Solution


def split_even(n: int) -> list[int] | None:
    s = str(n)
    if len(s) % 2 == 0:
        left = s[: len(s) // 2]
        right = s[len(s) // 2 :]
        return [int(left), int(right)]
    return None


@functools.cache
def apply_rules(n: int, times: int) -> int:
    if times == 0:
        return 1
    for rule in [lambda s: [1] if s == 0 else None, split_even]:
        res = rule(n)
        if res is not None:
            return sum(apply_rules(r, times - 1) for r in res)
    return apply_rules(n * 2024, times - 1)


class Solver(BaseSolver):
    def solve(self) -> Solution:
        blinks = [int(c) for c in self.data.strip().split()]
        yield sum(apply_rules(blink, 25) for blink in blinks)
        yield sum(apply_rules(blink, 75) for blink in blinks)


Solver.run()
