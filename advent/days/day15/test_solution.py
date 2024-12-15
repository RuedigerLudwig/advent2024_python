from advent.common import input
from advent.common.position import Position

from .solution import SmallGoods, day_num, part1, part2


def test_part1():
    lines = input.read_lines(day_num, "example01.txt")
    expected = 2028
    result = part1(lines)
    assert result == expected



def test_part2():
    lines = input.read_lines(day_num, "example02.txt")
    expected = 9021
    result = part2(lines)
    assert result == expected



def test_parse():
    lines = input.read_lines(day_num, "example01.txt")
    goods = SmallGoods.parse(lines)
    assert len(goods.map) == 8
    assert len(goods.map[0]) == 8
    assert goods.robot == Position(2, 2)
    assert len(goods.moves) == 15