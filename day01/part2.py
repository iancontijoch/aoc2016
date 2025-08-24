from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def dist(x1: int, y1: int, x2: int, y2: int) -> int:
    return abs(x2 - x1) + abs(y2 - y1)


def compute(s: str) -> int:
    pos, dir = ((0, 0), support.Direction4.UP)
    seen = set()
    line_s = s.splitlines()[0]
    steps = [(s[0], int(s[1:])) for s in line_s.split(', ')]
    for lr, n in steps:
        dir = dir.cw if lr == 'R' else dir.ccw
        for _ in range(n):
            pos = dir.apply(*pos)
            if pos not in seen:
                seen.add(pos)
            else:
                return dist(0, 0, *pos)
    return dist(0, 0, *pos)


INPUT_S_1 = '''\
R8, R4, R4, R8
'''
EXPECTED_1 = 4


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S_1, EXPECTED_1),
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
