from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from collections.abc import Callable

from advent.common.position import Direction, Position

day_num = 12

Fence = tuple[tuple[int, int], int]


@dataclass(frozen=True, slots=True)
class Garden:
    patches: list[str]

    @classmethod
    def parse(cls, lines: Iterator[str]) -> Garden:
        patches = list(lines)
        return Garden(patches)

    def get(self, pos: Position) -> str | None:
        if 0 <= pos.y < len(self.patches) and 0 <= pos.x < len(self.patches[pos.y]):
            return self.patches[pos.y][pos.x]
        return None

    @staticmethod
    def fence_key(pos: Position, dir: Direction) -> Fence:
        match dir:
            case Direction.East | Direction.West:
                return (dir.value, pos.x), pos.y
            case Direction.North | Direction.South:
                return (dir.value, pos.y), pos.x

    def value_patch(
        self, start: Position
    ) -> tuple[set[Position], list[Fence], set[Position]]:
        to_be_checked = {start}
        patch = {start}
        perimeter: list[Fence] = []
        flower = self.patches[start.y][start.x]
        neighbors: set[Position] = set()
        while to_be_checked:
            current = to_be_checked.pop()
            for direction in Direction:
                next = current + direction.as_position()
                if next in patch:
                    continue
                next_flower = self.get(next)
                if next_flower != flower:
                    perimeter.append(Garden.fence_key(next, direction))
                    if next_flower is not None:
                        neighbors.add(next)
                    continue
                patch.add(next)
                to_be_checked.add(next)
        return patch, perimeter, neighbors

    def find_price(self, value_perimeter: Callable[[list[Fence]], int]):
        visited: set[Position] = set()
        unknown = {Position(0, 0)}
        value = 0
        while unknown:
            current = unknown.pop()
            patch, perimeter, neighbors = self.value_patch(current)
            value += len(patch) * value_perimeter(perimeter)
            visited |= patch
            unknown = (unknown | neighbors) - visited
        return value


def part1(lines: Iterator[str]) -> int:
    garden = Garden.parse(lines)
    return garden.find_price(lambda p: len(p))


def count_fences(perimeter: list[Fence]) -> int:
    perimeter.sort()

    return 1 + sum(
        1
        for (fence1, pos1), (fence2, pos2) in zip(perimeter, perimeter[1:])
        if fence1 != fence2 or abs(pos1 - pos2) != 1
    )


def part2(lines: Iterator[str]) -> int:
    garden = Garden.parse(lines)
    return garden.find_price(count_fences)
