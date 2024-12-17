from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass

from advent.common.helper import as_two_tuple

day_num = 17


@dataclass(slots=True)
class Program:
    registers: list[int]
    code: list[int]
    ip: int = 0

    @staticmethod
    def second_part(data: str, divide: str) -> str:
        _, payload = data.split(":", maxsplit=2)
        return payload.strip()

    @classmethod
    def parse(cls, lines: Iterator[str]) -> Program:
        reg_a = int(Program.second_part(next(lines), ":"))
        reg_b = int(Program.second_part(next(lines), ":"))
        reg_c = int(Program.second_part(next(lines), ":"))
        _ = next(lines)
        code_str = Program.second_part(next(lines), ":")
        code = [int(i) for i in code_str.split(",")]
        return Program([reg_a, reg_b, reg_c], code)

    def combo(self, value: int) -> int:
        match value:
            case 0 | 1 | 2 | 3:
                return value
            case 4:
                return self.registers[0]
            case 5:
                return self.registers[1]
            case 6:
                return self.registers[2]
            case _:
                raise Exception("Unknown Operand")

    def run(self) -> Iterator[int]:
        while self.ip < len(self.code):
            if (out := self.run_once()) is not None:
                yield out

    def run_once(self) -> int | None:
        while self.ip < len(self.code):
            match self.code[self.ip], self.code[self.ip + 1]:
                case 0, v:  # adv
                    self.registers[0] >>= self.combo(v)
                    self.ip += 2
                case 1, v:  # bxl
                    self.registers[1] ^= v
                    self.ip += 2
                case 2, v:  # bst
                    self.registers[1] = self.combo(v) % 8
                    self.ip += 2
                case 3, v:  # jnz
                    if self.registers[0]:
                        self.ip = v
                    else:
                        self.ip += 2
                case 4, _:  # bxc
                    self.registers[1] ^= self.registers[2]
                    self.ip += 2
                case 5, v:  # out
                    out = self.combo(v) % 8
                    self.ip += 2
                    return out
                case 6, v:  # bdv
                    self.registers[1] = self.registers[0] >> self.combo(v)
                    self.ip += 2
                case 7, v:  # cdv
                    self.registers[2] = self.registers[0] >> self.combo(v)
                    self.ip += 2
                case c, _:
                    raise Exception(f"Illegal code: {c}")
        return None

    def test_numbers(self, num: list[int], value: int, bits: int) -> int | None:
        if not num:
            return value

        to_hit = num[0]
        value <<= bits
        for check in range(2**bits):
            self.registers[0] = value + check
            self.ip = 0
            out = self.run_once()
            if out == to_hit:
                result = self.test_numbers(num[1:], value + check, bits)
                if result is not None:
                    return result
        return None

    def check_assumptions(self):
        # we have an even number of code instructions
        assert len(self.code) % 2 == 0

        # there is exactly one output
        assert 1 == sum(1 for a, _ in as_two_tuple(self.code) if a == 5)

        # register a is changed only once
        assert 1 == sum(1 for a, _ in as_two_tuple(self.code) if a == 0)
        assert 1 == sum(1 for a, b in as_two_tuple(self.code) if a == 0 and b > 0)

        # the last instruction is the only jump and it jumps back to 0
        assert 1 == sum(1 for a, _ in as_two_tuple(self.code) if a == 3)
        assert self.code[-2] == 3
        assert self.code[-1] == 0

    def run_backwards(self) -> int:
        self.check_assumptions()

        bits = sum(b for a, b in as_two_tuple(self.code) if a == 0)

        test = list(reversed(self.code))
        result = self.test_numbers(test, 0, bits)
        if result is None:
            raise Exception("No valid number found")

        return result


def part1(lines: Iterator[str]) -> str:
    prog = Program.parse(lines)
    return ",".join(str(o) for o in prog.run())


def part2(lines: Iterator[str]) -> int:
    prog = Program.parse(lines)
    return prog.run_backwards()
