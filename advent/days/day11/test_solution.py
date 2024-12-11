from advent.common import input

from .solution import Stones, day_num, part1


def test_part1():
    lines = input.read_lines(day_num, "example01.txt")
    expected = 55312
    result = part1(lines)
    assert result == expected


def test_part2():
    assert True


def test_multi_blink():
    lines = input.read_lines(day_num, "example01.txt")
    stones = Stones.parse(lines)
    assert stones.multi_blink(6).count() == 22
