from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from queue import PriorityQueue

from advent.common.position import ORIGIN, Position

day_num = 18


class PathNotFoundException(Exception):
    pass


@dataclass(slots=True)
class Memory:
    falling: list[Position]
    first_batch: int
    end: Position

    @classmethod
    def parse(cls, lines: Iterator[str]) -> Memory:
        ext, fb = next(lines).split("/", maxsplit=2)
        extent = int(ext.strip())
        first_batch = int(fb.strip())

        _ = next(lines)

        falling: list[Position] = []
        for line in lines:
            fst, snd = line.split(",", maxsplit=2)
            falling.append(Position(int(fst), int(snd)))

        return Memory(falling, first_batch, Position.splat(extent - 1))

    def find_path(self, blocks: set[Position]) -> tuple[int, set[Position]]:
        known = {ORIGIN} | blocks
        queue: PriorityQueue[tuple[int, Position, set[Position]]] = PriorityQueue()
        queue.put((0, ORIGIN, {ORIGIN}))
        while not queue.empty():
            steps, position, path = queue.get()
            if position == self.end:
                return steps, path

            for next in position.unit_neighbors():
                if next in known or not next.is_within(ORIGIN, self.end):
                    continue

                known.add(next)
                queue.put((steps + 1, next, path | {next}))
        raise PathNotFoundException("No path found")

    def find_block_coords(self) -> Position:
        blocks = set(self.falling[: self.first_batch])
        path: set[Position] | None = None
        for next in self.falling[self.first_batch :]:
            try:
                blocks.add(next)
                if path is None or next in path:
                    _, path = self.find_path(blocks)
            except PathNotFoundException:
                return next
        raise Exception("no ultimately blocking block found")


def part1(lines: Iterator[str]) -> int:
    memory = Memory.parse(lines)
    blocks = set(memory.falling[: memory.first_batch])
    value, _ = memory.find_path(blocks)
    return value


def part2(lines: Iterator[str]) -> str:
    memory = Memory.parse(lines)
    last = memory.find_block_coords()
    return f"{str(last.x)},{str(last.y)}"
