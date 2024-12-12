from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from collections.abc import Callable

from advent.common.position import Direction, Position

day_num = 12

Fence = tuple[Position, Direction]


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

    def value_patch(
        self, start: Position
    ) -> tuple[str, list[Fence], set[Position], set[Position]]:
        to_be_checked = {start}
        patch = {start}
        perimeter: list[Fence] = []
        flower = self.get(start)
        assert flower is not None
        neighbors: set[Position] = set()
        while to_be_checked:
            current = to_be_checked.pop()
            for direction in Direction:
                next = current + direction.as_position()
                next_flower = self.get(next)
                if next_flower is None:
                    perimeter.append((next, direction))
                    continue
                if next_flower != flower:
                    perimeter.append((next, direction))
                    neighbors.add(next)
                    continue
                if next in patch:
                    continue
                patch.add(next)
                to_be_checked.add(next)
        return flower, perimeter, patch, neighbors

    def find_price(self, value_perimeter: Callable[[list[Fence]], int]):
        visited: set[Position] = set()
        unknown = {Position(0, 0)}
        value = 0
        while unknown:
            current = unknown.pop()
            _, perimeter, patch, neighbors = self.value_patch(current)
            peri_val = value_perimeter(perimeter)
            # print(f"{flower}:  {len(patch)} * {peri_val}")
            value += peri_val * len(patch)
            visited |= patch
            unknown = (unknown | neighbors) - visited
        return value


def part1(lines: Iterator[str]) -> int:
    garden = Garden.parse(lines)
    return garden.find_price(lambda p: len(p))


def fence_key(fence: Fence):
    match fence[1]:
        case Direction.East:
            return 1, fence[0].x, fence[0].y, fence
        case Direction.West:
            return 2, fence[0].x, fence[0].y, fence
        case Direction.North:
            return 3, fence[0].y, fence[0].x, fence
        case Direction.South:
            return 4, fence[0].y, fence[0].x, fence


def straight_perimeter(perimeter: list[Fence]) -> int:
    peri = [fence_key(p) for p in perimeter]
    peri = sorted(peri)

    value = 1
    ldir, lfst, lsnd, _ = peri[0]
    for cdir, cfst, csnd, _ in peri[1:]:
        if cdir != ldir or cfst != lfst or abs(csnd - lsnd) != 1:
            value += 1
        ldir = cdir
        lfst = cfst
        lsnd = csnd

    return value


def part2(lines: Iterator[str]) -> int:
    garden = Garden.parse(lines)
    return garden.find_price(straight_perimeter)
