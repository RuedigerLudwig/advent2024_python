from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterator

day_num = 7


@dataclass(frozen=True, slots=True)
class Equation:
    result: int
    operands: list[int]

    @classmethod
    def parse(cls, line: str) -> Equation:
        result, operands = line.split(":", maxsplit=2)
        operands = [int(o) for o in operands.split()]
        return Equation(int(result), operands)

    @staticmethod
    def up_operators(
        operators: list[int], max_number: int, runner: int = 1
    ) -> list[int] | None:
        for r in range(1, runner):
            operators[-r] = 0
        while runner <= len(operators):
            value = operators[-runner] + 1
            if value < max_number:
                operators[-runner] = value
                return operators

            operators[-runner] = 0
            runner += 1

        return None

    def is_valid(self, num_operators: int) -> bool:
        operators: list[int] | None = [0] * (len(self.operands) - 1)

        while operators is not None:
            result = self.operands[0]
            cut_off: int | None = None
            for pos, (operand, operator) in enumerate(
                zip(self.operands[1:], operators)
            ):
                match operator:
                    case 2:
                        op_len = int(math.log10(operand)) + 1
                        result = result * (10**op_len) + operand
                    case 1:
                        result *= operand
                    case _:
                        result += operand

                if result > self.result:
                    cut_off = pos
                    break

            if result == self.result:
                return True

            if cut_off is not None:
                to_cut = len(operators) - cut_off
                operators = self.up_operators(operators, num_operators, to_cut)
            else:
                operators = self.up_operators(operators, num_operators)

        return False

    def is_valid_two(self) -> bool:
        return self.is_valid(2)

    def is_valid_three(self) -> bool:
        return self.is_valid(2) or self.is_valid(3)


def part1(lines: Iterator[str]) -> int:
    return sum(
        eq.result for line in lines if (eq := Equation.parse(line)).is_valid_two()
    )


def part2(lines: Iterator[str]) -> int:
    return sum(
        eq.result for line in lines if (eq := Equation.parse(line)).is_valid_three()
    )
