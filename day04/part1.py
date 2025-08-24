from __future__ import annotations

import argparse
import os.path
from collections import Counter

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    totals = 0
    for line in lines:
        bracket_index = line.find('[')
        letters = [x for x in line[:bracket_index] if x != '-' and x.isalpha()]
        sector_id = int(
            ''.join(x for x in line[:bracket_index] if x.isnumeric()),
        )
        checksum = line[bracket_index + 1: -1]

        correct = ''.join(
            x
            for (x, _) in sorted(
                Counter(letters).most_common(),
                key=lambda x: (-x[1], x[0]),
            )
        )
        if checksum == correct[:5]:
            totals += sector_id
    return totals


INPUT_S_1 = """\
aaaaa-bbb-z-y-x-123[abxyz]
"""
EXPECTED_1 = 123

INPUT_S_2 = """\
a-b-c-d-e-f-g-h-987[abcde]
"""
EXPECTED_2 = 987

INPUT_S_3 = """\
not-a-real-room-404[oarel]
"""
EXPECTED_3 = 404

INPUT_S_4 = """\
totally-real-room-200[decoy]
"""
EXPECTED_4 = 0

INPUT_S_5 = """\
aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]
"""
EXPECTED_5 = 123 + 987 + 404


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S_1, EXPECTED_1),
        (INPUT_S_2, EXPECTED_2),
        (INPUT_S_3, EXPECTED_3),
        (INPUT_S_4, EXPECTED_4),
        (INPUT_S_5, EXPECTED_5),
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
