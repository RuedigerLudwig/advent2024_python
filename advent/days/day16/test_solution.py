from advent.common import input

from .solution import Maze, day_num, part1, part2


def test_part1():
    lines = input.read_lines(day_num, "example01.txt")
    expected = 7036
    result = part1(lines)
    assert result == expected


def test_part2():
    lines = input.read_lines(day_num, "example01.txt")
    expected = 45
    result = part2(lines)
    assert result == expected


def test_example01():
    lines = input.read_lines(day_num, "example01.txt")
    maze = Maze.parse(lines)
    value, seats = maze.solve()
    assert value == 7036
    assert len(seats) == 45


def test_example02():
    lines = input.read_lines(day_num, "example02.txt")
    maze = Maze.parse(lines)
    value, seats = maze.solve()
    assert value == 11048
    assert len(seats) == 64
