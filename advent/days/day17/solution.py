from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from enum import Enum

day_num = 17


class Instruction(Enum):
    Adv = 0
    Bxl = 1
    Bst = 2
    Jnz = 3
    Bxc = 4
    Out = 5
    Bdv = 6
    Cdv = 7


@dataclass(slots=True)
class Program:
    registers: list[int]
    code: list[int]
    ip: int = 0
    out: list[int] = field(default_factory=list)

    @classmethod
    def parse(cls, lines: Iterator[str]) -> Program:
        _, reg_a = next(lines).split(":")
        reg_a = int(reg_a.strip())
        _, reg_b = next(lines).split(":")
        reg_b = int(reg_b.strip())
        _, reg_c = next(lines).split(":")
        reg_c = int(reg_c.strip())
        _ = next(lines)
        _, prog = next(lines).split(":")
        program = [int(i.strip()) for i in prog.split(",")]
        return Program([reg_a, reg_b, reg_c], program)

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

    def step(self):
        match self.code[self.ip]:
            case 0:  # adv
                self.registers[0] //= 2 ** self.combo(self.code[self.ip + 1])
                self.ip += 2
            case 1:  # bxl
                self.registers[1] ^= self.code[self.ip + 1]
                self.ip += 2
            case 2:  # bst
                self.registers[1] = self.combo(self.code[self.ip + 1]) % 8
                self.ip += 2
            case 3:  # bst
                if self.registers[0]:
                    self.ip = self.code[self.ip + 1]
                else:
                    self.ip += 2
            case 4:  # bxc
                self.registers[1] ^= self.registers[2]
                self.ip += 2
            case 5:  # out
                self.out.append(self.combo(self.code[self.ip + 1]) % 8)
                self.ip += 2
            case 6:  # bdv
                self.registers[1] = self.registers[0] // 2 ** self.combo(
                    self.code[self.ip + 1]
                )
                self.ip += 2
            case 7:  # cdv
                self.registers[2] = self.registers[0] // 2 ** self.combo(
                    self.code[self.ip + 1]
                )
                self.ip += 2
            case _:
                raise Exception("Illegal inst")

    def run(self) -> str:
        while self.ip < len(self.code):
            self.step()
        return ",".join(str(o) for o in self.out)

    def is_copy(self) -> bool:
        return self.code == self.out


def part1(lines: Iterator[str]) -> str:
    prog = Program.parse(lines)
    return prog.run()


def part2(lines: Iterator[str]) -> int:
    return None
