from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

WIDTH, HEIGHT = 50, 6


def rect(
    a: int, b: int, coords: dict[tuple[int, int],  str],
) -> dict[tuple[int, int], str]:
    for y in range(b):
        for x in range(a):
            coords[(x, y)] = '#'
    return coords


def rotate(
    kind: str, a: int, b: int, coords: dict[tuple[int, int], str],
) -> dict[tuple[int, int], str]:

    new_coords = coords.copy()
    if kind == 'row':
        shifted_indices = {
            x: (x + b) % WIDTH
            for x in range(WIDTH)
        }
        for x in range(WIDTH):
            new_coords[(shifted_indices[x], a)] = coords[(x, a)]
    elif kind == 'col':
        shifted_indices = {
            y: (y + b) % HEIGHT
            for y in range(HEIGHT)
        }
        for y in range(HEIGHT):
            new_coords[(a, shifted_indices[y])] = coords[(a, y)]
    return new_coords


def parse_instructions(
    s: str, coords: dict[tuple[int, int], str],
) -> dict[tuple[int, int], str]:
    if 'rect' in s:
        _, dim_s = s.split()
        length, width = dim_s.split('x')
        coords = rect(int(length), int(width), coords)
    elif 'col' in s:
        _, _, x_s, _, b_s = s.split()
        a, b = int(x_s.split('=')[-1]), int(b_s)
        coords = rotate('col', a, b, coords)
    elif 'row' in s:
        _, _, y_s, _, b_s = s.split()
        a, b = int(y_s.split('=')[-1]), int(b_s)
        coords = rotate('row', a, b, coords)
    else:
        raise NotImplementedError
    return coords


def compute(s: str) -> int:
    coords = {(x, y): '.' for y in range(HEIGHT) for x in range(WIDTH)}
    for line in s.splitlines():
        coords = parse_instructions(line, coords)

    return len([k for k, v in coords.items() if v == '#'])


INPUT_S = """\
rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1
"""
EXPECTED = 6


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
