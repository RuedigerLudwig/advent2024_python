from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Iterator

from advent.common.position import Position

day_num = 6


class LoopException(Exception):
    pass


@dataclass(frozen=True, slots=True)
class Map:
    extent: Position
    obs_in_rows: list[list[int]]
    obs_in_cols: list[list[int]]
    start: Position
    facing: Position

    @classmethod
    def parse(cls, lines: Iterator[str]) -> Map:
        obstacles: set[Position] = set()
        start: Position | None = None
        facing: Position | None = None
        for row, line in enumerate(lines):
            for col, field in enumerate(line):
                match field:
                    case "#":
                        obstacles.add(Position(col, row))
                    case "^":
                        start = Position(col, row)
                        facing = Position(0, -1)
                    case _:
                        pass
                col += 1
            row += 1

        assert start is not None
        assert facing is not None

        extent = Position.component_max(*obstacles)
        extent += Position(1, 1)

        obs_in_rows: list[list[int]] = [[] for _ in range(extent.y)]
        obs_in_cols: list[list[int]] = [[] for _ in range(extent.x)]
        for ob in obstacles:
            obs_in_rows[ob.y].append(ob.x)
            obs_in_cols[ob.x].append(ob.y)

        for row in obs_in_rows:
            row.sort()
        for col in obs_in_cols:
            col.sort()

        return Map(extent, obs_in_rows, obs_in_cols, start, facing)

    @staticmethod
    def turn_right(facing: Position) -> Position:
        return Position(-facing.y, facing.x)

    def in_area(self, pos: Position) -> bool:
        return 0 <= pos.x < self.extent.x and 0 <= pos.y < self.extent.y

    def do_steps(self, position: Position, facing: Position) -> tuple[Position, bool]:
        if facing.x == 0:
            if facing.y > 0:
                for row in self.obs_in_cols[position.x]:
                    if row > position.y:
                        return Position(position.x, row - 1), True
                return Position(position.x, self.extent.y), False
            else:
                for row in reversed(self.obs_in_cols[position.x]):
                    if row < position.y:
                        return Position(position.x, row + 1), True
                return Position(position.x, -1), False
        elif facing.x > 0:
            for col in self.obs_in_rows[position.y]:
                if col > position.x:
                    return Position(col - 1, position.y), True
            return Position(self.extent.x, position.y), False

        for col in reversed(self.obs_in_rows[position.y]):
            if col < position.x:
                return Position(col + 1, position.y), True
        return Position(-1, position.y), False

    def walk(self) -> set[Position]:
        visited = {self.start}
        been_before = {(self.start, self.facing)}
        facing = self.facing
        position = self.start
        while True:
            next_position, in_area = self.do_steps(position, facing)
            while position != next_position:
                visited.add(position)
                position += facing
            if not in_area:
                return visited

            facing = Map.turn_right(facing)

            if (position, facing) in been_before:
                raise LoopException
            been_before.add((position, facing))

    def add_obstacle(self, start: Position, facing: Position) -> Map:
        obs_in_cols = self.obs_in_cols.copy()
        obstacle = start + facing
        curr_col = obs_in_cols[obstacle.x].copy()
        added = False
        for pos, val in enumerate(curr_col):
            if val > obstacle.y:
                added = True
                curr_col.insert(pos, obstacle.y)
                break
        if not added:
            curr_col.append(obstacle.y)
        obs_in_cols[obstacle.x] = curr_col

        obs_in_rows = self.obs_in_rows.copy()
        curr_row = obs_in_rows[obstacle.y].copy()
        added = False
        for pos, val in enumerate(curr_row):
            if val > obstacle.x:
                added = True
                curr_row.insert(pos, obstacle.x)
                break
        if not added:
            curr_row.append(obstacle.x)
        obs_in_rows[obstacle.y] = curr_row

        return Map(self.extent, obs_in_rows, obs_in_cols, start, Map.turn_right(facing))

    def is_obstacle(self, position: Position) -> bool:
        return position.x in self.obs_in_rows[position.y]

    def loop_guard(self) -> int:
        added = 0
        checked: set[Position] = set()
        facing = self.facing
        position = self.start
        while True:
            next_position = position + facing
            if not self.in_area(next_position):
                return added
            elif self.is_obstacle(next_position):
                facing = Map.turn_right(facing)
            else:
                if next_position not in checked:
                    loop_map = self.add_obstacle(position, facing)
                    try:
                        loop_map.walk()
                    except LoopException:
                        added += 1
                    checked.add(next_position)
                position = next_position


def part1(lines: Iterator[str]) -> int:
    map = Map.parse(lines)
    return len(map.walk())


def part2(lines: Iterator[str]) -> int:
    map = Map.parse(lines)
    return map.loop_guard()
