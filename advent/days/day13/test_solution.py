from advent.common import input

from .solution import Machine, day_num, part1, part2


def test_part1():
    lines = input.read_lines(day_num, "example01.txt")
    expected = 480
    result = part1(lines)
    assert result == expected


def test_part2():
    lines = input.read_lines(day_num, "example01.txt")
    expected = 875318608908
    result = part2(lines)
    assert result == expected


def test_parse():
    lines = input.read_lines(day_num, "example01.txt")
    machines = list(Machine.parse(lines))
    assert len(machines) == 4


def test_win():
    lines = input.read_lines(day_num, "example01.txt")
    machines = list(Machine.parse(lines))
    assert machines[0].win_prize() == 280
    assert machines[1].win_prize() is None
    assert machines[2].win_prize() == 200
    assert machines[3].win_prize() is None
