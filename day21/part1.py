from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def swap_positions(s: str, x: int, y: int) -> str:
    cx, cy = s[x], s[y]
    if x <= y:
        return s[:x] + cy + s[x+1:y] + cx + s[y+1:]
    else:
        return s[:y] + cx + s[y+1:x] + cy + s[x+1:]


def swap_letters(s: str, a: str, b: str) -> str:
    ai, bi = s.index(a), s.index(b)

    return swap_positions(s, ai, bi)


def reverse(s: str, x: int, y: int) -> str:
    return s[:x] + s[x:y+1][::-1] + s[y+1:]


def rotate_step(s: str, d: str, x: int) -> str:
    x = x % len(s)
    if d == 'left':
        return s[x:] + s[:x]
    else:
        return s[-x:] + s[:-x]


def rotate_based(s: str, a: str) -> str:
    i = s.index(a)
    n = 1 + i + int(i >= 4)
    s = rotate_step(s, 'right', n)
    return s


def move(s: str, x: int, y: int) -> str:
    cx = s[x]
    s = s[:x] + s[x+1:]  # remove at index x
    s = s[:y] + cx + s[y:]
    return s


def compute(s: str, word: str) -> str:
    lines = s.splitlines()
    for line in lines:
        if 'swap' in line:
            if 'position' in line:
                _, _, x, _, _, y = line.split()
                word = swap_positions(word, int(x), int(y))
            elif 'letter' in line:
                _, _, a, _, _, b = line.split()
                word = swap_letters(word, a, b)
            else:
                raise ValueError
        elif 'reverse' in line:
            _, _, x, _, y = line.split()
            word = reverse(word, int(x), int(y))
        elif 'rotate' in line:
            if 'step' in line:
                _, d, x, _ = line.split()
                word = rotate_step(word, d, int(x))
            elif 'based' in line:
                *_, a = line.split()
                word = rotate_based(word, a)
            else:
                raise ValueError
        elif 'move' in line:
            _, _, x, _, _, y = line.split()
            word = move(word, int(x), int(y))
        else:
            raise ValueError
    return word


INPUT_S = '''\
swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 step
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d
'''
WORD = 'abcde'
EXPECTED = 'decab'


@pytest.mark.parametrize(
    ('input_s', 'x', 'y', 'expected'),
    (
        ('abcde', 4, 0, 'ebcda'),
    ),
)
def test_swap_positions(input_s: str, x: int, y: int, expected: str) -> None:
    assert swap_positions(input_s, x, y) == expected


@pytest.mark.parametrize(
    ('input_s', 'a', 'b', 'expected'),
    (
        ('ebcda', 'd', 'b', 'edcba'),
    ),
)
def test_swap_letters(input_s: str, a: str, b: str, expected: str) -> None:
    assert swap_letters(input_s, a, b) == expected


@pytest.mark.parametrize(
    ('input_s', 'x', 'y', 'expected'),
    (
        ('edcba', 0, 4, 'abcde'),
    ),
)
def test_reverse(input_s: str, x: int, y: int,  expected: str) -> None:
    assert reverse(input_s, x, y) == expected


@pytest.mark.parametrize(
    ('input_s', 'd', 'x', 'expected'),
    (
        ('abcde', 'left', 1, 'bcdea'),
        ('abcde', 'left', 2, 'cdeab'),
        ('abcde', 'left', 5, 'abcde'),
        ('abcde', 'left', 6, 'bcdea'),
        ('abcde', 'right', 1, 'eabcd'),
        ('abcde', 'right', 2, 'deabc'),

    ),
)
def test_rotate_step(input_s: str, d: str, x: int,  expected: str) -> None:
    assert rotate_step(input_s, d, x) == expected


@pytest.mark.parametrize(
    ('input_s', 'a', 'expected'),
    (
        ('abdec', 'b', 'ecabd'),
        ('ecabd', 'd', 'decab'),
    ),
)
def test_rotate_based(input_s: str, a: str, expected: str) -> None:
    assert rotate_based(input_s, a) == expected


@pytest.mark.parametrize(
    ('input_s', 'x', 'y', 'expected'),
    (
        # ('bcdea', 1, 4, 'bdeac'),
        ('bdeac', 3, 0, 'abdec'),
    ),
)
def test_move(input_s: str, x: int, y: int, expected: str) -> None:
    assert move(input_s, x, y) == expected


@pytest.mark.parametrize(
    ('input_s', 'word', 'expected'),
    (
        (INPUT_S, WORD, EXPECTED),
    ),
)
def test(input_s: str, word: str, expected: int) -> None:
    assert compute(input_s, word) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read(), 'abcdefgh'))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
