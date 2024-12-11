from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from collections.abc import Iterator

day_num = 5


@dataclass(frozen=True, slots=True)
class Manual:
    order: dict[int, list[int]]
    updates: list[list[int]]

    @classmethod
    def parse_order(cls, lines: Iterator[str]) -> Iterator[tuple[int, int]]:
        while (line := next(lines)) != "":
            page1, page2 = line.split("|", maxsplit=1)
            yield (int(page1), int(page2))

    @classmethod
    def parse(cls, lines: Iterator[str]) -> Manual:
        order: dict[int, list[int]] = {}
        for p1, p2 in Manual.parse_order(lines):
            lst = order.get(p1)
            if lst is None:
                lst = [p2]
            else:
                lst.append(p2)
            order[p1] = lst

        updates: list[list[int]] = []
        for line in lines:
            updates.append([int(number) for number in line.split(",")])
        return Manual(order, updates)

    def is_update_ordered(self, update: list[int]) -> bool:
        updates = list(reversed(update))
        for pos, page2 in enumerate(updates):
            following = self.order.get(page2)
            if following is None:
                continue
            for page1 in updates[pos + 1 :]:
                if page1 in following:
                    return False
        return True

    def follows(self, page1: int, page2: int) -> bool:
        return page2 in self.order.get(page1, [])

    def reorder(self, update: list[int]) -> list[int]:
        unordered = deque(update)

        ordered: list[int] = []
        while not not unordered:
            page_to_insert = unordered.popleft()
            if not ordered:
                ordered.append(page_to_insert)
            else:
                inserted_page = False
                for pos, page in enumerate(ordered):
                    if self.follows(page_to_insert, page):
                        ordered.insert(pos, page_to_insert)
                        inserted_page = True
                        break

                if not inserted_page:
                    if not unordered:
                        ordered.append(page_to_insert)
                        return ordered
                    elif self.follows(ordered[-1], page_to_insert):
                        ordered.append(page_to_insert)
                    else:
                        unordered.append(page_to_insert)
        return ordered

    def value_ordered_updates(self) -> int:
        result = 0
        for update in self.updates:
            if self.is_update_ordered(update):
                result += update[len(update) // 2]
        return result

    def value_unordered_updates(self) -> int:
        result = 0
        for update in self.updates:
            if not self.is_update_ordered(update):
                reordered = self.reorder(update)
                result += reordered[len(reordered) // 2]
        return result


def part1(lines: Iterator[str]) -> int:
    manual = Manual.parse(lines)
    return manual.value_ordered_updates()


def part2(lines: Iterator[str]) -> int:
    manual = Manual.parse(lines)
    return manual.value_unordered_updates()
