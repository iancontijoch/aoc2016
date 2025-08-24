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


def pairwise_3(iterable: Iterable[T]) -> Iterator[tuple[T, T, T]]:
    window: deque[T] = deque(maxlen=3)
    for x in iterable:
        window.append(x)
        if len(window) == 3:
            yield (window[0], window[1], window[2])


def is_aba(a: str, b: str, c: str) -> bool:
    return a != b and a == c


def get_bab(a: str, b: str, c: str) -> str:
    return b + a + b


def is_valid(line: str) -> bool:
    blocks = re.split(r'\[|\]', line)
    supernets = blocks[0::2]
    hypernets = blocks[1::2]

    for seg_super in supernets:
        for trio in pairwise_3(seg_super):
            if is_aba(*trio):
                for seg_hyper in hypernets:
                    if get_bab(*trio) in seg_hyper:
                        return True
    return False


def compute(s: str) -> int:
    lines = s.splitlines()
    totals = 0

    for line in lines:
        if is_valid(line):
            totals += 1

    return totals


INPUT_S_1 = '''\
aba[bab]xyz
'''
EXPECTED_1 = 1

INPUT_S_2 = '''\
xyx[xyx]xyx
'''
EXPECTED_2 = 0

INPUT_S_3 = '''\
aaa[kek]eke
'''
EXPECTED_3 = 1

INPUT_S_4 = '''\
zazbz[bzb]cdb
'''
EXPECTED_4 = 1


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S_1, EXPECTED_1),
        (INPUT_S_2, EXPECTED_2),
        (INPUT_S_3, EXPECTED_3),
        (INPUT_S_4, EXPECTED_4),
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
