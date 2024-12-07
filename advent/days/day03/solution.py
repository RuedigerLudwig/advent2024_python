from __future__ import annotations

from enum import Enum
import re
from typing import Iterator

day_num = 3


class State(Enum):
    START = 999
    M = 0
    U = 1
    L = 2
    OB = 3
    FFD = 4
    SFD = 5
    TFD = 6
    K = 7
    FSD = 8
    SSD = 9
    TSD = 10
    D = 11
    O = 12
    N = 13
    AP = 14
    T = 15
    ODB = 16
    ONB = 17


def parse_line(line: str) -> int:
    result = 0
    mul = r"mul\((\d{1,3}),(\d{1,3})\)"
    regex = re.compile(mul)
    for m in regex.finditer(line):
        num1 = int(m.group(1))
        num2 = int(m.group(2))
        result += num1 * num2

    return result


def parse_do_line(line: str, do_mul: bool) -> tuple[int, bool]:
    mul = r"(mul\((\d{1,3}),(\d{1,3})\)|don't\(\)|do\(\))"
    result = 0
    for m in re.findall(mul, line):
        all = m[0]
        match all:
            case "do()":
                do_mul = True
            case "don't()":
                do_mul = False
            case _:
                if do_mul:
                    num1 = int(m[1])
                    num2 = int(m[2])
                    result += num1 * num2

    return result, do_mul


def parse_line_x(line: str) -> int:
    state: State = State.START
    num1 = 0
    num2 = 0
    result = 0
    for c in line:
        match c, state:
            case "m", _:
                state = State.M
            case "u", State.M:
                state = State.U
            case "l", State.U:
                state = State.L
            case "(", State.L:
                state = State.OB
            case "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9", State.OB:
                num1 = int(c)
                state = State.FFD
            case "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9", State.FFD:
                num1 = num1 * 10 + int(c)
                state = State.SFD
            case "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9", State.SFD:
                num1 = num1 * 10 + int(c)
                state = State.TFD
            case ",", State.FFD | State.SFD | State.TFD:
                state = State.K
            case "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9", State.K:
                num2 = int(c)
                state = State.FSD
            case "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9", State.FSD:
                num2 = num2 * 10 + int(c)
                state = State.SSD
            case "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9", State.SSD:
                num2 = num2 * 10 + int(c)
                state = State.TSD
            case ")", State.FSD | State.SSD | State.TSD:
                result += num1 * num2
                state = State.START

            case _:
                state = State.START

    return result


def parse_do_line_(line: str, do_mul: bool) -> tuple[int, bool]:
    state: State = State.START
    num1 = 0
    num2 = 0
    result = 0
    for c in line:
        match c, state:
            case "m", State.START:
                state = State.M
            case "u", State.M:
                state = State.U
            case "l", State.U:
                state = State.L
            case "(", State.L:
                state = State.OB
            case "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9", State.OB:
                num1 = int(c)
                state = State.FFD
            case "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9", State.FFD:
                num1 = num1 * 10 + int(c)
                state = State.SFD
            case "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9", State.SFD:
                num1 = num1 * 10 + int(c)
                state = State.TFD
            case ",", State.FFD | State.SFD | State.TFD:
                state = State.K
            case "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9", State.K:
                num2 = int(c)
                state = State.FSD
            case "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9", State.FSD:
                num2 = num2 * 10 + int(c)
                state = State.SSD
            case "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9", State.SSD:
                num2 = num2 * 10 + int(c)
                state = State.TSD
            case ")", State.FSD | State.SSD | State.TSD:
                if do_mul:
                    result += num1 * num2
                state = State.START
            case "d", _:
                state = State.D
            case "o", State.D:
                state = State.O
            case "n", State.O:
                state = State.N
            case "'", State.N:
                state = State.AP
            case "t", State.AP:
                state = State.T
            case "(", State.O:
                state = State.ODB
            case ")", State.ODB:
                do_mul = True
                state = State.START
            case "(", State.T:
                state = State.ONB
            case ")", State.ONB:
                do_mul = False
                state = State.START
            case _:
                state = State.START

    return result, do_mul


def part1(lines: Iterator[str]) -> int:
    return sum(parse_line(line) for line in lines)


def part2(lines: Iterator[str]) -> int:
    result = 0
    do_mul = True
    for line in lines:
        r, do_mul = parse_do_line(line, do_mul)
        result += r
    return result
