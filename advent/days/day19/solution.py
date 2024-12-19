from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field

day_num = 19


@dataclass(slots=True)
class Tree:
    start: str
    virtual: bool
    following: list[Tree] = field(default_factory=list)

    def insert(self, next: Tree):
        added = False
        for child in self.following:
            if next.start.startswith(child.start):
                child.insert(next)
                added = True
        if not added:
            if len(self.start) + 1 == len(next.start):
                self.following.append(next)
            else:
                virt = Tree(next.start[: len(self.start) + 1], True)
                virt.insert(next)
                self.following.append(virt)

    def compress(self):
        for child in self.following:
            child.compress()
        if self.virtual and len(self.following) == 1:
            child = self.following[0]
            self.virtual = child.virtual
            self.start = child.start
            self.following = child.following

    def print(self, indent: int = 0):
        print("--" * indent, end="")
        if self.start != "":
            print(f" {self.start}", end="")
            if self.virtual:
                print(" (virtual)")
            else:
                print()
        else:
            print("(root)")
        for child in self.following:
            child.print(indent + 1)


@dataclass(slots=True)
class Towels:
    available: Tree
    desired: list[str]

    @classmethod
    def parse(cls, lines: Iterator[str]) -> Towels:
        available = [av.strip() for av in next(lines).split(",")]
        available.sort(key=lambda a: (len(a), a))
        tree = Tree("", True)
        for a in available:
            tree.insert(Tree(a, False))

        tree.compress()
        # tree.print()
        # raise Exception("Stop")

        _ = next(lines)

        desired = [line.strip() for line in lines]

        return Towels(tree, desired)

    def is_possible(
        self, towel: str, available: Tree, impossible: set[str], check_virtual: bool
    ) -> bool:
        if towel in impossible:
            return False
        if not towel:
            return True

        for av in available.following:
            if towel.startswith(av.start):
                if self.is_possible(towel, av, impossible, False):
                    return True
                if not av.virtual and self.is_possible(
                    towel[len(av.start) :], self.available, impossible, True
                ):
                    return True

        impossible.add(towel)
        return False

    def count_possible(self) -> int:
        sum = 0
        for towel in self.desired:
            if self.is_possible(towel, self.available, set(), False):
                sum += 1
        return sum

    def count_variants(self, towel: str, available: Tree, impossible: set[str]) -> int:
        if towel in impossible:
            return 0
        if not towel:
            return 1

        variants = 0
        for av in available.following:
            if towel.startswith(av.start):
                variants += self.count_variants(towel, av, impossible)
                if not av.virtual:
                    variants += self.count_variants(
                        towel[len(av.start) :], self.available, impossible
                    )

        return variants

    def count_all_variants(self) -> int:
        sum = 0
        impossible: set[str] = set()
        for towel in self.desired:
            if self.is_possible(towel, self.available, impossible, False):
                sum += self.count_variants(towel, self.available, impossible)
        return sum


def part1(lines: Iterator[str]) -> int:
    towel = Towels.parse(lines)
    return towel.count_possible()


def part2(lines: Iterator[str]) -> int:
    towel = Towels.parse(lines)
    return towel.count_all_variants()
