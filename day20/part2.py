from __future__ import annotations

import argparse
import itertools
import os.path
from collections import deque

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def range_isin(check: range, isin: range) -> bool:
    return check.start >= isin.start and check.stop <= isin.stop


def merge(a: range, b: range) -> range:
    if a.start > b.start:
        raise ValueError

    # a < b; no overlap -- return leftmost
    if a.start < b.start and a.stop < b.start:
        return a

    # b > a; overlap
    elif a.start <= b.start and a.stop < b.stop:
        return range(a.start, b.stop)

    # b < a; no overlap shouldn't happen because we sorted
    elif b.start > b.start:
        raise ValueError
    # b < a; overlap
    elif a.start <= b.start and a.stop > b.stop:
        return a
    # b == a
    elif a == b:
        return a
    else:
        raise NotImplementedError


def consolidate(lst: list[range]) -> list[range]:
    lst.sort(key=lambda x: (x.start, x.stop))
    ret = []
    q = deque(lst)
    while q:
        if len(q) == 1:
            a = q.popleft()
            if a not in ret:
                ret.append(a)
            break
        a, b = q.popleft(), q.popleft()
        cand = merge(a, b)

        if cand == a:
            if a not in ret:
                ret.append(a)
            if range_isin(check=b, isin=a):
                # ignore b and pop a back in
                q.appendleft(a)
            else:
                # a is non-overlapping with b, so pop b back in
                q.appendleft(b)
        elif cand == b:
            ret.append(b)
            q.appendleft(b)
        else:
            # the cand is a new, merged range
            ret.append(cand)
            q.appendleft(cand)

    return ret


def compute(s: str, max_n: int) -> int:
    totals = 0
    lines = s.splitlines()
    gaps: list[range] = []

    # get ranges
    seen: list[range] = []
    for line in lines:
        start, end = map(int, line.split('-'))
        seen.append(range(start, end + 1))

    # sort ranges by start and stop
    seen.sort(key=lambda x: (x[0], x[1]))

    # consolidate overlapping ranges
    seen = consolidate(seen)

    # detect gaps
    for a, b in itertools.pairwise(seen):
        if b.start > a.stop:
            gaps.append(range(a.stop, b.start))

    # add any gaps between last range and the max
    gaps.append(range(seen[-1].stop, max_n + 1))
    gaps.sort(key=lambda x: (x.start))

    # count gaps
    for a, b in itertools.pairwise(gaps):
        if a.stop < b.start:  # no overlap
            totals += len(a)
        else:
            raise ValueError

    # get length of final gap
    totals += len(gaps[-1])
    return totals


INPUT_S = """\
5-8
0-2
4-7
"""
MAX_N = 9
EXPECTED = 2

INPUT_S2 = """\
5-6
0-1
4-7
"""
MAX_N2 = 9
EXPECTED2 = 4


@pytest.mark.parametrize(
    ('input_s', 'max_n', 'expected'),
    (
        (INPUT_S, MAX_N, EXPECTED),
        (INPUT_S2, MAX_N2, EXPECTED2),
    ),
)
def test(input_s: str, max_n: int, expected: int) -> None:
    assert compute(input_s, max_n) == expected


@pytest.mark.parametrize(
    ('lst', 'expected'),
    (
        (
            [range(0, 5), range(7, 10), range(3, 6)],
            [range(0, 6), range(7, 10)],
        ),
        ([range(0, 5), range(4, 10)], [range(0, 10)]),
        ([range(4, 10), range(2, 8)], [range(2, 10)]),
        ([range(4, 10)], [range(4, 10)]),
        ([range(0, 5), range(0, 10)], [range(0, 10)]),
        ([range(0, 10), range(2, 5)], [range(0, 10)]),
        ([range(0, 10), range(0, 5)], [range(0, 10)]),
        (
            [range(0, 2), range(3, 4), range(10, 20)],
            [range(0, 2), range(3, 4), range(10, 20)],
        ),
    ),
)
def test_consolidate(lst: list[range], expected: int) -> None:
    assert consolidate(lst) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read(), max_n=4294967295))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
