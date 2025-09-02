from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def isnumeric(s: str) -> bool:
    return '-' in s or s.isnumeric()


def invert(s: str) -> str:
    parts = s.split()
    if len(parts) == 2:
        # one-argument instructions
        ins, x_s = s.split()
        ins = 'dec' if ins == 'inc' else 'inc'
        return f'{ins} {x_s}'
    elif len(parts) == 3:
        ins, x_s, y_s = s.split()
        ins = 'cpy' if ins == 'jnz' else 'jnz'
        if ins == 'cpy' and y_s.isnumeric():
            # invalid
            return 'invalid'
        return f'{ins} {x_s} {y_s}'
    raise ValueError


def compute(s: str) -> int:
    lines = s.splitlines()
    regs = {x: 0 for x in 'abcd'}

    # puzzle input starts with 7 but test doesn't
    if 'cpy a b' in lines[0]:
        regs['a'] = 7
    i, j = 0, len(lines)
    while i < j:
        line = lines[i]
        if 'invalid' in line:
            i += 1
        elif 'jnz' in line:
            _, x_s, y_s = line.split()
            try:
                x = int(x_s) if isnumeric(x_s) else regs[x_s]
                y = int(y_s) if isnumeric(y_s) else regs[y_s]
            except KeyError:
                i += 1
                continue
            i += 1 if x == 0 else y
            continue
        elif 'tgl' in line:
            _, x_s = line.split()
            try:
                x = int(x_s) if isnumeric(x_s) else regs[x_s]
            except KeyError:
                raise
            if i+x >= len(lines):
                i += 1
                continue
            lines[i+x] = invert(lines[i+x])
        elif 'cpy' in line:
            _, x_s, y_s = line.split()
            try:
                x = int(x_s) if isnumeric(x_s) else regs[x_s]
            except KeyError:
                raise
            regs[y_s] = x
        elif 'inc' in line:
            _, x_s = line.split()
            regs[x_s] += 1
        elif 'dec' in line:
            _, x_s = line.split()
            regs[x_s] -= 1
        else:
            raise NotImplementedError
        i += 1
    return regs['a']


INPUT_S = '''\
cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a
'''
EXPECTED = 3


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
