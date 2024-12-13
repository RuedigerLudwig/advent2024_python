from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass

from advent.common.position import Position

day_num = 13


@dataclass(slots=True, frozen=True)
class Machine:
    button_a: Position
    button_b: Position
    prize: Position

    @classmethod
    def parse_position(cls, line: str) -> Position:
        _, values = line.split(":", maxsplit=2)
        x_str, y_str = values.split(",")
        x = int(x_str.strip()[2:])
        y = int(y_str.strip()[2:])
        return Position(x, y)

    @classmethod
    def parse_one(cls, lines: Iterator[str]) -> Machine | None:
        try:
            button_a = Machine.parse_position(next(lines))
        except StopIteration:
            return None
        button_b = Machine.parse_position(next(lines))
        prize = Machine.parse_position(next(lines))
        try:
            _ = next(lines)
        except StopIteration:
            pass
        return Machine(button_a, button_b, prize)

    @classmethod
    def parse(cls, lines: Iterator[str]) -> Iterator[Machine]:
        while machine := Machine.parse_one(lines):
            yield machine

    def win_prize(self, added: int = 0, max_pushes: int | None = 100) -> int | None:
        prize = self.prize + Position.splat(added)
        temp_1 = self.button_a.x * self.button_b.y - self.button_a.y * self.button_b.x
        if temp_1 == 0:
            return None
        temp_2 = self.button_a.x * prize.y - self.button_a.y * prize.x

        pushes_b = temp_2 / temp_1
        if (
            pushes_b % 1 != 0
            or pushes_b <= 0
            or (max_pushes is not None and pushes_b > max_pushes)
        ):
            return None

        pushes_a = (prize.x - self.button_b.x * pushes_b) / self.button_a.x
        if max_pushes is not None and pushes_a > max_pushes:
            return None

        return int(pushes_a * 3 + pushes_b)


def part1(lines: Iterator[str]) -> int:
    return sum(
        prize
        for machine in Machine.parse(lines)
        if (prize := machine.win_prize()) is not None
    )


def part2(lines: Iterator[str]) -> int:
    return sum(
        prize
        for machine in Machine.parse(lines)
        if (prize := machine.win_prize(10_000_000_000_000, None)) is not None
    )
