from __future__ import annotations

import argparse
import os.path
import re
from collections import deque
from collections.abc import Iterable
from collections.abc import Iterator
from typing import TypeVar

import pytest

import support

T = TypeVar('T')


INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def pairwise_4(iterable: Iterable[T]) -> Iterator[tuple[T, T, T, T]]:
    window: deque[T] = deque(maxlen=4)
    for x in iterable:
        window.append(x)
        if len(window) == 4:
            yield (window[0], window[1], window[2], window[3])


def is_abba(s: str) -> bool:
    return any(
        a != b and a == d and b == c
        for a, b, c, d in pairwise_4(s)
    )


def compute(s: str) -> int:
    lines = s.splitlines()
    totals = 0

    for line in lines:
        blocks = re.split(r'\[|\]', line)
        supernets = blocks[0::2]
        hypernets = blocks[1::2]

        if any(is_abba(seg) for seg in hypernets):
            continue
        if any(is_abba(seg) for seg in supernets):
            totals += 1

    return totals


INPUT_S_1 = '''\
abba[mnop]qrst
'''
EXPECTED_1 = 1

INPUT_S_2 = '''\
abcd[bddb]xyyx
'''
EXPECTED_2 = 0

INPUT_S_3 = '''\
aaaa[qwer]tyui
'''
EXPECTED_3 = 0

INPUT_S_4 = '''\
ioxxoj[asdfgh]zxcvbn
'''
EXPECTED_4 = 1

INPUT_S_5 = '''\
ioxxoj[asdfgh]zxcvbn[flurm]blurp
'''
EXPECTED_5 = 1

INPUT_S_6 = '''\
abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn
ioxxoj[asdfgh]zxcvbn[flurm]blurp
'''
EXPECTED_6 = 3

INPUT_S_6 = '''\
abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn
ioxxoj[asdfgh]zxcvbn[flurm]blurp
'''
EXPECTED_6 = 3

INPUT_S_7 = '''\
abba[mnopror]qrst[prrpa]
'''
EXPECTED_7 = 0


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S_1, EXPECTED_1),
        (INPUT_S_2, EXPECTED_2),
        (INPUT_S_3, EXPECTED_3),
        (INPUT_S_4, EXPECTED_4),
        (INPUT_S_5, EXPECTED_5),
        (INPUT_S_6, EXPECTED_6),
        (INPUT_S_7, EXPECTED_7),
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
