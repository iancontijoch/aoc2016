from __future__ import annotations

import argparse
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def do(line: str, seen: set[int], index_offset: int = 0) -> int:

    # find (axb) markers
    markers = list(re.finditer(r'\(\d+x\d+\)', line))
    total = 0

    # base case - return the length of the non-marker string
    if not markers:
        return len(line)

    for marker in markers:
        # map back to the original marker position in the starting string
        # needed because the marker.start() index is based on recursed str
        starting_index = index_offset + marker.start()

        # avoid recursing over same marker twice
        if starting_index in seen:
            continue
        seen.add(starting_index)

        # (axb)________ <- window
        window_len = int(marker.group().split('x')[0][1:])
        window_start, window_end = marker.end(), marker.end() + window_len

        # b from (a x b)
        multiplier = int(marker.group().split('x')[-1][:-1])
        window = line[window_start: window_end]

        # increase offset by jumping to the next marker
        total += multiplier * do(window, seen, index_offset + marker.end())

    return total


def non_window_lengths(line: str) -> int:
    seen = set()
    possible = set(range(len(line)))
    markers = [m for m in re.finditer(r'\(\d+x\d+\)', line)]
    for marker in markers:
        window_len = int(marker.group().split('x')[0][1:])
        window_end = marker.end() + window_len

        for x in range(marker.start(), window_end):
            seen.add(x)

    return len(possible - seen)


def compute(s: str) -> int:
    lines = s.splitlines()
    totals = 0
    seen: set[int] = set()

    for line in lines:
        total = do(line, seen, 0)
        strays = non_window_lengths(line)
        totals += total + strays

    return totals


INPUT_S1 = """\
(3x3)XYZ
"""
# EXPECTED1 = 'XYZXYZXYZ'
EXPECTED1 = 9

INPUT_S2 = """\
X(8x2)(3x3)ABCY
"""
# EXPECTED2 = 'XABCABCABCABCABCABCY'
EXPECTED2 = len('XABCABCABCABCABCABCY')

INPUT_S3 = """\
(27x12)(20x12)(13x14)(7x10)(1x12)A
"""
# EXPECTED3 = 'A' * 241920
EXPECTED3 = 241920

INPUT_S4 = """\
(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN
"""
# EXPECTED4 = 'ABCBCDEFEFG'
EXPECTED4 = 445

# INPUT_S5 = """\
# (6x1)(1x3)A
# """
# # EXPECTED5 = '(1x3)A'
# EXPECTED5 = 6

# INPUT_S6 = """\
# X(8x2)(3x3)ABCY
# """
# # EXPECTED6 = 'X(3x3)ABC(3x3)ABCY'
# EXPECTED6 = 18


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S1, EXPECTED1),
        (INPUT_S2, EXPECTED2),
        (INPUT_S3, EXPECTED3),
        (INPUT_S4, EXPECTED4),
        # (INPUT_S5, EXPECTED5),
        # (INPUT_S6, EXPECTED6),
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
