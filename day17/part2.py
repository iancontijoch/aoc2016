from __future__ import annotations

import argparse
import os.path
from collections import deque
from collections.abc import Generator
from hashlib import md5

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def hash(s: str) -> str:
    return md5(s.encode('utf-8')).hexdigest()[:4]


def is_open(s: str) -> Generator[bool]:
    return (c in 'bcdef' for c in s)


def udlr_adj_4(x: int, y: int) -> Generator[tuple[str, int, int]]:
    yield 'U', x, y - 1
    yield 'D', x, y + 1
    yield 'L', x - 1, y
    yield 'R', x + 1, y


def compute(s: str) -> int | None:
    line = s.splitlines()[0]

    coords = {(x, y): '' for x in range(4) for y in range(4)}

    pos, end, path = (0, 0), (3, 3), ''
    todo = [(pos, path)]

    def bfs(
        todo: list[tuple[tuple[int, int], str]],
        seen: set[tuple[tuple[int, int], str]] | None = None,
    ) -> int | None:
        longest_path = None
        q = deque(todo)

        if seen is None:
            seen = set()

        while q:
            pos, path = q.popleft()
            if (pos, path) not in seen:
                seen.add((pos, path))

            if pos == end:
                if longest_path is None:
                    longest_path = path
                elif len(path) > len(longest_path):
                    longest_path = path
                continue

            hash_str = hash(line + path)

            for adj, open_flag in zip(udlr_adj_4(*pos), is_open(hash_str)):
                dir_c, cand_x, cand_y = adj
                cand = (cand_x, cand_y)
                if cand in coords and open_flag:
                    q.append((cand, path + dir_c))
        return len(longest_path) if longest_path is not None else None

    return bfs(todo)


INPUT_S0 = """\
hijkl
"""
EXPECTED0 = None

INPUT_S1 = """\
ihgpwlah
"""
EXPECTED1 = 370

INPUT_S2 = """\
kglvqrro
"""
EXPECTED2 = 492

INPUT_S3 = """\
ulqzkmiv
"""
EXPECTED3 = 830


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S0, EXPECTED0),
        (INPUT_S1, EXPECTED1),
        (INPUT_S2, EXPECTED2),
        (INPUT_S3, EXPECTED3),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
