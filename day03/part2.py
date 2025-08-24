from __future__ import annotations

import argparse
import itertools
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    seen = set()
    totals = 0

    numbers = list(
        itertools.chain.from_iterable(
            support.parse_numbers_split(line) for line in lines
        ),
    )
    col1, col2, col3 = numbers[::3], numbers[1::3], numbers[2::3]

    triangles = itertools.chain.from_iterable((
        itertools.batched(col1, n=3),
        itertools.batched(col2, n=3),
        itertools.batched(col3, n=3),
    ))

    for triangle in triangles:
        is_valid = True
        if triangle in seen:
            continue
        seen.add(triangle)
        combos = (
            (0, (1, 2)),
            (1, (0, 2)),
            (2, (0, 1)),
        )

        is_valid = all(
            sum(triangle[s] for s in sides) > triangle[remaining]
            for remaining, sides in combos
        )

        if is_valid:
            totals += 1

    return totals


INPUT_S = """\
101 301 501
102 302 502
103 303 503
201 401 601
202 402 602
203 403 603
"""
EXPECTED = 6


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    ((INPUT_S, EXPECTED),),
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
