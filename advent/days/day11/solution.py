from __future__ import annotations

from dataclasses import dataclass
from math import log10
from typing import Iterator

day_num = 11


@dataclass(frozen=True, slots=True)
class Stones:
    stones: dict[int, int]

    @classmethod
    def parse(cls, lines: Iterator[str]) -> Stones:
        stones: dict[int, int] = {}
        for stone in next(lines).split():
            s = int(stone)
            stones[s] = stones.get(s, 0) + 1
        return Stones(stones)

    def count(self) -> int:
        return sum(self.stones.values())

    def blink(self) -> Stones:
        stones: dict[int, int] = {}
        for stone, count in self.stones.items():
            if stone == 0:
                stones[1] = stones.get(1, 0) + count
            else:
                length = int(log10(stone)) + 1
                if length % 2 == 0:
                    first, second = divmod(stone, 10 ** (length // 2))
                    stones[first] = stones.get(first, 0) + count
                    stones[second] = stones.get(second, 0) + count
                else:
                    new_value = stone * 2024
                    stones[new_value] = stones.get(new_value, 0) + count
        return Stones(stones)

    def multi_blink(self, times: int) -> Stones:
        runner = self

        for _ in range(times):
            runner = runner.blink()
        return runner


def part1(lines: Iterator[str]) -> int:
    stones = Stones.parse(lines)
    return stones.multi_blink(25).count()


def part2(lines: Iterator[str]) -> int:
    stones = Stones.parse(lines)
    return stones.multi_blink(75).count()
