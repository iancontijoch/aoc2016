from __future__ import annotations

import argparse
import itertools
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str, max_n: int) -> int:
    lines = s.splitlines()
    gaps: list[range] = []

    seen: list[range] = []
    for line in lines:
        start, end = map(int, line.split('-'))
        seen.append(range(start, end + 1))

    seen.sort(key=lambda x: (x[0], x[1]))
    for a, b in itertools.pairwise(seen):
        if b.start > a.stop:
            gaps.append(range(a.stop, b.start))

    gaps.append(range(seen[-1].stop, max_n + 1))
    return min(gaps, key=lambda x: x[0]).start


INPUT_S = '''\
5-8
0-2
4-7
'''
MAX_N = 9
EXPECTED = 3


@pytest.mark.parametrize(
    ('input_s', 'max_n', 'expected'),
    (
        (INPUT_S, MAX_N, EXPECTED),
    ),
)
def test(input_s: str, max_n: int, expected: int) -> None:
    assert compute(input_s, max_n) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read(), max_n=4294967295))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
