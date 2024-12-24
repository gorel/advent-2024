# /usr/bin/env python3

from __future__ import annotations

import operator
import re

import graphviz

from advent.base import BaseSolver, Solution

OPS = {"AND": operator.and_, "OR": operator.or_, "XOR": operator.xor}
OPCOLORS = {"AND": "red", "OR": "green", "XOR": "blue"}

Gate = tuple[str, str, str]


def wiresum(wires: dict[str, int], prefix: str) -> int:
    res = 0
    for i in range(max(int(w[1:]) for w in wires if w.startswith(prefix)), -1, -1):
        res = (res << 1) | wires[f"{prefix}{i:02d}"]
    return res


class Solver(BaseSolver):
    def simulate(self, wires: dict[str, int], dep: dict[str, Gate]) -> tuple[dict[str, int], int]:
        wires = wires.copy()
        progress = True
        while progress:
            progress = False
            for out, (lhs, op, rhs) in dep.items():
                if out in wires:
                    continue
                if lhs in wires and rhs in wires:
                    wires[out] = OPS[op](wires[lhs], wires[rhs])
                    progress = True
        return wires, wiresum(wires, "z")

    def debug_wires(self, wires: dict[str, int], dep: dict[str, Gate]) -> list[str]:
        wires = wires.copy()
        g = graphviz.Digraph(filename="wires", format="png")

        found_bad = []
        # [dnn XOR dqd -> ffj] and [dnn AND dqd -> z08]
        dep["z08"] = "dnn", "XOR", "dqd"
        dep["ffj"] = "dnn", "AND", "dqd"
        found_bad += ["z08", "ffj"]
        # [x15 XOR y15 -> kfm] and [x15 AND y15 -> dwp]
        dep["kfm"] = "x15", "AND", "y15"
        dep["dwp"] = "x15", "XOR", "y15"
        found_bad += ["kfm", "dwp"]
        # [x22 AND y22 -> z22] and [hgq XOR pgt -> gjh]
        dep["z22"] = "hgq", "XOR", "pgt"
        dep["gjh"] = "x22", "AND", "y22"
        found_bad += ["z22", "gjh"]
        # [rns XOR hnn -> jdr] and [ctt OR vhw -> z31]
        dep["z31"] = "rns", "XOR", "hnn"
        dep["jdr"] = "ctt", "OR", "vhw"
        found_bad += ["z31", "jdr"]

        # NOTE: We expect every z[i] to have an input of an XOR gate.
        # Except the last one, which takes the "carry"
        for out, (lhs, op, rhs) in dep.items():
            if out[0] == "z" and op != "XOR":
                # Carry
                if op == "OR" and out == max(dep):
                    continue

                for node in lhs, rhs, out:
                    g.node(node, fillcolor="red", style="filled")
                print(f"Possible incorrect wire at {lhs} {op} {rhs} => {out}")

        # Check against expected out
        wires_out, z = self.simulate(wires, dep)
        x = wiresum(wires_out, "x")
        y = wiresum(wires_out, "y")
        expect = bin(x + y)
        actual = bin(z)
        print(f"Expect {expect}")
        print(f"Actual {actual}")
        bad = []
        for i, (e, a) in enumerate(zip(expect, actual)):
            if e != a:
                idx = len(expect) - i - 1
                bad.append(idx)
                g.node(f"z{idx:02d}", fillcolor="red", style="filled")
        if bad:
            print(f"Bad outputs: {bad}")

        # Add edges on x, y, and z for visualization
        added = set()
        for out, (lhs, op, rhs) in dep.items():
            g.edge(lhs, out, color=OPCOLORS[op])
            g.edge(rhs, out, color=OPCOLORS[op])
            for w in out, lhs, rhs:
                if w[0] in "xyz" and w not in added:
                    val = int(re.findall(r"\d+", w)[0])
                    nodename = f"{w[0]}{val+1:02d}"
                    if nodename in wires or nodename in dep:
                        g.edge(w, f"{w[0]}{val+1:02d}")
                    added.add(w)

        g.render()
        return found_bad


    def solve(self) -> Solution:
        dep, wires = {}, {}
        for gate in self.sections[1].splitlines():
            lhs, op, rhs, _, out = gate.split()
            dep[out] = lhs, op, rhs

        for wire in self.sections[0].splitlines():
            lhs, rhs = wire.split(":")
            wires[lhs] = int(rhs)
        _, part1 = self.simulate(wires, dep)
        yield part1

        if self.is_example:
            yield None

        part2 = self.debug_wires(wires, dep)
        yield ",".join(sorted(part2))


Solver.run()
