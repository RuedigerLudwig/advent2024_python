from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Iterator

day_num = 1


@dataclass(frozen=True, slots=True)
class Data:
    first: list[int]
    second: list[int]

    @classmethod
    def parse(cls, lines: Iterator[str]) -> Data:
        first, second = zip(
            *((int(a), int(b)) for (a, b) in (line.split(maxsplit=2) for line in lines))
        )

        return Data(first, second)

    def differences(self) -> int:
        return sum(abs(a - b) for a, b in zip(sorted(self.first), sorted(self.second)))

    def similarity(self) -> int:
        occur: dict[int, int] = {}
        for b in self.second:
            occur[b] = occur.get(b, 0) + 1
        return sum(a * occur.get(a, 0) for a in self.first)


def part1(lines: Iterator[str]) -> int:
    data = Data.parse(lines)
    return data.differences()


def part2(lines: Iterator[str]) -> int:
    data = Data.parse(lines)
    return data.similarity()
