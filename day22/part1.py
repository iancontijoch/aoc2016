from __future__ import annotations

import argparse
import itertools
import os.path
from dataclasses import dataclass

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


@dataclass
class Filesystem:
    x: int
    y: int
    name: str
    size: int
    used: int
    avail: int
    use: int


def compute(s: str) -> int:
    lines = s.splitlines()[2:]
    viable: set[tuple[tuple[int, int], tuple[int, int]]] = set()

    coords: dict[tuple[int, int], Filesystem] = {
        (x, y): Filesystem(x, y, 'foo', 0, 0, 0, 0)
        for x in range(31)
        for y in range(31)
    }

    for line in lines:
        node_s, size_s, used_s, avail_s, use_s = line.split()
        size = int(size_s[:-1])
        used = int(used_s[:-1])
        avail = int(avail_s[:-1])
        use = int(use_s[:-1])

        _, x_s, y_s = node_s.split('-')
        x, y = int(x_s[1:]), int(y_s[1:])
        coords[(x, y)] = Filesystem(x, y, node_s, size, used, avail, use)

    for x1, y1 in itertools.product(range(31), repeat=2):
        for x2, y2 in itertools.product(range(31), repeat=2):

            a, b = coords[(x1, y1)], coords[(x2, y2)]
            if a.used != 0 and a.name != b.name and a.used <= b.avail:
                viable.add(((a.x, a.y), (b.x, b.y)))
    return len(viable)


INPUT_S = '''\

'''
EXPECTED = 1


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
