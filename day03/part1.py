from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    seen = set()
    totals = 0
    for line in lines:
        is_valid = True
        numbers = support.parse_numbers_split(line)
        numbers_tup = tuple(numbers)
        if numbers_tup in seen:
            continue
        seen.add(numbers_tup)
        combos = (
            (0, (1, 2)),
            (1, (0, 2)),
            (2, (0, 1)),
        )

        is_valid = all(
            sum(numbers[s] for s in sides) > numbers[remaining]
            for remaining, sides in combos
        )

        if is_valid:
            totals += 1
    return totals


INPUT_S = '''\
5 10 25
'''
EXPECTED = 0


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
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
