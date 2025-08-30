from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    todo = []
    for line in lines:
        first, rest = line.split(';')
        n_pos = int(first.split()[3])
        pos = int(rest.split()[-1][:-1])
        todo.append((n_pos, pos))

    # part 2 disc
    todo.append((11, 0))
    t = 0
    while True:
        if all(
            (pos + t + (i + 1)) % n_pos == 0
            for i, (n_pos, pos) in enumerate(todo)
        ):
            break
        t += 1
    return t


INPUT_S = """\
Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.
"""
EXPECTED = 5


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
