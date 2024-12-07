from advent.common import input

from .solution import Equation, day_num, part1, part2


def test_part1():
    lines = input.read_lines(day_num, "example01.txt")
    expected = 3749
    result = part1(lines)
    assert result == expected


def test_part2():
    lines = input.read_lines(day_num, "example01.txt")
    expected = 11387
    result = part2(lines)
    assert result == expected


def test_three():
    assert Equation.parse("7290: 6 8 6 15").is_valid_three()
    assert Equation.parse("192: 17 8 14").is_valid_three()
    assert Equation.parse("156: 15 6").is_valid_three()
