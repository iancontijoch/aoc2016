from __future__ import annotations

import argparse
import os.path
from collections import deque
from dataclasses import dataclass
from typing import TypeAlias

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

Pos: TypeAlias = tuple[int, int]
Coords: TypeAlias = dict[Pos, 'Filesystem']
CoordsMarkers: TypeAlias = dict[Pos, str]


@dataclass
class Filesystem:
    x: int
    y: int
    name: str
    size: int
    used: int
    avail: int
    use: int

    def marker(self, coords: Coords, start: tuple[int, int]) -> str:
        can_receive = any(
            other.used <= self.avail
            for _, other in coords.items()
            if other != self and other.used != 0
        )

        can_give = any(
            other.avail >= self.used and other
            for _, other in coords.items()
            if other != self
        )

        if (self.x, self.y) == start:
            return 'G'
        elif not can_receive and can_give:
            return '.'
        elif not can_receive and not can_give:
            return '#'
        elif can_receive or not can_give:
            return '_'
        else:
            raise NotImplementedError


def compute(s: str) -> int:
    lines = s.splitlines()[2:]
    width = int(len(lines) ** 0.5)
    goal = (width - 1, 0)

    coords: dict[tuple[int, int], Filesystem] = {
        (x, y): Filesystem(x, y, 'foo', 0, 0, 0, 0)
        for x in range(width)
        for y in range(width)
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

    coords_markers = {k: v.marker(coords, goal) for k, v in coords.items()}
    empty_pos = [pos for pos, v in coords_markers.items() if v == '_'][0]

    def bfs(
        start: Pos,
        end: Pos,
        coords_markers: CoordsMarkers,
        seen: set[tuple[Pos, int]] | None = None,
    ) -> int:
        """get shortest path to the Goal"""
        todo = [(start, 0)]
        min_d = 10**9

        if seen is None:
            seen = set()

        q = deque(todo)
        while q:
            pos, d = q.popleft()
            if d > min_d:
                continue

            if pos == end:
                min_d = min(min_d, d)
                continue

            if (pos, d) in seen:
                continue

            seen.add((pos, d))
            for cand in support.adjacent_4(*pos):
                if cand in coords and coords_markers[cand] != '#':
                    q.append((cand, d + 1))
        return min_d

    # find beeline to G and minus 1 to get adj(G)
    beeline = bfs(start=empty_pos, end=goal, coords_markers=coords_markers)
    beeline -= 1

    # total = beeline + 5 moves per one shift left
    # there are (width - 2) shifts left
    # there is one final shift into the end position
    total = beeline + 5 * (width - 2) + 1
    return total


INPUT_S = """\
root@ebhq-gridcenter# df -h
Filesystem            Size  Used  Avail  Use%
/dev/grid/node-x0-y0   10T    8T     2T   80%
/dev/grid/node-x0-y1   11T    6T     5T   54%
/dev/grid/node-x0-y2   32T   28T     4T   87%
/dev/grid/node-x1-y0    9T    7T     2T   77%
/dev/grid/node-x1-y1    8T    0T     8T    0%
/dev/grid/node-x1-y2   11T    7T     4T   63%
/dev/grid/node-x2-y0   10T    6T     4T   60%
/dev/grid/node-x2-y1    9T    8T     1T   88%
/dev/grid/node-x2-y2    9T    6T     3T   66%
"""
EXPECTED = 7


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
