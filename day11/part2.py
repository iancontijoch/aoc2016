from __future__ import annotations

import argparse
import itertools
import os.path
import re
from collections import deque
from collections.abc import Sequence
from typing import TypeAlias

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

Item: TypeAlias = tuple[str, str]
Carry: TypeAlias = tuple[Item, ...]
State: TypeAlias = tuple[int, dict[Item, int]]
CanonKey: TypeAlias = tuple[int, tuple[tuple[int, int], ...]]


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
    return bool(unmatched_microchips)


def _canon_key(elev: int, item_floors: dict[Item, int]) -> CanonKey:
    pairs: list[tuple[int, int]] = []
    elems: set[str] = {elem for _, elem in item_floors}
    for elem in elems:
        gf = item_floors.get(('g', elem))
        mf = item_floors.get(('m', elem))
        if gf is None or mf is None:
            continue
        pairs.append((gf, mf))
    pairs.sort()
    return (elev, tuple(pairs))


def _get_cand_carry(
    current_floor: int,
    item_floors: dict[Item, int],
) -> list[Carry]:
    items_on_floor: list[Item] = [
        item for item, floor in item_floors.items() if floor == current_floor
    ]

    res: list[Carry] = []
    for k in (2, 1):
        res.extend(itertools.combinations(items_on_floor, k))

    return list(res)


def _get_cand_states(
    current_floor: int, item_floors: dict[Item, int],
) -> list[tuple[int, Carry]]:
    cand: list[tuple[int, Carry]] = []
    any_below = any(floor < current_floor for floor in item_floors.values())
    carries = _get_cand_carry(current_floor, item_floors)

    for next_floor in _get_cand_floors(current_floor):
        going_up = next_floor > current_floor
        if not going_up and not any_below:
            continue
        for carry in carries:
            if going_up and len(carry) == 1:
                continue
            if not going_up and len(carry) == 2:
                continue
            cand.append((next_floor, carry))

    # add single-item moves after doubles
    for next_floor in _get_cand_floors(current_floor):
        if next_floor > current_floor:
            for carry in carries:
                if len(carry) == 1:
                    cand.append((next_floor, carry))

    return cand


def compute(s: str) -> int:
    lines = s.splitlines()
    item_floors: dict[Item, int] = {}
    for i, line in enumerate(lines):
        generators = [('g', w[:2])
                      for w in re.findall(r'(\w+) generator', line)]
        microchips = [('m', w[:2])
                      for w in re.findall(r'(\w+)-\w+ microchip', line)]
        for g in generators:
            item_floors[g] = i + 1
        for m in microchips:
            item_floors[m] = i + 1

        # part 2 items
        item_floors[('g', 'el')] = 1
        item_floors[('m', 'el')] = 1
        item_floors[('g', 'di')] = 1
        item_floors[('m', 'di')] = 1

    current_floor = 1
    steps = 0
    state: State = (current_floor, item_floors)
    todo: tuple[tuple[State, int], ...] = ((state, steps),)

    def _update_floors(
        floor: int,
        carrying: Carry,
        item_floors: dict[Item, int],
    ) -> dict[Item, int]:
        item_floors = item_floors.copy()
        for item in carrying:
            item_floors[item] = floor

        return item_floors

    def bfs(
        todo: tuple[tuple[State, int], ...],
        seen: set[CanonKey] | None = None,
    ) -> int:
        q = deque(todo)
        if seen is None:
            seen = set()

        while q:
            (elev, floors), steps = q.popleft()
            key = _canon_key(elev, floors)
            if key in seen:
                continue
            seen.add(key)

            if list(floors.values()).count(4) == len(floors):
                return steps

            for next_floor, carry in _get_cand_states(elev, floors):
                new_floors = _update_floors(next_floor, carry, floors)
                src_items = [i for i, fl in new_floors.items() if fl == elev]
                dst_items = [
                    i for i, fl in new_floors.items()
                    if fl == next_floor
                ]

                if _is_irradiated(src_items) or _is_irradiated(dst_items):
                    continue
                q.append(((next_floor, new_floors), steps + 1))
        return 10**9

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
