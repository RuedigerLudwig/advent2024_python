from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass

from advent.common.position import Direction, Position

day_num = 16

PosDir = tuple[Position, Direction]


@dataclass(slots=True)
class Maze:
    path: set[Position]
    start: Position
    end: Position

    @classmethod
    def parse(cls, lines: Iterator[str]) -> Maze:
        start: Position | None = None
        end: Position | None = None
        path: set[Position] = set()
        for row, line in enumerate(lines):
            for col, tile in enumerate(line):
                match tile:
                    case "S":
                        start = Position(col, row)
                        path.add(start)
                    case "E":
                        end = Position(col, row)
                        path.add(end)
                    case ".":
                        path.add(Position(col, row))
                    case _:
                        pass

        assert start is not None and end is not None
        return Maze(path, start, end)

    @staticmethod
    def check_add(
        known: dict[PosDir, tuple[int, set[Position]]],
        pos_dir: PosDir,
        value: int,
        path: set[Position],
    ) -> bool:
        prev = known.get((pos_dir))
        if prev is not None:
            prev_value, prev_path = prev
            if prev_value < value:
                return False
            elif prev_value == value:
                known[pos_dir] = value, prev_path | path
                return True

        known[pos_dir] = value, path
        return True

    def solve(self) -> tuple[int, set[Position]]:
        known = {(self.start, Direction.East): (0, {self.start})}
        queue = {(self.start, Direction.East)}
        while queue:
            min_item = min(queue, key=lambda pd: known[pd][0])
            queue.remove(min_item)

            position, direction = min_item
            if position == self.end:
                return known[min_item]

            value, path = known[min_item]
            next_pos = position + direction.as_position()
            if next_pos in self.path and next_pos not in path:
                new_path = path | {next_pos}
                if Maze.check_add(known, (next_pos, direction), value + 1, new_path):
                    queue.add((next_pos, direction))

            left = direction.turn_left()
            if (position + left.as_position()) in self.path:
                if Maze.check_add(known, (position, left), value + 1000, path):
                    queue.add((position, left))

            right = direction.turn_right()
            if (position + right.as_position()) in self.path:
                if Maze.check_add(known, (position, right), value + 1000, path):
                    queue.add((position, right))

        raise Exception("No Path found")


def part1(lines: Iterator[str]) -> int:
    maze = Maze.parse(lines)
    value, _ = maze.solve()
    return value


def part2(lines: Iterator[str]) -> int:
    maze = Maze.parse(lines)
    _, seats = maze.solve()
    return len(seats)
