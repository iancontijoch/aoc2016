from __future__ import annotations

import argparse
import itertools
import os.path
import re
from collections import deque
from collections.abc import Iterable
from collections.abc import Sequence
from typing import TypeAlias

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

Item: TypeAlias = tuple[str, str]
Carry: TypeAlias = tuple[Item, ...]
State: TypeAlias = tuple[int, Sequence[Item] | None, dict[Item, int]]


def _get_cand_floors(current_floor: int) -> tuple[int, ...]:
    if current_floor == 1:
        return (2,)
    elif current_floor == 4:
        return (3,)
    else:
        return current_floor - 1, current_floor + 1


def _is_irradiated(items: Sequence[tuple[str, str]]) -> bool:
    microchips = [item for item in items if item[0] == 'm']
    generators = [item for item in items if item[0] == 'g']
    unmatched_microchips = [
        m
        for m in microchips
        if m[1:] not in (g[1:] for g in generators) and len(generators) > 0
    ]
    if unmatched_microchips:
        return True

    return False


def _get_cand_carry(
    current_floor: int,
    carrying: Sequence[Item] | None,
    item_floors: dict[Item, int],
) -> list[Carry]:
    items: list[Carry] = []
    items_on_floor: set[Item] = {
        item for item, floor in item_floors.items() if floor == current_floor
    }
    if carrying is not None:
        items_on_floor.update(carrying)
    for i in range(1, 3):
        combos: Iterable[Carry] = itertools.combinations(
            sorted(items_on_floor),
            i,
        )
        items.extend(combos)

    return [combo for combo in items if not _is_irradiated(combo)]


def _get_cand_states(
    current_floor: int,
    carrying: Sequence[Item] | None,
    item_floors: dict[Item, int],
) -> list[tuple[int, Carry]]:
    cand_floors = _get_cand_floors(current_floor)
    cand_carry = _get_cand_carry(current_floor, carrying, item_floors)

    return list(itertools.product(cand_floors, cand_carry))


def compute(s: str) -> int:
    lines = s.splitlines()
    # floors = defaultdict(list)
    item_floors = dict()
    total_items = 0
    for i, line in enumerate(lines):
        generators = [('g', w[:2])
                      for w in re.findall(r'(\w+) generator', line)]
        microchips = [('m', w[:2])
                      for w in re.findall(r'(\w+)-\w+ microchip', line)]
        for g in generators:
            item_floors[g] = i + 1
        for m in microchips:
            item_floors[m] = i + 1

        total_items += len(generators) + len(microchips)

    current_floor = 1
    steps = 0
    carrying = None
    state: State = (current_floor, carrying, item_floors)

    todo: tuple[tuple[State, int, list[object]], ...] = ((state, steps, []),)

    def _update_floors(
        floor: int, carrying: Carry, item_floors: dict[Item, int],
    ) -> dict[Item, int]:
        item_floors = item_floors.copy()
        for item in carrying:
            item_floors[item] = floor

        return item_floors

    def bfs(
        todo: tuple[tuple[State, int, list[object]], ...],
        seen: set[
            tuple[
                int, Sequence[Item] | None,
                frozenset[tuple[Item, int]],
            ]
        ] | None = None,
    ) -> int:
        q = deque(todo)
        shortest = 1_000_000
        if seen is None:
            seen = set()

        while q:
            state, steps, path = q.popleft()
            current_floor, carrying, item_floors = state
            frozen_state = (
                current_floor,
                carrying,
                frozenset(item_floors.items()),
            )

            if frozen_state in seen or steps >= shortest:
                continue

            seen.add(frozen_state)

            if list(item_floors.values()).count(4) == len(item_floors):
                shortest = min(shortest, steps)
                continue

            cand_states = _get_cand_states(
                current_floor,
                carrying,
                item_floors,
            )
            for cand in cand_states:
                next_floor, carrying_cand = cand

                cand_floor = item_floors.copy()
                cand_floor = _update_floors(
                    next_floor,
                    carrying_cand,
                    cand_floor,
                )

                current_floor_items_after = [
                    item
                    for item, floor in cand_floor.items()
                    if floor == current_floor
                ]

                next_floor_items_after = [
                    item
                    for item, floor in cand_floor.items()
                    if floor == next_floor
                ]

                is_invalid = _is_irradiated(
                    next_floor_items_after + list(carrying_cand),
                ) or _is_irradiated(current_floor_items_after)

                if not is_invalid:
                    q.append(
                        (
                            (next_floor, carrying_cand, cand_floor),
                            steps + 1,
                            path.copy() + [frozen_state].copy(),
                        ),
                    )
        return shortest

    return bfs(todo, seen=None)


INPUT_S = """\
The first floor contains a hydrogen-compatible microchip \
    and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.
"""
EXPECTED = 11


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


@pytest.mark.parametrize(
    ('input_int', 'expected'),
    ((1, (2,)), (2, (1, 3)), (3, (2, 4)), (4, (3,))),
)
def test_get_cand_floors(input_int: int, expected: int) -> None:
    assert _get_cand_floors(input_int) == expected


@pytest.mark.parametrize(
    ('input', 'expected'),
    (
        ((('m', 'h'), ('g', 'h')), False),
        ((('m', 'h'), ('g', 't')), True),
        ((('m', 'h'), ('g', 't'), ('m', 't')), True),
        ((('m', 'h'), ('g', 'h'), ('g', 't')), False),
        ((('g', 'x'), ('g', 'h'), ('g', 't')), False),
        ((('m', 'h'),), False),
        ((('g', 'h'),), False),
    ),
)
def test_is_irradiated(input: Carry, expected: int) -> None:
    assert _is_irradiated(input) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
