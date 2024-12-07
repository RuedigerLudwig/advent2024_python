from advent.common import input

from .solution import Report, day_num, part1, part2


def test_part1():
    lines = input.read_lines(day_num, "example01.txt")
    expected = 2
    result = part1(lines)
    assert result == expected


def test_part2():
    lines = input.read_lines(day_num, "example01.txt")
    expected = 4
    result = part2(lines)
    assert result == expected


def test_parse_safe():
    line = "7 6 4 2 1"
    report = Report.parse(line)
    assert report.is_safe()


def test_parse_safe_damped():
    line = "4 5 3 2 1"
    report = Report.parse(line)
    assert report.is_safe_damped()


def test_parse_safe_damped2():
    line = "1 2 7 8 9"
    report = Report.parse(line)
    assert not report.is_safe_damped()
