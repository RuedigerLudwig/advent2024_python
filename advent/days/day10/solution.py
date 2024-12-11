from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from collections.abc import Iterator

from advent.common.position import Position

day_num = 10


@dataclass(frozen=True, slots=True)
class Trail:
    map: list[list[int]]

    @classmethod
    def parse(cls, lines: Iterator[str]) -> Trail:
        map = [[int(height) for height in line] for line in lines]
        return Trail(map)

    def get_all_at_height(self, look_for: int) -> Iterator[Position]:
        for y, row in enumerate(self.map):
            for x, height in enumerate(row):
                if height == look_for:
                    yield Position(x, y)

    def get_position(self, pos: Position) -> int | None:
        if 0 <= pos.y < len(self.map) and 0 <= pos.x < len(self.map[pos.y]):
            return self.map[pos.y][pos.x]
        return None

    def walk(self) -> int:
        path_count = 0
        for trailhead in self.get_all_at_height(0):
            visited: set[Position] = set()
            to_test: deque[tuple[Position, int]] = deque()
            to_test.append((trailhead, 0))
            while to_test:
                current_pos, current_height = to_test.pop()
                for next_pos in current_pos.unit_neighbors():
                    if next_pos in visited:
                        continue

                    next_height = self.get_position(next_pos)
                    if next_height is None or next_height != current_height + 1:
                        continue

                    visited.add(next_pos)
                    if next_height == 9:
                        path_count += 1
                        continue

                    to_test.appendleft((next_pos, next_height))

        return path_count

    def distinct(self) -> int:
        path_count = 0
        to_test = deque((p, 0) for p in self.get_all_at_height(0))
        while to_test:
            current_pos, current_height = to_test.pop()
            for next_pos in current_pos.unit_neighbors():
                next_height = self.get_position(next_pos)
                if next_height is None or next_height != current_height + 1:
                    continue

                if next_height == 9:
                    path_count += 1
                    continue

                to_test.appendleft((next_pos, next_height))
        return path_count


def part1(lines: Iterator[str]) -> int:
    trail = Trail.parse(lines)
    return trail.walk()


def part2(lines: Iterator[str]) -> int:
    trail = Trail.parse(lines)
    return trail.distinct()
