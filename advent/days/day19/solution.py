from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field

day_num = 19


@dataclass(slots=True)
class TowelTree:
    start: str
    is_virtual: bool
    children: list[TowelTree] = field(default_factory=list)

    def insert(self, next: TowelTree):
        for child in self.children:
            if next.start.startswith(child.start):
                child.insert(next)
                return

        if len(self.start) + 1 == len(next.start):
            self.children.append(next)
        else:
            virt = TowelTree(next.start[: len(self.start) + 1], True)
            virt.insert(next)
            self.children.append(virt)

    def compress(self):
        for child in self.children:
            child.compress()

        if self.is_virtual and len(self.children) == 1:
            child = self.children[0]
            self.is_virtual = child.is_virtual
            self.start = child.start
            self.children = child.children

    def print(self, indent: int = 0):
        print("--" * indent, end="")
        if self.start != "":
            print(f" {self.start}", end="")
            if self.is_virtual:
                print(" (virtual)")
            else:
                print()
        else:
            print("(root)")
        for child in self.children:
            child.print(indent + 1)


@dataclass(slots=True)
class Towels:
    pattern: TowelTree
    desired: list[str]

    @classmethod
    def parse(cls, lines: Iterator[str]) -> Towels:
        raw_towels = [towel.strip() for towel in next(lines).split(",")]
        raw_towels.sort(key=lambda a: (len(a), a))
        towels = TowelTree("", True)
        for towel in raw_towels:
            towels.insert(TowelTree(towel, False))

        towels.compress()

        _ = next(lines)

        desired = [line.strip() for line in lines]

        return Towels(towels, desired)

    def is_possible(
        self, design: str, towels: TowelTree, impossible: set[str], is_final: bool
    ) -> bool:
        if design in impossible:
            return False
        if not design:
            return True

        for towel in towels.children:
            if design.startswith(towel.start):
                if self.is_possible(design, towel, impossible, False):
                    return True
                if not towel.is_virtual and self.is_possible(
                    design[len(towel.start) :], self.pattern, impossible, True
                ):
                    return True

        if is_final:
            impossible.add(design)
        return False

    def count_possible(self) -> int:
        sum = 0
        impossible: set[str] = set()
        for design in self.desired:
            if self.is_possible(design, self.pattern, impossible, False):
                sum += 1
        return sum

    def count_variants(
        self, banner: str, towels: TowelTree, known: dict[str, int], is_final: bool
    ) -> int:
        if (count := known.get(banner)) is not None:
            return count
        if not banner:
            return 1

        variants = 0
        for towel in towels.children:
            if banner.startswith(towel.start):
                variants += self.count_variants(banner, towel, known, False)
                if not towel.is_virtual:
                    variants += self.count_variants(
                        banner[len(towel.start) :], self.pattern, known, True
                    )

        if is_final:
            known[banner] = variants

        return variants

    def count_all_variants(self) -> int:
        sum = 0
        known: dict[str, int] = {}
        for towel in self.desired:
            sum += self.count_variants(towel, self.pattern, known, True)
        return sum


def part1(lines: Iterator[str]) -> int:
    towel = Towels.parse(lines)
    return towel.count_possible()


def part2(lines: Iterator[str]) -> int:
    towel = Towels.parse(lines)
    return towel.count_all_variants()
