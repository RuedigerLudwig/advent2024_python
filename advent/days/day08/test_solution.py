from advent.common import input

from .solution import day_num, part1, part2


def test_part1():
    lines = input.read_lines(day_num, "example01.txt")
    expected = 14
    result = part1(lines)
    assert result == expected


def test_part2():
    lines = input.read_lines(day_num, "example01.txt")
    expected = 34
    result = part2(lines)
    assert result == expected