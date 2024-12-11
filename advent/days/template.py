from collections.abc import Iterator
from typing import Any, Protocol, TypeGuard

ResultType = int | str | list[str]


class Day(Protocol):
    day_num: int

    @staticmethod
    def part1(lines: Iterator[str]) -> ResultType | None: ...

    @staticmethod
    def part2(lines: Iterator[str]) -> ResultType | None: ...


def is_day(object: Any) -> TypeGuard[Day]:
    try:
        return (
            isinstance(object.day_num, int)
            and callable(object.part1)
            and callable(object.part2)
        )
    except AttributeError:
        return False
