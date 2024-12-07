from advent.common import input

from .solution import Manual, day_num, part1, part2


def test_part1():
    lines = input.read_lines(day_num, "example01.txt")
    expected = 143
    result = part1(lines)
    assert result == expected


def test_part2():
    lines = input.read_lines(day_num, "example01.txt")
    expected = 123
    result = part2(lines)
    assert result == expected


def test_parse():
    lines = input.read_lines(day_num, "example01.txt")
    manual = Manual.parse(lines)
    assert len(manual.updates) == 6


def test_ordered():
    lines = input.read_lines(day_num, "example01.txt")
    manual = Manual.parse(lines)
    assert manual.is_update_ordered(manual.updates[0])
    assert not manual.is_update_ordered(manual.updates[5])


def test_order():
    lines = input.read_lines(day_num, "example01.txt")
    manual = Manual.parse(lines)
    assert manual.reorder([75, 97, 47, 61, 53]) == [97, 75, 47, 61, 53]
    assert manual.reorder([97, 13, 75, 29, 47]) == [97, 75, 47, 29, 13]
