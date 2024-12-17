from advent.common import input

from .solution import Program, day_num, part1, part2


def test_part1():
    lines = input.read_lines(day_num, "example01.txt")
    expected = "4,6,3,5,6,3,5,2,1,0"
    result = part1(lines)
    assert result == expected


def test_part2():
    lines = input.read_lines(day_num, "example03.txt")
    expected = 117440
    result = part2(lines)
    assert result == expected


def test_backwards():
    lines = input.read_lines(day_num, "example03.txt")
    expected = 117440
    prog = Program.parse(lines)
    result = prog.run_backwards()
    assert result == expected


def test_small1():
    prog = Program([0, 0, 9], [2, 6])
    prog.run_once()
    assert prog.registers[1] == 1


def test_small2():
    prog = Program([10, 0, 0], [5, 0, 5, 1, 5, 4])
    out = list(prog.run())
    assert out == [0, 1, 2]


def test_small3():
    prog = Program([2024, 0, 0], [0, 1, 5, 4, 3, 0])
    out = list(prog.run())
    assert out == [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]
    assert prog.registers[0] == 0


def test_small4():
    prog = Program([0, 29, 0], [1, 7])
    list(prog.run())
    assert prog.registers[1] == 26


def test_small5():
    prog = Program([0, 2024, 43690], [4, 0])
    list(prog.run())
    assert prog.registers[1] == 44354
