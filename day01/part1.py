from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def dist(x1: int, y1: int, x2: int, y2: int):
    return abs(x2 - x1) + abs(y2 - y1)

def compute(s: str) -> int:
    pos, dir = ((0, 0), support.Direction4.UP)
    line_s = s.splitlines()[0]
    steps = [(s[0], int(s[1:])) for s in line_s.split(', ')]
    for lr, n in steps:
        dir = dir.cw if lr == 'R' else dir.ccw
        pos = dir.apply(*pos, n=n)
    
    return dist(0, 0, *pos)
        
        
        


INPUT_S_1 = '''\
R2, L3
'''
EXPECTED_1 = 5

INPUT_S_2 = '''\
R2, R2, R2
'''
EXPECTED_2 = 2

INPUT_S_3 = '''\
R5, L5, R5, R3
'''
EXPECTED_3 = 12


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S_1, EXPECTED_1),
        (INPUT_S_2, EXPECTED_2),
        (INPUT_S_3, EXPECTED_3),
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
