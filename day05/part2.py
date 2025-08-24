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
    password = [''] * 8

    while '' in password:
        cand = line + str(index)
        cand_hex = hashlib.md5(cand.encode('utf-8')).hexdigest()
        if cand_hex[:5] == '00000':
            pos_s, char = cand_hex[5], cand_hex[6]
            if not pos_s.isnumeric():
                index += 1
                continue
            pos = int(pos_s)
            if pos in range(8):
                if password[pos] == '':
                    password[pos] = char
        index += 1
    ret = ''.join(password)
    return ret


INPUT_S = '''\
abc
'''
EXPECTED = '05ace8e3'


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
