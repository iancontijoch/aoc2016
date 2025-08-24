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
    for pair_4 in pairwise_4(s):
        left, right = pair_4[:2], pair_4[2:]
        if left[0] == left[1]:
            continue
        if left == right[::-1]:
            return True
    return False


def compute(s: str) -> int:
    lines = s.splitlines()
    totals = 0
    pattern_re = re.compile(r'\[[a-z]+\]')

    for line in lines:
        sequences: list[tuple[int, int]] = []
        letter_blocks: list[tuple[int, int]] = []
        end = 0
        spans_it = pattern_re.finditer(line)
        while True:
            try:
                span = next(spans_it)
                # remove the brackets from the span
                sequences.append((span.start() + 1, span.end() - 1))
                if letter_blocks:
                    # end of the previous sequence to start of the next
                    letter_blocks.append((end, span.start()))
                else:
                    # add the first letter block
                    letter_blocks.append((0, span.start()))
                end = span.end()
            except StopIteration:
                break
        # end of last sequence thru end
        letter_blocks.append((sequences[-1][1] + 1, len(line)))
        if any(is_abba(line[start:end]) for start, end in sequences):
            continue

        if any(is_abba(line[start:end]) for start, end in letter_blocks):
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
