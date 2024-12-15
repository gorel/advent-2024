# /usr/bin/env python3

from __future__ import annotations

from advent.base import BaseSolver, Solution
from advent.graph import Direction, Grid, Point


def can_move(grid: Grid[str], obj: tuple[Point, str], dir: Direction) -> bool:
    # No need for inbounds checks since we have the surrounding '#'
    p = obj[0] + dir
    match c := grid[p]:
        case "#":
            return False
        case ".":
            return True
        case "[":
            # We also need to check that the right side can move
            rp = p + Direction.RIGHT
            rc = grid[rp]
            return can_move(grid, (p, c), dir) and can_move(grid, (rp, rc), dir)
        case "]":
            # We also need to check that the left side can move
            lp = p + Direction.LEFT
            lc = grid[lp]
            return can_move(grid, (p, c), dir) and can_move(grid, (lp, lc), dir)
        case _:
            return can_move(grid, (p, c), dir)


def move(grid: Grid[str], obj: tuple[Point, str], dir: Direction) -> tuple[Point, str]:
    # Assume can_move was called before
    p = obj[0] + dir
    c = grid[p]
    grid[obj[0]] = "."
    match grid[p]:
        case "0":
            move(grid, (p, c), dir)
        case "[":
            move(grid, (p, c), dir)
            move(grid, (p + Direction.RIGHT, grid[p + Direction.RIGHT]), dir)
        case "]":
            move(grid, (p, c), dir)
            move(grid, (p + Direction.LEFT, grid[p + Direction.LEFT]), dir)
    grid[p] = obj[1]
    return p, obj[1]


def ENHANCE(gridlines: list[list[str]]) -> Grid[str]:
    res = []
    for line in gridlines:
        row = []
        for c in line:
            match c:
                case "#" | ".":
                    row += [c, c]
                case "@":
                    row += ["@", "."]
                case "O":
                    row += ["[", "]"]
        res.append(row)
    return Grid(res)


class Solver(BaseSolver):
    def solve(self) -> Solution:
        grid_str, directions_str = self.sections
        grid = Grid([list(line) for line in grid_str.splitlines()])
        directions = "".join(s.strip() for s in directions_str)

        robot = next(grid.where("@"))
        for d in directions:
            dir = Direction.from_str(d)
            if can_move(grid, robot, dir):
                robot = move(grid, robot, dir)

        yield sum(box.row * 100 + box.col for box, _ in grid.where("O"))

        grid2 = ENHANCE([list(line) for line in grid_str.splitlines()])
        robot = next(grid2.where("@"))
        for d in directions:
            dir = Direction.from_str(d)
            if can_move(grid2, robot, dir):
                robot = move(grid2, robot, dir)

        yield sum(box.row * 100 + box.col for box, _ in grid2.where("["))


Solver.run()
