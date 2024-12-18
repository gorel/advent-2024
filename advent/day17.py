# /usr/bin/env python3

from __future__ import annotations

import dataclasses

from advent.base import BaseSolver, Solution


@dataclasses.dataclass
class Computer:
    prog: list[int]
    a: int
    b: int = 0
    c: int = 0
    ip: int = 0
    out: list[int] = dataclasses.field(default_factory=list)
    matching: bool = False

    def match_one(self) -> int:
        return self.run(match_one=True)[0]

    def run(self, match_one: bool = False) -> list[int]:
        cache = set()

        while self.ip < len(self.prog) - 1:
            cache_key = (self.ip, self.a, self.b, self.c)
            # To avoid an input that never halts
            if cache_key in cache:
                return [-1]
            cache.add(cache_key)
            opcode = self.prog[self.ip]
            operand = self.prog[self.ip + 1]
            self.op(opcode, operand)
            if match_one and len(self.out) > 0:
                break
        return self.out

    def op(self, opcode: int, operand: int) -> None:
        match opcode:
            case 0:  # adv
                self.a = self.a // 2 ** self.combo(operand)
            case 1:  # bxl
                self.b = self.b ^ operand
            case 2:  # bst
                self.b = self.combo(operand) % 8
            case 3:  # jnz
                if self.a != 0:
                    self.ip = operand - 2
            case 4:  # bxc
                self.b = self.b ^ self.c
            case 5:  # out
                self.out.append(self.combo(operand) % 8)
                idx = len(self.out) - 1
                if self.matching:
                    if self.matching and self.out[idx] != self.prog[idx]:
                        self.ip = len(self.prog)
            case 6:  # bdv
                self.b = self.a // 2 ** self.combo(operand)
            case 7:  # cdv
                self.c = self.a // 2 ** self.combo(operand)
        self.ip += 2

        pass

    def combo(self, combo: int) -> int:
        match combo:
            case 4:
                return self.a
            case 5:
                return self.b
            case 6:
                return self.c
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
        c = Computer(prog, reg["A"])
        out = c.run()
        yield ",".join(str(i) for i in out)

        if self.is_example:
            a = 0
            res = []
            while res != prog:
                a += 1
                res = Computer(prog, a).run()
            yield a
            return

        # Prog[-i] only depends on the last three bits of A. Therefore, we can
        # work backwards to generate the set of possible 3-bit A values that
        # output the target value to build up our solution. We need to check
        # *all* possibilities at each stage, because some bits may generate some
        # of the last few outputs while not solving the first few. At the end,
        # we just return the smallest input that yields the quine.
        possibilities = {0}
        for expected in prog[::-1]:
            next_possibilities = set()
            for res in possibilities:
                next_possibilities |= {
                    (res << 3 | c)
                    for c in range(8)
                    if Computer(prog, res << 3 | c).match_one() == expected
                }
            possibilities = next_possibilities
        yield min(possibilities)


Solver.run()
