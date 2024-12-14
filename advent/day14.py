# /usr/bin/env python3

from __future__ import annotations

import re

from advent.base import BaseSolver, Solution


class Solver(BaseSolver):
    def solve(self) -> Solution:
        width = 11 if self.is_example else 101
        height = 7 if self.is_example else 103

        Q = [0, 0, 0, 0]
        robots = []
        for line in self.lines:
            # p=0,4 v=3,-3
            match = re.findall(r"-?\d+", line)
            px, py = int(match[0]), int(match[1])
            vx, vy = int(match[2]), int(match[3])
            robots.append(((px, py), (vx, vy)))

            px, py = (px + vx * 100) % width, (py + vy * 100) % height

            # Sort into quadrants, ignoring things in the axes
            if px == width // 2 or py == height // 2:
                continue
            if px < width // 2:
                if py < height // 2:
                    Q[0] += 1
                else:
                    Q[1] += 1
            else:
                if py < height // 2:
                    Q[2] += 1
                else:
                    Q[3] += 1

        yield Q[0] * Q[1] * Q[2] * Q[3]

        if self.is_example:
            yield None

        i = 0
        while True:
            i += 1
            ps = set()
            for (px, py), (vx, vy) in robots:
                px, py = (px + vx * i) % width, (py + vy * i) % height
                if (px, py) in ps:
                    break
                ps.add((px, py))

            # I *did not* find this solution myself (I just ran through until
            # I saw a tree in my terminal), but the "trick" is to look for a
            # case where the robots are all on unique positions.
            if len(ps) == len(robots):
                yield i

            """
            # Original solution using "printing and staring" technique

            time.sleep(0.1)
            os.system("clear")
            print(f"After {i} seconds")
            for y in range(height):
                for x in range(width):
                    print("#" if (x, y) in ps else " ", end="")
                print()
            """


Solver.run()
