from __future__ import annotations

import argparse
import itertools
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def expand(a: str, max_len: int) -> str:
    while len(a) < max_len:
        b = a[::-1].replace('0', 'z').replace('1', '0').replace('z', '1')
        a += '0' + b
    return a


def checksum(s: str) -> str:
    ret = ''
    for a, b in itertools.batched(s, 2):
        ret += '1' if a == b else '0'

    if len(ret) % 2 == 0:
        return checksum(ret)
    return ret


def compute(s: str, max_len: int) -> str:
    line = s.splitlines()[0]
    return checksum(expand(line, max_len)[:max_len])


INPUT_S_1 = """\
110010110100
"""
MAX_LEN_1 = 12
EXPECTED_1 = '100'

INPUT_S_2 = """\
10000
"""
MAX_LEN_2 = 20
EXPECTED_2 = '01100'


@pytest.mark.parametrize(
    ('input_s', 'max_len', 'expected'),
    (
        ('1', 3, '100'),
        ('0', 3, '001'),
        ('11111', 11, '11111000000'),
        ('111100001010', 25, '1111000010100101011110000'),
        ('10000', 20, '10000011110010000111110'),
    ),
)
def test_expand(input_s: str, max_len: int, expected: int) -> None:
    assert expand(input_s, max_len) == expected


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('110010110100', '100'),
    ),
)
def test_checksum(input_s: str, expected: int) -> None:
    assert checksum(input_s) == expected


@pytest.mark.parametrize(
    ('input_s', 'max_len', 'expected'),
    (
        (INPUT_S_1, MAX_LEN_1, EXPECTED_1),
        (INPUT_S_2, MAX_LEN_2, EXPECTED_2),
    ),
)
def test(input_s: str, max_len: int, expected: int) -> None:
    assert compute(input_s, max_len) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read(), max_len=272))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
