# /usr/bin/env python3

from __future__ import annotations

import collections

from advent.base import BaseSolver, Solution


def evolve(n: int) -> int:
    # Mult 64, mix with secret, and prune
    # 16777216 = 0b1000000000000000000000000
    #          = 1 + 0xFFFFFF
    res = ((n << 6) ^ n) & 0xFFFFFF
    # Divide 32, mix with secret, and prune
    res = ((res >> 5) ^ res) & 0xFFFFFF
    # Mult 2048, mix with secret, and prune
    res = ((res << 11) ^ res) & 0xFFFFFF
    return res


class Solver(BaseSolver):
    def solve(self) -> Solution:
        part1 = 0
        seq = collections.defaultdict(dict)
        for i, line in enumerate(self.lines):
            cur = int(line)
            last4 = collections.deque([])
            for _ in range(2000):
                last4.append(cur % 10)
                nxt = evolve(cur)
                if len(last4) > 4:
                    rng = tuple(last4[x + 1] - last4[x] for x in range(len(last4) - 1))
                    last4.popleft()
                    if i not in seq[rng]:
                        seq[rng][i] = last4[-1]
                cur = nxt
            # And record the last number
            last4.append(cur % 10)
            if len(last4) > 4:
                rng = tuple(last4[x + 1] - last4[x] for x in range(len(last4) - 1))
                last4.popleft()
                if i not in seq[rng]:
                    seq[rng][i] = last4[-1]
            part1 += cur
        yield part1

        yield max(sum(seq[rng].values()) for rng in seq)


Solver.run()
