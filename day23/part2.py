from __future__ import annotations

import argparse
import os.path
from typing import TypeAlias

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

Reg: TypeAlias = dict[str, int]


def is_int(s: str) -> bool:
    return s.lstrip('-').isdigit()


def value(x: str, regs: Reg) -> int:
    if isinstance(x, int):
        return x
    if is_int(x):
        return int(x)
    return regs[x]


def invert(s: str) -> str:
    parts = s.split()
    match parts:
        case []:
            raise ValueError('empty instruction')
        case ['inc' | 'dec' | 'tgl' as op, dst]:
            one_arg_toggle = {'inc': 'dec', 'dec': 'inc', 'tgl': 'inc'}
            return f"{one_arg_toggle[op]} {dst}"
        case ['cpy', src, dst]:
            return f"jnz {src} {dst}"
        case ['jnz', x, y]:
            return 'skip' if is_int(y) else f"cpy {x} {y}"
        case [op, *_]:
            raise ValueError(f"unknown op {op}")
    raise ValueError


def _is_reg(s: str) -> bool:
    return s.isalpha() and len(s) == 1


def _tok(line: str) -> list[str]:
    return line.split()


def optimize(program: list[str], ip: int, regs: Reg) -> int | None:
    n = len(program)

    # add-loop: inc X; dec Y; jnz Y -2
    if ip + 2 < n:
        t0 = _tok(program[ip])
        t1 = _tok(program[ip + 1])
        t2 = _tok(program[ip + 2])
        if (
            t0[:1] == ['inc']
            and len(t0) == 2
            and _is_reg(t0[1])
            and t1[:1] == ['dec']
            and len(t1) == 2
            and _is_reg(t1[1])
            and t2 == ['jnz', t1[1], '-2']
            and t0[1] != t1[1]
        ):
            X, Y = t0[1], t1[1]
            regs[X] += regs[Y]
            regs[Y] = 0
            return ip + 3

    # mul-loop: cpy B C; inc A; dec C; jnz C -2; dec D; jnz D -5
    if ip + 5 < n:
        t0 = _tok(program[ip + 0])
        t1 = _tok(program[ip + 1])
        t2 = _tok(program[ip + 2])
        t3 = _tok(program[ip + 3])
        t4 = _tok(program[ip + 4])
        t5 = _tok(program[ip + 5])
        if (
            t0[:1] == ['cpy']
            and len(t0) == 3
            and _is_reg(t0[1])
            and _is_reg(t0[2])
            and t1[:1] == ['inc']
            and len(t1) == 2
            and _is_reg(t1[1])
            and t2 == ['dec', t0[2]]
            and t3 == ['jnz', t0[2], '-2']
            and t4[:1] == ['dec']
            and len(t4) == 2
            and _is_reg(t4[1])
            and t5 == ['jnz', t4[1], '-5']
        ):
            B, C = t0[1], t0[2]
            A = t1[1]
            D = t4[1]
            regs[A] += regs[B] * regs[D]
            regs[C] = 0
            regs[D] = 0
            return ip + 6

    return None


def run(program: list[str], regs: Reg) -> Reg:
    i = 0
    n = len(program)
    while 0 <= i < n:
        j = optimize(program, i, regs)
        if j is not None:
            i = j
            continue

        op, *args = program[i].split()
        if op == 'cpy':
            src, dst = args
            if dst.isalpha():
                regs[dst] = value(src, regs)
            i += 1
        elif op == 'inc':
            (dst,) = args
            regs[dst] += 1
            i += 1
        elif op == 'dec':
            (dst,) = args
            regs[dst] -= 1
            i += 1
        elif op == 'jnz':
            cond, off = args
            i += value(off, regs) if value(cond, regs) != 0 else 1
        elif op == 'tgl':
            (off,) = args
            idx = i + value(off, regs)
            if 0 <= idx < n:
                program[idx] = invert(program[idx])
            i += 1
        elif op == 'skip':
            i += 1
        else:
            raise ValueError(f"unknown op {op}")
    return regs


def compute(s: str) -> int:
    lines = s.splitlines()
    regs = {'a': 12, 'b': 0, 'c': 0, 'd': 0}
    final_regs = run(program=lines, regs=regs)
    return final_regs['a']


INPUT_S = """\
cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a
"""
EXPECTED = 3


@pytest.mark.parametrize(('input_s', 'expected'), ((INPUT_S, EXPECTED),))
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
