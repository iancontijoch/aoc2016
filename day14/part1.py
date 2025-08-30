from __future__ import annotations

import argparse
import hashlib
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    keys: set[int] = set()
    salt = lines[0]

    i = 0
    while len(keys) < 65:
        hash_str_i = hashlib.md5(f"{salt}{i}".encode()).hexdigest()
        match = re.search(r'(\w)\1{2}', hash_str_i)
        if match:
            c = match.groups()[0]
            j = i + 1
            next_thousand = j + 999
            while j < next_thousand:
                hash_str_j = hashlib.md5(
                    f"{salt}{j}".encode(),
                ).hexdigest()

                match = re.search(c * 5, hash_str_j)
                if match:
                    keys.add(i)
                    if len(keys) == 64:
                        return i
                    break
                j += 1
        i += 1
    return 0


INPUT_S = """\
abc
"""
EXPECTED = 22728


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    ((INPUT_S, EXPECTED),),
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
