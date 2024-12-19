# /usr/bin/env python3

from __future__ import annotations

import functools

from advent.base import BaseSolver, Solution


class Solver(BaseSolver):
    def solve(self) -> Solution:
        patterns_str, designs = self.sections
        patterns = [s.strip() for s in patterns_str.split(",")]

        @functools.cache
        def ways(design: str) -> int:
            if design == "":
                return 1
            return sum(
                ways(design[len(pattern) :])
                for pattern in patterns
                if design.startswith(pattern)
            )

        yield sum(ways(design) > 0 for design in designs.splitlines())
        yield sum(ways(design) for design in designs.splitlines())


Solver.run()
