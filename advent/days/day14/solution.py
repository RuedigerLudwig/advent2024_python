from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from itertools import  count, pairwise
from math import prod
from collections.abc import Callable

from advent.common.position import Position

day_num = 14

def get_position(line: str) -> Position:
    x,y = line.strip()[2:].split(",")
    return Position(int(x), int(y))

@dataclass(slots=True)
class Robot:
    position: Position
    velocity: Position

    @classmethod
    def parse(cls, line: str) -> Robot:
        p, v = line.split(" ", maxsplit=2)
        return Robot(get_position(p), get_position(v))


@dataclass(slots=True)
class Bathroom:
    extent:Position
    robots: list[Robot]

    @classmethod
    def parse(cls, lines: Iterator[str]) -> Bathroom:
        extent = get_position(next(lines))
        robots = [Robot.parse(line) for line in lines]
        return Bathroom(extent, robots)

    def animate(self, times: int):
        for _ in range(times):
            for robot in self.robots:
                robot.position += robot.velocity
                robot.position = Position(robot.position.x % self.extent.x, robot.position.y % self.extent.y)


    def get_value(self) -> int:
        q1, q2, q3, q4 = 0, 0, 0, 0
        mx = self.extent.x // 2
        my = self.extent.y // 2
        for robot in self.robots:
            if robot.position.x < mx:
                if robot.position.y < my:
                    q1 += 1
                elif robot.position.y > my:
                    q2 += 1
            elif robot.position.x > mx:
                if robot.position.y < my:
                    q3 += 1
                elif robot.position.y > my:
                    q4 += 1
        return prod([q1, q2, q3, q4])

    def check(self, component: Callable[[Position], int]) -> bool:
        lst = [0] * component(self.extent)
        expected = len(self.robots) // len(lst) * 4
        for robot in self.robots:
            lst[component(robot.position)] += 1
        return any(True for a,b in pairwise(lst) if abs(a-b) > expected)


    def check_horiz(self) -> bool:
        return self.check(lambda p: p.y)

    def check_vert(self) -> bool:
        return self.check(lambda p: p.x)

    def print(self):
        for y in range(self.extent.y):
            for x in range(self.extent.x):
                pos = Position(x, y)
                count = sum(1 for robot in self.robots if robot.position == pos)
                if 0 < count <= 9:
                    print(f"{count}", end="")
                elif count > 9:
                    print("*", end="")
                else:
                    print(".", end="")
            print()

def part1(lines: Iterator[str]) -> int:
    bath = Bathroom.parse(lines)
    bath.animate(100)
    return bath.get_value()


def part2(lines: Iterator[str]) -> int:
    bath = Bathroom.parse(lines)
    v_start = None
    v_diff = None
    h_start = None
    h_diff = None
    for n in count(start=1):
        bath.animate(1)
        if bath.check_horiz():
            if h_start is None:
                h_start = n
            elif h_diff is None:
                h_diff = n - h_start
            else:
                assert h_diff == (n - h_start) // 2
        if bath.check_vert():
            if v_start is None:
                v_start = n
            elif v_diff is None:
                v_diff = n - v_start
            else:
                assert v_diff == (n - v_start) // 2
        if v_diff is not None and h_diff is not None:
            break

    assert h_start is not None and  h_diff is not None and  v_start is not None and v_diff is not None

    diff = (h_start - v_start) / v_diff
    quot = h_diff / v_diff
    for n in count(start=1):
        result = n * quot + diff
        if result % 1 == 0:
            return h_diff * n + h_start

    return 0