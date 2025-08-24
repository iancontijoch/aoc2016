from __future__ import annotations

import argparse
import hashlib
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> str:
    line = s.splitlines()[0]
    index = 0
    password = ''

    while len(password) < 8:
        cand = line + str(index)
        cand_hex = hashlib.md5(cand.encode('utf-8')).hexdigest()
        if cand_hex[:5] == '00000':
            password += cand_hex[5]
        index += 1
    return password


INPUT_S = '''\
abc
'''
EXPECTED = '18f47a30'


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
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
