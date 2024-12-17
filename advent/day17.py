# /usr/bin/env python3

from __future__ import annotations

import dataclasses

import z3

from advent.base import BaseSolver, Solution


@dataclasses.dataclass
class Computer:
    prog: list[int]
    reg: dict[str, int]
    ip: int = 0
    out: list[int] = dataclasses.field(default_factory=list)
    matching: bool = False
    start_a: int | None = None

    def run(self, a: int | None = None) -> list[int]:
        self.start_a = a
        cache = set()
        if a is not None:
            self.reg["A"] = a
            self.matching = True

        while self.ip < len(self.prog) - 1:
            cache_key = (self.ip, self.reg["A"], self.reg["B"], self.reg["C"])
            if cache_key in cache:
                return [-1]
            cache.add(cache_key)
            opcode = self.prog[self.ip]
            operand = self.prog[self.ip + 1]
            self.op(opcode, operand)
        return self.out

    def op(self, opcode: int, operand: int) -> None:
        match opcode:
            case 0:  # adv
                self.reg["A"] = self.reg["A"] // 2 ** self.combo(operand)
            case 1:  # bxl
                self.reg["B"] = self.reg["B"] ^ operand
            case 2:  # bst
                self.reg["B"] = self.combo(operand) % 8
            case 3:  # jnz
                if self.reg["A"] != 0:
                    self.ip = operand - 2
            case 4:  # bxc
                self.reg["B"] = self.reg["B"] ^ self.reg["C"]
            case 5:  # out
                self.out.append(self.combo(operand) % 8)
                idx = len(self.out) - 1
                if self.matching:
                    if idx > 7:
                        print(f"Got success at {idx} for starting a {self.start_a}")
                    if self.matching and self.out[idx] != self.prog[idx]:
                        self.ip = len(self.prog)
            case 6:  # bdv
                self.reg["B"] = self.reg["A"] // 2 ** self.combo(operand)
            case 7:  # cdv
                self.reg["C"] = self.reg["A"] // 2 ** self.combo(operand)
        self.ip += 2

        pass

    def combo(self, combo: int) -> int:
        match combo:
            case 4:
                return self.reg["A"]
            case 5:
                return self.reg["B"]
            case 6:
                return self.reg["C"]
            case 7:
                exit("Encountered combo(7) - you messed up")
            case _:
                return combo


class Solver(BaseSolver):
    def solve(self) -> Solution:
        #          0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
        # Program: 2,4,1,3,7,5,1,5,0,3,4,2,5,5,3,0
        #                                      ^
        # ip= 0: bst 4 -> B = A % 8
        # ip= 2: bxl 3 -> B = B ^ 3
        # ip= 4: cdv 5 -> C = A / (1<<B)
        # ip= 6: bxl 5 -> B = B ^ 5
        # ip= 8: adv 3 -> A = A / 8
        # ip=10: bxc 2 -> B = B ^ C
        # ip=12: out 5 -> out B % 8
        # ip=14: jnz
        """
        while a != 0:
            b = a % 8
            b = b ^ 3
            c = a / (1 << b)
            b = b ^ 5
            a = a / 8
            b = b ^ c
            print(b % 8)
        """

        registers, program = self.sections

        reg = {}
        for register in registers.split("\n"):
            parts = register.split()
            reg[parts[1].rstrip(":")] = int(parts[2])

        prog = [int(x) for x in program.split()[1].split(",")]
        c = Computer(prog, reg)
        out = c.run()
        yield ",".join(str(i) for i in out)

        if self.is_example:
            a = 0
            res = []
            while res != prog:
                a += 1
                res = Computer(prog, reg).run(a)
            yield a
            return

        opt = z3.Optimize()
        # Assuming a fits in a 64-bit int
        avec = z3.BitVec("a", 64)
        a, b, c = avec, 0, 0
        for expected in prog:
            b = a % 8
            b = b ^ 3
            c = a / (1 << b)
            b = b ^ 5
            a = a / 8
            b = b ^ c
            opt.add((b % 8) == expected)
        opt.add(a == 0)
        opt.minimize(avec)
        if opt.check() == z3.sat:
            res = opt.model().eval(avec)
            assert isinstance(res, z3.BitVecNumRef)
            yield res.as_long()


Solver.run()
