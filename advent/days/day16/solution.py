from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from queue import PriorityQueue

from advent.common.position import Direction, Position

day_num = 16


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

    def walk(self) -> int:
        known: dict[Position, int] = {}
        queue: PriorityQueue[tuple[int, Position, Direction]] = PriorityQueue()
        queue.put((0, self.start, Direction.East))
        while not queue.empty():
            value, position, direction = queue.get()
            if position == self.end:
                return value
            prev_value = known.get(position)
            if prev_value is not None and prev_value <= value:
                continue
            known[position] = value
            for next_dir in Direction:
                if next_dir == direction.reverse():
                    continue
                next_pos = position + next_dir.as_position()
                if next_pos not in self.path:
                    continue
                if next_dir == direction:
                    queue.put((value + 1, next_pos, next_dir))
                else:
                    queue.put((value + 1001, next_pos, next_dir))
        raise Exception("No path found")

    def sit_down_(self) -> int:
        known: dict[tuple[Position, Direction], tuple[int, set[Position]]] = {
            (self.start, Direction.East): (0, {self.start})
        }
        queue = {(self.start, Direction.East)}
        while queue:
            min_item = None
            min_value = None
            for pos in queue:
                value, _ = known[pos]
                if min_value is None or min_value >= value:
                    min_value = value
                    min_item = pos
            assert min_item is not None
            queue.remove(min_item)
            value, path = known[min_item]
            position, direction = min_item

            if position == self.end:
                return len(path)
            for next_dir in Direction:
                if next_dir == direction:
                    next_pos = position + next_dir.as_position()
                    if next_pos not in self.path or next_pos in path:
                        continue
                    new_path = path.copy()
                    new_path.add(position)
                    queue.put((value + 1, next_pos, next_dir, new_path))
                elif next_dir != direction.reverse():
                    queue.put((value + 1001, next_pos, next_dir, new_path))

        for row in range(self.start.y + 2):
            for col in range(self.end.x + 2):
                pos = Position(col, row)
                if pos in best:
                    print("O", end="")
                elif pos in self.path:
                    print(".", end="")
                else:
                    print("#", end="")
            print()

        return len(best)


def part1(lines: Iterator[str]) -> int:
    maze = Maze.parse(lines)
    return maze.walk()


def part2(lines: Iterator[str]) -> int:
    maze = Maze.parse(lines)
    return maze.sit_down()
