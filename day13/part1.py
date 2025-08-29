from __future__ import annotations

import argparse
import os.path
from collections import deque
from typing import TypeAlias

import pytest

import support

Pos: TypeAlias = tuple[int, int]


INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str, end: tuple[int, int]) -> int:
    lines = s.splitlines()
    num = int(lines[0])

    def _is_wall(x: int, y: int) -> bool:
        ret = x * x + 3 * x + 2 * x * y + y + y * y
        ret += num
        return bin(ret)[2:].count('1') % 2 != 0

    coords = {
        (x, y): '#' if _is_wall(x, y) else '.'
        for x in range(end[0] + 100)
        for y in range(end[1] + 100)
    }

    start = (1, 1)
    steps = 0

    todo = [(start, steps)]

    def bfs(
        todo: list[tuple[Pos, int]],
        end: Pos,
        seen: set[Pos] | None = None,
    ) -> int:
        if seen is None:
            seen = set()
        q = deque(todo)
        while q:
            pos, steps = q.popleft()
            if pos in seen:
                continue
            seen.add(pos)

            if pos == end:
                return steps

            cands = (
                cand
                for cand, val in coords.items()
                if val == '.' and cand in support.adjacent_4(*pos)
            )
            for cand in cands:
                q.append((cand, steps + 1))
        return 10**9

    return bfs(todo, end)


INPUT_S = """\
10
"""
EXPECTED = 11
END = (7, 4)


@pytest.mark.parametrize(
    ('input_s', 'end', 'expected'),
    ((INPUT_S, END, EXPECTED),),
)
def test(input_s: str, end: tuple[int, int], expected: int) -> None:
    assert compute(input_s, end) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read(), end=(31, 39)))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
