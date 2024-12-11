from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from collections.abc import Iterator


from advent.common.helper import as_two_tuple

day_num = 9


@dataclass(frozen=True, slots=True)
class DiskMap:
    orig: list[int]

    @classmethod
    def parse(cls, lines: Iterator[str]) -> DiskMap:
        orig = [int(digit) for digit in next(lines)]
        return DiskMap(orig)

    @staticmethod
    def gauss_sum(n: int) -> int:
        return (n * n + n) // 2

    @staticmethod
    def sum(start: int, len: int) -> int:
        result = sum(n for n in range(start, start + len))
        return result

    def compress(self) -> int:
        blocks = self.orig.copy()

        checksum = 0
        start_file = 0
        start_pos = 0
        start_disk = 0
        end_file = (len(blocks) - 1) // 2
        end_pos = len(blocks) - 1
        while end_pos > start_pos:
            checksum += start_file * DiskMap.sum(start_disk, blocks[start_pos])
            start_disk += blocks[start_pos]
            start_pos += 1
            while blocks[start_pos] != 0:
                diff = min(blocks[end_pos], blocks[start_pos])
                checksum += end_file * DiskMap.sum(start_disk, diff)
                start_disk += diff
                blocks[start_pos] -= diff
                blocks[end_pos] -= diff
                if blocks[end_pos] == 0:
                    end_pos -= 2
                    end_file -= 1
            start_pos += 1
            start_file += 1
        checksum += start_file * DiskMap.sum(start_disk, blocks[start_pos])
        return checksum

    def compress_better(self) -> int:
        file_blocks: list[tuple[int, int]] = []
        spaces: list[deque[int]] = [deque() for _ in range(10)]
        position = 0
        for blocks, space in as_two_tuple(self.orig, default=0):
            assert blocks != 0
            file_blocks.append((blocks, position))
            position += blocks
            spaces[space].appendleft(position)
            position += space

        checksum = 0

        for file, (blocks, position) in enumerate(reversed(file_blocks)):
            file = len(file_blocks) - file - 1

            best = min(
                (
                    (spaces[space][-1], space)
                    for space in range(blocks, 10)
                    if spaces[space] and spaces[space][-1] < position
                ),
                default=None,
            )

            if best is not None:
                space_position, space = best

                checksum += file * DiskMap.sum(space_position, blocks)

                spaces[space].pop()
                rest_space = space - blocks
                if rest_space > 0:
                    space_position += blocks
                    larger: deque[int] = deque()
                    while (
                        spaces[rest_space] and spaces[rest_space][-1] < space_position
                    ):
                        larger.append(spaces[rest_space].pop())
                    spaces[rest_space].append(space_position)
                    while larger:
                        spaces[rest_space].append(larger.pop())
            else:
                checksum += file * DiskMap.sum(position, blocks)
        return checksum


def part1(lines: Iterator[str]) -> int:
    disk = DiskMap.parse(lines)
    return disk.compress()


def part2(lines: Iterator[str]) -> int:
    disk = DiskMap.parse(lines)
    return disk.compress_better()
