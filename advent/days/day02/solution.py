from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

day_num = 2


@dataclass(slots=True, frozen=True)
class Report:
    data: list[int]

    @classmethod
    def parse(cls, line: str) -> Report:
        return Report([int(number) for number in line.split()])

    @staticmethod
    def cmp(f: int, s: int) -> bool:
        return f < s <= f + 3

    @staticmethod
    def check(a: int, b: int, direction: bool | None) -> tuple[bool, bool | None]:
        match direction:
            case None:
                if Report.cmp(a, b):
                    return True, True
                elif Report.cmp(b, a):
                    return True, False
                else:
                    return False, direction

            case True:
                if not Report.cmp(a, b):
                    return False, direction
            case False:
                if not Report.cmp(b, a):
                    return False, direction
        return True, direction

    def is_safe(self) -> bool:
        direction: bool | None = None
        for a, b in zip(self.data, self.data[1:]):
            result, direction = Report.check(a, b, direction)
            if not result:
                return False
        return True

    @staticmethod
    def cmp2(f: int, s: int) -> bool | None:
        if f < s:
            if s <= f + 3:
                return True
        elif s < f:
            if f <= s + 3:
                return False
        return None

    def is_safe_damped_(self) -> bool:
        if self.is_safe():
            return True

        for i in range(len(self.data)):
            lst = self.data.copy()
            del lst[i]
            if Report(lst).is_safe():
                return True
        return False

    def is_safe_damped(self) -> bool:
        def check(first: int, data: list[int], direction: bool, dumped: bool) -> bool:
            for second in data:
                if Report.cmp2(first, second) != direction:
                    if dumped:
                        return False
                    dumped = True
                else:
                    first = second
            return True

        first, second = self.data[0], self.data[1]
        if (direction := Report.cmp2(first, second)) is not None:
            if check(second, self.data[2:], direction, False):
                return True

        third = self.data[2]

        if (direction := Report.cmp2(first, third)) is not None:
            if check(third, self.data[3:], direction, True):
                return True

        direction = Report.cmp2(second, third)
        if direction is None:
            return False

        return check(third, self.data[3:], direction, True)


def part1(lines: Iterator[str]) -> int:
    return sum(1 for line in lines if Report.parse(line).is_safe())


def part2(lines: Iterator[str]) -> int:
    return sum(1 for line in lines if Report.parse(line).is_safe_damped())
