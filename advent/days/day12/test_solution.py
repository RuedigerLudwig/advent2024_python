from advent.common import input
from advent.common.position import Position

from .solution import Garden, day_num, part1, part2


def test_part1():
    lines = input.read_lines(day_num, "example01.txt")
    expected = 1930
    result = part1(lines)
    assert result == expected


def test_part2():
    lines = input.read_lines(day_num, "example01.txt")
    expected = 1206
    result = part2(lines)
    assert result == expected


def test_walk_a():
    lines = input.read_lines(day_num, "example02.txt")
    patch, fences, neighbors = Garden.parse(lines).value_patch(Position(2, 1))
    assert len(patch) == 4
    assert len(fences) == 10
    assert len(neighbors) == 5


def test_value_small():
    lines = input.read_lines(day_num, "example02.txt")
    garden = Garden.parse(lines)
    assert garden.find_price(lambda p: len(p)) == 140
