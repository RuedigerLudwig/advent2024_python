from advent.common import input

from .solution import Towels, day_num, part1, part2


def test_part1():
    lines = input.read_lines(day_num, "example01.txt")
    expected = 6
    result = part1(lines)
    assert result == expected


def test_part2():
    lines = input.read_lines(day_num, "example01.txt")
    expected = 16
    result = part2(lines)
    assert result == expected


def test_parse():
    lines = input.read_lines(day_num, "example01.txt")
    towels = Towels.parse(lines)
    assert towels.available.start == ""
    assert {c.start for c in towels.available.following} == {"r", "wr", "b", "g"}
    assert len(towels.desired) == 8


def test_check():
    lines = input.read_lines(day_num, "example01.txt")
    towels = Towels.parse(lines)
    assert towels.count_all_variants() == 16
