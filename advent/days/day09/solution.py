from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator


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
        files = self.orig.copy()

        checksum = 0
        start_file = 0
        start_pos = 0
        start_disk = 0
        end_file = (len(files) - 1) // 2
        end_pos = len(files) - 1
        while end_pos > start_pos:
            checksum += start_file * DiskMap.sum(start_disk, files[start_pos])
            start_disk += files[start_pos]
            start_pos += 1
            while files[start_pos] != 0:
                diff = min(files[end_pos], files[start_pos])
                checksum += end_file * DiskMap.sum(start_disk, diff)
                start_disk += diff
                files[start_pos] -= diff
                files[end_pos] -= diff
                if files[end_pos] == 0:
                    end_pos -= 2
                    end_file -= 1
            start_pos += 1
            start_file += 1
        checksum += start_file * DiskMap.sum(start_disk, files[start_pos])
        return checksum

    def compress_better(self) -> int:
        files: list[tuple[int, int]] = []
        spaces: list[tuple[int, int]] = []
        position = 0
        for file, space in as_two_tuple(self.orig, default=0):
            files.append((file, position))
            position += file
            spaces.append((space, position))
            position += space

        checksum = 0

        for file, (blocks, position) in enumerate(reversed(files)):
            file = len(files) - file - 1

            found = False
            for space_id in range(len(spaces)):
                space, space_position = spaces[space_id]
                if space_position >= position:
                    break
                if space >= blocks:
                    checksum += file * DiskMap.sum(space_position, blocks)
                    spaces[space_id] = space - blocks, space_position + blocks
                    found = True
                    break
            if not found:
                checksum += file * DiskMap.sum(position, blocks)
        return checksum


def part1(lines: Iterator[str]) -> int:
    disk = DiskMap.parse(lines)
    return disk.compress()


def part2(lines: Iterator[str]) -> int:
    disk = DiskMap.parse(lines)
    return disk.compress_better()
