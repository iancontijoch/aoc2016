from __future__ import annotations

import argparse
import itertools
import math
import os.path
from collections import deque

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    coords = support.parse_coords(s)
    points = {int(c): pos for pos, c in coords.items() if c.isdigit()}
    spaces = [pos for pos, c in coords.items() if c != '#']

    def bfs_from(src: tuple[int, int]) -> dict[tuple[int, int], int]:
        dist = {src: 0}
        q = deque(dist)
        while q:
            pos = q.popleft()
            d = dist[pos]
            for adj in support.adjacent_4(*pos):
                if adj in spaces and adj not in dist:
                    dist[adj] = d + 1
                    q.append(adj)
        return dist

    dist_from = {k: bfs_from(pos) for k, pos in points.items()}

    # build pairwise distance matrix between numbered points
    pair = {}
    keys = sorted(points.keys())
    for a, b in itertools.combinations(keys, 2):
        da = dist_from[a].get(points[b], math.inf)
        pair[(a, b)] = pair[(b, a)] = da

    targets = [n for n in points.keys() if n != 0]
    best = float(10**9)
    for perm in itertools.permutations(targets):
        total = 0.0
        route = (0,) + perm
        ok = True
        for x, y in itertools.pairwise(route):
            dxy = pair.get((x, y), math.inf)
            if dxy == math.inf:
                ok = False
                break
            total += dxy
            if total >= best:
                ok = False
                break
        if ok and total < best:
            best = total
    return int(best) if best < math.inf else -1


INPUT_S = """\
###########
#0.1.....2#
#.#######.#
#4.......3#
###########
"""
EXPECTED = 14


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


# def dijkstra(start) -> dict[tuple[int, int], int]:
#     dist = {start: 0}
#     prev = {start, None}
#     targets = set(nums_pos)

#     todo = [(start, 0)]
#     while todo and targets:
#         pos, d = heapq.heappop(todo)
#         if d != dist.get(pos, math.inf):
#             continue

#         if coords[pos] in targets:
#             targets.remove(pos)

#         for
