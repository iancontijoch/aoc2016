from __future__ import annotations

import argparse
import itertools
import math
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    n = int(lines[0])
    a = 3 ** math.floor(math.log(n, 3))

    if 2 * a >= n:
        return (n - a) or n
    else:
        return 2 * n - 3 * a


def compute_manual(n: int) -> tuple[int, int, int]:
    size = n
    lst = [(n, 1) for n in range(1, size + 1)]

    i = 0
    while len(lst) > 1:
        size = len(lst)
        offset = size // 2

        across = ((i + offset) % size) or size

        _, across_val = lst[across]
        curr_elf, curr_val = lst[i]

        # take gifts and remove player
        lst[i] = (curr_elf, curr_val + across_val)
        lst = lst[:across] + lst[across + 1:]
        it = itertools.cycle(lst)
        next(it)
        lst = [next(it) for _ in range(len(lst))]

    return (n, lst[0][0], lst[0][0] - n)


INPUT_S = """\
713
"""
EXPECTED = 697


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

        # the compute_manual solution works but is slow,
        # analyzing the differences between n and output from
        # n=(1, 3001), I figured out the patten in the compute function

        # for x in range(1, 3001):
        #     (n, ans, diff) = compute_manual(x)
        #     ans2 = compute(str(x))
        #     print(n, ':', ans, ans2, ans3)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
