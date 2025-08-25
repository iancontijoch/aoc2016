from __future__ import annotations

import argparse
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def expand_chunk(
    s: str,
    parens_re: re.Pattern[str],
    marker_re: re.Pattern[str],
) -> str:
    marker = parens_re.search(s)
    if marker is None:
        return s  # string as-is

    marker_s = marker.group()
    m = marker_re.search(marker_s)
    if m is not None:
        left, right = tuple(map(int, m.groups()))

    chunk = s[: marker.start()] + s[marker.end(): marker.end() + left] * right
    rest = s[(marker.end() + left):]

    return chunk + expand_chunk(rest, parens_re, marker_re)


def compute(s: str) -> int:
    lines = s.splitlines()
    parens_re = re.compile(r'\(\d+x\d+\)')
    marker_re = re.compile(r'\((\d+)x(\d+)\)')
    totals = 0
    for line in lines:
        totals += len(expand_chunk(line, parens_re, marker_re))

    return totals


INPUT_S1 = """\
ADVENT
"""
# EXPECTED1 = 'ADVENT'
EXPECTED1 = 6

INPUT_S2 = """\
A(1x5)BC
"""
# EXPECTED2 = 'ABBBBBC'
EXPECTED2 = 7

INPUT_S3 = """\
(3x3)XYZ
"""
# EXPECTED3 = 'XYZXYZXYZ'
EXPECTED3 = 9

INPUT_S4 = """\
A(2x2)BCD(2x2)EFG
"""
# EXPECTED4 = 'ABCBCDEFEFG'
EXPECTED4 = 11

INPUT_S5 = """\
(6x1)(1x3)A
"""
# EXPECTED5 = '(1x3)A'
EXPECTED5 = 6

INPUT_S6 = """\
X(8x2)(3x3)ABCY
"""
# EXPECTED6 = 'X(3x3)ABC(3x3)ABCY'
EXPECTED6 = 18


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S1, EXPECTED1),
        (INPUT_S2, EXPECTED2),
        (INPUT_S3, EXPECTED3),
        (INPUT_S4, EXPECTED4),
        (INPUT_S5, EXPECTED5),
        (INPUT_S6, EXPECTED6),
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
