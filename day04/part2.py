from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def shift(n: int) -> int:
    if n == 32:
        return 45
    elif n == 45:
        return 32
    elif n < 97:
        raise NotImplementedError
    elif n == 122:
        return 97
    else:
        return n + 1


def cycle(word: str, times: int) -> str:
    for _ in range(times):
        word = ''.join(chr(shift(ord(x))) for x in word)
    return word


def compute(s: str) -> int:
    lines = s.splitlines()
    for line in lines:
        bracket_index = line.find('[')
        letters = ''.join(
            x for x in line[:bracket_index - 1]
            if x == '-' or x.isalpha()
        )
        sector_id = int(
            ''.join(x for x in line[:bracket_index] if x.isnumeric()),
        )
        decrypted = cycle(letters, sector_id)
        print(decrypted, sector_id)
    return 0


INPUT_S_1 = """\
qzmt-zixmtkozy-ivhz-343[qzmts]
"""
EXPECTED_1 = 'very encrypted name'


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S_1, EXPECTED_1),
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
