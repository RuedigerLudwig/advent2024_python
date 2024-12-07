from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

from advent.common.position import Position

day_num = 4

deltas = [
    Position(1, -1),
    Position(-1, -1),
    Position(-1, 1),
    Position(1, 1),
    Position(1, 0),
    Position(0, -1),
    Position(-1, 0),
    Position(0, 1),
]


@dataclass(frozen=True, slots=True)
class Xmas:
    data: list[str]

    @classmethod
    def parse(cls, lines: Iterator[str]) -> Xmas:
        data = list(lines)
        assert not not data
        return Xmas(data)

    def get(self, pos: Position) -> str | None:
        if 0 <= pos.y < len(self.data):
            row = self.data[pos.y]
            if 0 <= pos.x < len(row):
                return row[pos.x]
        return None

    def count_straight(self, start: Position, word: str) -> int:
        match_count = 0
        for delta in deltas:
            step = start
            does_match = True
            for letter in word:
                step += delta
                if self.get(step) != letter:
                    does_match = False
                    break

            if does_match:
                match_count += 1
        return match_count

    def find_xmas(self) -> int:
        first = "X"
        rest = "MAS"
        result = 0
        for y, row in enumerate(self.data):
            for x, ch in enumerate(row):
                if ch == first:
                    result += self.count_straight(Position(x, y), rest)
        return result

    def count_cross(self, start: Position) -> bool:
        count = 0
        for delta in deltas[:4]:
            if self.get(start + delta) == "M" and self.get(start - delta) == "S":
                count += 1
                if count == 2:
                    return True
        return False

    def find_x_mas(self) -> int:
        first = "A"
        result = 0
        for y, row in enumerate(self.data[1:-1], 1):
            for x, ch in enumerate(row[1:-1], 1):
                if ch == first and self.count_cross(Position(x, y)):
                    result += 1
        return result


def part1(lines: Iterator[str]) -> int:
    return Xmas.parse(lines).find_xmas()


def part2(lines: Iterator[str]) -> int:
    return Xmas.parse(lines).find_x_mas()
