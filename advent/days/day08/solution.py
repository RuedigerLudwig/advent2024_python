from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from collections.abc import Iterator

from advent.common.position import Position

day_num = 8


@dataclass(frozen=True, slots=True)
class AntennaMap:
    extent: Position
    antenna: dict[str, list[Position]]

    @classmethod
    def parse(cls, lines: Iterator[str]) -> AntennaMap:
        antenna: dict[str, list[Position]] = {}
        extent = Position(0, 0)
        for row, line in enumerate(lines):
            if row > extent.y:
                extent = extent.set_y(row)
            for col, tile in enumerate(line):
                if col > extent.x:
                    extent = extent.set_x(col)

                if not tile.isalnum():
                    continue

                lst = antenna.get(tile)
                if lst is None:
                    lst = []
                lst.append(Position(col, row))
                antenna[tile] = lst
        return AntennaMap(extent, antenna)

    def get_antinodes(self) -> set[Position]:
        antinodes: set[Position] = set()
        for nodes in self.antenna.values():
            for node1, node2 in combinations(nodes, 2):
                diff = node1 - node2
                pos1 = node1 + diff
                if 0 <= pos1.x <= self.extent.x and 0 <= pos1.y <= self.extent.y:
                    antinodes.add(pos1)
                pos2 = node2 - diff
                if 0 <= pos2.x <= self.extent.x and 0 <= pos2.y <= self.extent.y:
                    antinodes.add(pos2)
        return antinodes

    def count_antinodes(self) -> int:
        return len(self.get_antinodes())

    def get_real_antinodes(self) -> set[Position]:
        antinodes: set[Position] = set()
        for nodes in self.antenna.values():
            for node1, node2 in combinations(nodes, 2):
                diff = node1 - node2
                pos1 = node1
                while 0 <= pos1.x <= self.extent.x and 0 <= pos1.y <= self.extent.y:
                    antinodes.add(pos1)
                    pos1 += diff
                pos2 = node2
                while 0 <= pos2.x <= self.extent.x and 0 <= pos2.y <= self.extent.y:
                    antinodes.add(pos2)
                    pos2 -= diff
        return antinodes

    def count_real_antinodes(self) -> int:
        return len(self.get_real_antinodes())


def part1(lines: Iterator[str]) -> int:
    return AntennaMap.parse(lines).count_antinodes()


def part2(lines: Iterator[str]) -> int:
    return AntennaMap.parse(lines).count_real_antinodes()
