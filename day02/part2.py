from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

dirs = {
    'U': support.Direction4.UP,
    'D': support.Direction4.DOWN,
    'L': support.Direction4.LEFT,
    'R': support.Direction4.RIGHT,
}

keypad = {
    (0, 2): '5',
    (1, 1): '2',
    (1, 2): '6',
    (1, 3): 'A',
    (2, 0): '1',
    (2, 1): '3',
    (2, 2): '7',
    (2, 3): 'B',
    (2, 4): 'D',
    (3, 1): '4',
    (3, 2): '8',
    (3, 3): 'C',
    (4, 2): '9',

}


def compute(s: str) -> str:
    lines = s.splitlines()

    pos = (0, 2)
    res = ''
    for line in lines:
        for d in line:
            cand = dirs.get(d, support.Direction4.UP).apply(*pos)
            pos = cand if cand in keypad else pos
        res += str(keypad.get(pos))
    return res


INPUT_S = '''\
ULL
RRDDD
LURDL
UUUUD
'''
EXPECTED = '5DB3'


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
