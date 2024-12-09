# /usr/bin/env python3

from __future__ import annotations

import dataclasses
from typing import Iterator

from advent.base import BaseSolver, Solution


@dataclasses.dataclass
class Node:
    file_idx: int | None
    length: int
    prev: Node | None = None
    next: Node | None = None
    tail: Node | None = None

    @classmethod
    def from_runs(cls, runs: list[int]) -> Node:
        head = Node(-1, -1)
        cur = head
        for idx, run in enumerate(runs):
            if idx % 2 == 0:
                cur = cur.append(Node(idx // 2, run))
            else:
                cur = cur.append(Node(None, run))
        head.tail = cur.append(Node(-1, -1))
        return head

    def prepend(self, node: Node) -> Node:
        node.next = self
        node.prev = self.prev
        if self.prev is not None:
            self.prev.next = node
        self.prev = node
        return node

    def append(self, node: Node) -> Node:
        node.next = self.next
        self.next = node
        node.prev = self
        return node

    def defrag(self) -> None:
        for node in self:
            if node.file_idx is None:
                assert self.tail is not None
                rcur = self.tail.prev
                assert rcur is not None
                while node.length > 0 and rcur is not None and rcur is not node:
                    if rcur.file_idx is None or rcur.length == 0:
                        rcur = rcur.prev
                        continue

                    to_move = min(node.length, rcur.length)
                    # Now we *prepend* this node with our filled value
                    # And set the new length to remaining - to_move
                    node.prepend(Node(rcur.file_idx, to_move))
                    rcur.length -= to_move
                    node.length -= to_move

                    # Lastly: rcur has None added to its *end*
                    if rcur.next is not self.tail:
                        assert rcur.next is not None
                        if rcur.next.file_idx is None:
                            rcur.next.length += to_move
                        else:
                            rcur.append(Node(None, to_move))
                    rcur = rcur.prev

    def defrag2(self) -> None:
        moved = set()
        assert self.tail is not None
        rcur = self.tail.prev
        assert rcur is not None
        while rcur is not self:
            assert rcur is not None
            # If this is empty or of zero length, count it as "solved"
            if rcur.file_idx is None or rcur.length == 0 or rcur.file_idx in moved:
                rcur = rcur.prev
                continue

            for node in self:
                # First fit is *after* the block, which would make fragmentation worse
                if node is rcur:
                    break

                # Node isn't empty -> obviously can't move here
                if node.file_idx is not None:
                    continue

                # Block won't fit here, try the next one
                if rcur.length > node.length:
                    continue

                # Move the block here - this is equivalent to prepending the rcur node
                # and reducing this node's length accordingly
                node.prepend(Node(rcur.file_idx, rcur.length))
                node.length -= rcur.length
                moved.add(rcur.file_idx)
                rcur.file_idx = None
                # Merge it with the previous if they're both None now
                assert rcur.prev is not None
                if rcur.prev.file_idx is None:
                    to_add = rcur.length
                    next = rcur.next
                    # If the next is *also* None, they all get combined
                    assert rcur.next is not None
                    if rcur.next.file_idx is None:
                        to_add = rcur.length + rcur.next.length
                        next = rcur.next.next
                    rcur.prev.length += to_add
                    rcur.prev.next = next
                    assert next is not None
                    next.prev = rcur.prev
                break

            # Move onto the next block for defragging
            assert rcur is not None
            rcur = rcur.prev

    def checksum(self) -> int:
        res = 0
        block_idx = 0
        for node in self:
            # Sum from block_idx to block_idx + cur.length of block_idx * cur.file_idx
            if node.file_idx is not None:
                res += sum(
                    node.file_idx * b for b in range(block_idx, block_idx + node.length)
                )
            block_idx += node.length
        return res

    def __iter__(self) -> Iterator[Node]:
        cur = self.next
        while cur is not None and cur.length != -1:
            yield cur
            cur = cur.next

    def __str__(self) -> str:
        return "".join(
            (str(node.file_idx) if node.file_idx is not None else ".") * node.length
            for node in self
        )


class Solver(BaseSolver):
    def solve(self) -> Solution:
        runs = [int(c) for c in self.data.strip()]

        part1 = Node.from_runs(runs)
        part1.defrag()
        yield part1.checksum()

        part2 = Node.from_runs(runs)
        part2.defrag2()
        yield part2.checksum()


Solver.run()
