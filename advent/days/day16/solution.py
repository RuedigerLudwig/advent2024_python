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
                    case '#':
                        pass
                    case _:
                        raise Exception(f"Unknown tile: {tile}")

        assert start is not None and end is not None
        return Maze(path, start, end)

    @staticmethod
    def check_add(
        known: dict[PosDir, tuple[int, set[Position]]],
        position: Position,
        direction: Direction,
        value: int,
        path: set[Position],
    ) -> bool:
        pos_dir = position, direction
        prev = known.get((pos_dir))
        if prev is not None:
            prev_value, prev_path = prev
            if prev_value < value:
                return False
            elif prev_value == value:
                prev_path.add(position)
                prev_path |= path
                return True

        known[pos_dir] = value, path | {position}
        return True

    def solve(self) -> tuple[int, set[Position]]:
        visited = {(self.start, Direction.East): (0, {self.start})}
        queue = {(self.start, Direction.East)}
        while queue:
            min_item = min(queue, key=lambda pd: visited[pd][0])
            queue.remove(min_item)

            position, direction = min_item
            if position == self.end:
                return visited[min_item]

            value, path = visited[min_item]

            for dir, added in [
                (direction, 1),
                (direction.turn_left(), 1_001),
                (direction.turn_right(), 1_001),
            ]:
                next_pos = position + dir.as_position()
                if next_pos in self.path and next_pos not in path:
                    if Maze.check_add(visited, next_pos, dir, value + added, path):
                        queue.add((next_pos, dir))

        raise Exception("No Path found")


def part1(lines: Iterator[str]) -> int:
    maze = Maze.parse(lines)
    value, _ = maze.solve()
    return value


def part2(lines: Iterator[str]) -> int:
    maze = Maze.parse(lines)
    _, seats = maze.solve()
    return len(seats)
