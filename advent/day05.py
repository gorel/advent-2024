# /usr/bin/env python3

from __future__ import annotations

import collections

from advent.base import BaseSolver, Solution


def fix(before: dict[str, set[str]], update: list[str]) -> int:
    res = []
    to_find = set(update)
    while len(to_find) > 0:
        for req in to_find:
            # Find the next thing that has all dependencies satisfied
            if before[req] & to_find:
                continue
            res.append(req)
            to_find.remove(req)
            break
    # Return the midpoint like before
    return res[len(res) // 2]


class Solver(BaseSolver):
    def solve(self) -> Solution:
        prereq = collections.defaultdict(set)
        updates = []
        in_rules = True
        for line in self.lines:
            if not line:
                in_rules = False
                continue
            if in_rules:
                l, r = line.split("|")
                prereq[r].add(l)
            else:
                updates.append(line.split(","))

        part1 = 0
        part2 = 0
        for update in updates:
            after = set(update)
            valid = True
            have = set()
            for req in update:
                # This thing is no longer coming later
                after.discard(req)
                # If any of the remaining "after" are in our "before", that's bad
                if after & prereq[req]:
                    valid = False
                    break
                have.add(req)
            if valid:
                part1 += int(update[len(update) // 2])
            else:
                part2 += int(fix(prereq, update))

        yield part1
        yield part2


Solver.run()
