from __future__ import annotations

import argparse
import itertools
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    size = int(s.splitlines()[0])
    inventory = {n: 1 for n in range(1, size + 1)}
    it = itertools.cycle(range(1, size + 1))
    skipped = set()
    while True:
        pos = next(it)
        if inventory[pos] == 0:
            continue

        while True:
            next_pos = next(it)
            if inventory[next_pos] != 0:
                break

        inventory[pos] += inventory[next_pos]
        inventory[next_pos] = 0
        skipped.add(next_pos)

        done = len(skipped) == size - 1
        if done:
            return pos


INPUT_S = """\
5
"""
EXPECTED = 3


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
