# /usr/bin/env python3

from __future__ import annotations

import time

from rich.console import Group
from rich.live import Live
from rich.text import Text

from advent.base import BaseSolver, Solution
from advent.graph import Direction, Grid, Point


def can_move(
    grid: Grid[str],
    obj: tuple[Point, str],
    dir: Direction,
    checked: set[Point] | None = None,
) -> bool:
    checked = checked or set()
    # No need for inbounds checks since we have the surrounding '#'
    p = obj[0] + dir
    match c := grid[p]:
        case "#":
            return False
        case ".":
            return True
        case "[":
            # We also need to check that the right side can move
            checked.add(p)
            other_half_can_move = True
            if p + Direction.RIGHT not in checked:
                rp = p + Direction.RIGHT
                rc = grid[rp]
                other_half_can_move = can_move(grid, (rp, rc), dir, checked)
            return can_move(grid, (p, c), dir, checked) and other_half_can_move
        case "]":
            # We also need to check that the left side can move
            checked.add(p)
            other_half_can_move = True
            if p + Direction.LEFT not in checked:
                lp = p + Direction.LEFT
                lc = grid[lp]
                other_half_can_move = can_move(grid, (lp, lc), dir, checked)
            return can_move(grid, (p, c), dir, checked) and other_half_can_move
        case _:
            return can_move(grid, (p, c), dir)


def move(
    grid: Grid[str],
    obj: tuple[Point, str],
    dir: Direction,
    moved: set[Point] | None = None,
) -> tuple[Point, str]:
    moved = moved or set()
    # Assume can_move was called before
    p = obj[0] + dir
    if p in moved:
        return p, obj[1]
    moved.add(p)
    grid[obj[0]] = "."
    match grid[p]:
        case "O":
            move(grid, (p, grid[p]), dir, moved)
        case "[":
            move(grid, (p, grid[p]), dir, moved)
            if p + Direction.RIGHT not in moved:
                move(grid, (p + Direction.RIGHT, grid[p + Direction.RIGHT]), dir, moved)
        case "]":
            move(grid, (p, grid[p]), dir, moved)
            if p + Direction.LEFT not in moved:
                move(grid, (p + Direction.LEFT, grid[p + Direction.LEFT]), dir, moved)
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
        directions = "".join(s.strip() for s in directions_str)

        grid = Grid([list(line) for line in grid_str.splitlines()])
        robot = next(grid.where("@"))
        with Live() as live:
            d_total = Text()
            for d in directions:
                dir = Direction.from_str(d)
                moved = False
                if can_move(grid, robot, dir):
                    moved = True
                    robot = move(grid, robot, dir)
                if self.is_example:
                    time.sleep(0.5)
                    d_total.append(str(d), style="green" if moved else "red")
                    live.update(Group(d_total, grid.short_str()))
        yield sum(box.row * 100 + box.col for box, _ in grid.where("O"))

        grid2 = ENHANCE([list(line) for line in grid_str.splitlines()])
        robot = next(grid2.where("@"))
        with Live() as live:
            d_total = Text()
            for d in directions:
                dir = Direction.from_str(d)
                moved = False
                if can_move(grid2, robot, dir):
                    moved = True
                    robot = move(grid2, robot, dir)
                if self.is_example:
                    time.sleep(0.5)
                    d_total.append(str(d), style="green" if moved else "red")
                    live.update(Group(d_total, grid2.short_str()))
        yield sum(box.row * 100 + box.col for box, _ in grid2.where("["))


Solver.run()
