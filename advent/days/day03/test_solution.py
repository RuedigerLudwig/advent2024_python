from advent.common import input

from .solution import day_num, parse_do_line, parse_line, part1, part2


def test_part1():
    lines = input.read_lines(day_num, "example01.txt")
    expected = 161
    result = part1(lines)
    assert result == expected


def test_part2():
    lines = input.read_lines(day_num, "example02.txt")
    expected = 48
    result = part2(lines)
    assert result == expected


def test_parse():
    line = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    assert parse_line(line) == 161


def test_do_parse():
    line = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    assert parse_do_line(line, True) == (48, True)
