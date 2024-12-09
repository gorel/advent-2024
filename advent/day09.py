# /usr/bin/env python3

from __future__ import annotations

from advent.base import BaseSolver, Solution


def calculate(
    vals: list[tuple[int | None, int]], move_blocks: bool = False
) -> tuple[str, int]:
    s = ""
    res = 0
    block_idx = 0
    l_idx = 0
    while l_idx < len(vals):
        val, run = vals[l_idx]
        # Move items from the right
        if val is None:
            remaining = run
            r_idx = len(vals) - 1
            while remaining and l_idx <= r_idx:
                rval, rrun = vals[r_idx]
                if rval is None or rrun == 0:
                    r_idx -= 1
                    continue

                if move_blocks and rrun > remaining:
                    r_idx -= 1
                    continue

                to_move = min(remaining, rrun)
                vals[r_idx] = (rval, rrun - to_move)
                # sum from b = block_idx to block_idx + to_move of b * rval
                res += sum(b * rval for b in range(block_idx, block_idx + to_move))
                s += str(rval) * to_move
                if vals[r_idx][-1] == 0:
                    r_idx -= 1
                block_idx += to_move
                remaining -= to_move
            s += "." * remaining
            block_idx += remaining
        else:
            # Sum from b = block_idx to block_idx + run of b * val
            res += sum(b * val for b in range(block_idx, block_idx + run))
            block_idx += run
            s += str(val) * run
        l_idx += 1
    return s, res


def runs_to_vals(runs: list[int]) -> list[tuple[int | None, int]]:
    vals = []
    for idx, run in enumerate(runs):
        if idx % 2 == 0:
            vals.append((idx // 2, run))
        else:
            vals.append((None, run))
    return vals


class Solver(BaseSolver):
    def solve(self) -> Solution:
        runs = [int(c) for c in self.data.strip()]

        _, part1 = calculate(runs_to_vals(runs))
        _, part2 = calculate(runs_to_vals(runs), move_blocks=True)
        yield part1
        yield part2


Solver.run()
