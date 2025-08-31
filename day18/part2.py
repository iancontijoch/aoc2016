from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

TRAP_VALUES = (
    ('^', '^', '.'),
    ('.', '^', '^'),
    ('^', '.', '.'),
    ('.', '.', '^'),
)


def compute(s: str, n_rows: int = 1) -> int:
    line = s.splitlines()[0]
    ret = line
    totals = line.count('.')
    print_s = line + '\n'

    def get_row(line: str) -> str:
        ret = ''
        for i, center in enumerate(line):
            left = line[i - 1] if i - 1 >= 0 else '.'
            right = line[i + 1] if i + 1 < len(line) else '.'
            ret += '^' if (left, center, right) in TRAP_VALUES else '.'
        return ret

    for _ in range(n_rows - 1):
        ret = get_row(ret)
        totals += ret.count('.')
        print_s += ret + '\n'
    return totals


INPUT_S_1 = '''\
..^^.
'''
INPUT_N_ROWS_1 = 3
# EXPECTED_1 = '''\
# ..^^.
# .^^^^
# ^^..^
# '''
EXPECTED_1 = 6

INPUT_S_2 = '''\
.^^.^.^^^^
'''
INPUT_N_ROWS_2 = 10
# EXPECTED_2 = '''\
# .^^.^.^^^^
# ^^^...^..^
# ^.^^.^.^^.
# ..^^...^^^
# .^^^^.^^.^
# ^^..^.^^..
# ^^^^..^^^.
# ^..^^^^.^^
# .^^^..^.^^
# ^^.^^^..^^
# '''
EXPECTED_2 = 38


@pytest.mark.parametrize(
    ('input_s', 'input_n_rows', 'expected'),
    (
        (INPUT_S_1, INPUT_N_ROWS_1, EXPECTED_1),
        (INPUT_S_2, INPUT_N_ROWS_2, EXPECTED_2),
    ),
)
def test(input_s: str, input_n_rows: int, expected: int) -> None:
    assert compute(input_s, input_n_rows) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read(), 400000))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
