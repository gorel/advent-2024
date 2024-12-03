# /usr/bin/env python3

from __future__ import annotations

import re

from advent.base import BaseSolver, Solution

# Find groups like mul(\d+,\d+)
R = re.compile(r"mul\((\d+),(\d+)\)")
# Find groups like mul(\d+,\d+) or do() or don't()
R2 = re.compile(r"(mul\((\d+),(\d+)\))|(do\(\))|(don't\(\))")


class Solver(BaseSolver):
    def solve(self) -> Solution:
        part1 = 0
        for match in R.findall(self.data):
            ints = [int(x) for x in match]
            part1 += ints[0] * ints[1]
        yield part1

        part2 = 0
        do = True
        for match in R2.findall(self.data):
            if match[3]:
                do = True
            elif match[4]:
                do = False
            elif do:
                ints = [int(x) for x in match[1:3]]
                part2 += ints[0] * ints[1]
        yield part2


Solver.run()
