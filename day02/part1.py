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
    (0, 0): 1,
    (1, 0): 2,
    (2, 0): 3,
    (0, 1): 4, 
    (1, 1): 5,
    (2, 1): 6,
    (0, 2): 7,
    (1, 2): 8,
    (2, 2): 9,
}

def compute(s: str) -> int:
    lines = s.splitlines()
    
    coords = {
        (x, y)
        for y in range(3)
        for x in range(3)
    }
    
    pos = (1, 1)
    res = ''
    for line in lines:
        for d in line:
            cand = dirs.get(d).apply(*pos)
            pos = cand if cand in coords else pos
        res += str(keypad.get(pos))
    return int(res)


INPUT_S = '''\
ULL
RRDDD
LURDL
UUUUD
'''
EXPECTED = 1985


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
