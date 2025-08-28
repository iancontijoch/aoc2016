from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    regs = {x: 0 for x in 'abcd'}
    i = 0
    j = len(lines)
    while i < j:
        line = lines[i]
        if 'jnz' in line:
            _, x_s, y_s = line.split()
            x = int(x_s) if x_s.isnumeric() else regs.get(x_s, 0)
            y = int(y_s)

            i += 1 if x == 0 else y
            continue
        elif 'cpy' in line:
            _, x_s, y_s = line.split()
            x = int(x_s) if x_s.isnumeric() else regs.get(x_s, 0)
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
cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a
'''
EXPECTED = 42


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
