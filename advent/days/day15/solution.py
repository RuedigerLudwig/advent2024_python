from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from enum import Enum
from typing import Self

from advent.common.position import Direction, Position

day_num = 15


class Tile(Enum):
    Empty = 0
    Box = 1
    BoxRight = 2
    Wall = 3


@dataclass(slots=True)
class GoodsStore:
    map: list[list[Tile]]
    moves: list[Direction]
    robot: Position

    @classmethod
    def parse_tile(cls, tile: str) -> Iterator[Tile]: ...

    def push(self, position: Position, direction: Position): ...

    @staticmethod
    def parse_move(char: str) -> Direction:
        match char:
            case ">":
                return Direction.East
            case "^":
                return Direction.North
            case "<":
                return Direction.West
            case "v":
                return Direction.South
            case _:
                raise Exception(f"Unknown Move: {char}")

    @classmethod
    def parse(cls, lines: Iterator[str]) -> Self:
        map: list[list[Tile]] = []
        robot: Position | None = None
        while line := next(lines):
            map_row: list[Tile] = []
            for block in line:
                if block == "@":
                    robot = Position(len(map_row), len(map))
                map_row.extend(cls.parse_tile(block))

            map.append(map_row)

        moves = [cls.parse_move(move) for line in lines for move in line]

        assert robot is not None
        return cls(map, moves, robot)

    def step(self, dir: Direction):
        direction = dir.as_position()
        next_pos = self.robot + direction
        match  self.map[next_pos.y][next_pos.x]:
            case Tile.Empty:
                self.robot = next_pos
            case Tile.Box | Tile.BoxRight:
                self.push(next_pos, direction)
            case Tile.Wall:
                pass

    def walk(self):
        for move in self.moves:
            self.step(move)

    def get_gps_value(self) -> int:
        sum = 0
        for y, row in enumerate(self.map):
            for x, block in enumerate(row):
                if block is Tile.Box:
                    sum += 100 * y + x
        return sum


@dataclass(slots=True)
class SmallGoods(GoodsStore):
    @classmethod
    def parse_tile(cls, tile: str) -> Iterator[Tile]:
        match tile:
            case "#":
                yield Tile.Wall
            case "O":
                yield Tile.Box
            case _:
                yield Tile.Empty

    def push(self, position: Position, direction: Position):
        next_check = position + direction
        while self.map[next_check.y][next_check.x] == Tile.Box:
            next_check += direction

        if self.map[next_check.y][next_check.x] == Tile.Empty:
            self.map[next_check.y][next_check.x] = Tile.Box
            self.map[position.y][position.x] = Tile.Empty
            self.robot = position


@dataclass(slots=True)
class LargeGoods(GoodsStore):
    @classmethod
    def parse_tile(cls, tile: str) -> Iterator[Tile]:
        match tile:
            case "#":
                yield Tile.Wall
                yield Tile.Wall
            case "O":
                yield Tile.Box
                yield Tile.BoxRight
            case _:
                yield Tile.Empty
                yield Tile.Empty

    def push_horizontal(self, pos: Position, direction: Position):
        check_pos = pos
        while self.map[check_pos.y][check_pos.x] in [Tile.Box, Tile.BoxRight]:
            check_pos += direction

        if self.map[check_pos.y][check_pos.x] == Tile.Empty:
            while check_pos != pos:
                next = check_pos - direction
                self.map[check_pos.y][check_pos.x] = self.map[next.y][next.x]
                check_pos = next
            self.map[pos.y][pos.x] = Tile.Empty
            self.robot = pos

    def push_vertical(self, pos: Position, direction: Position):
        push_row: list[set[int]] = []
        if self.map[pos.y][pos.x] == Tile.Box:
            push_row.append({pos.x, pos.x + 1})
        else:
            push_row.append({pos.x - 1, pos.x})

        check_y = pos.y
        finished = False
        while not finished:
            check_y += direction.y
            next_blocks: set[int] = set()
            pushing_blocks = push_row[-1]
            for block_x in pushing_blocks:
                match self.map[check_y][block_x]:
                    case Tile.Wall:
                        # We hit any wall: This must mean a full stop
                        return

                    case Tile.Empty:
                        pass

                    case Tile.Box:
                        next_blocks |= {block_x, block_x + 1}

                    case Tile.BoxRight:
                        next_blocks |= {block_x - 1, block_x}

            if next_blocks:
                push_row.append(next_blocks)
            else:
                finished = True

        while push_row:
            pushed_row = push_row.pop()
            from_y = check_y - direction.y
            for block_x in pushed_row:
                self.map[check_y][block_x] = self.map[from_y][block_x]
                self.map[from_y][block_x] = Tile.Empty
            check_y = from_y
        self.robot = pos

    def push(self, position: Position, direction: Position):
        if direction.y == 0:
            self.push_horizontal(position, direction)
        else:
            self.push_vertical(position, direction)


def part1(lines: Iterator[str]) -> int:
    goods = SmallGoods.parse(lines)
    goods.walk()
    return goods.get_gps_value()


def part2(lines: Iterator[str]) -> int:
    goods = LargeGoods.parse(lines)
    goods.walk()
    return goods.get_gps_value()
