from advent.common import input

from .solution import DiskMap, day_num, part1, part2


def test_part1():
    lines = input.read_lines(day_num, "example01.txt")
    expected = 1928
    result = part1(lines)
    assert result == expected


def test_part2():
    lines = input.read_lines(day_num, "example01.txt")
    expected = 2858
    result = part2(lines)
    assert result == expected


def test_parse():
    lines = input.read_lines(day_num, "example01.txt")
    disk = DiskMap.parse(lines)
    assert len(disk.orig) == 19
    disk.compress()
