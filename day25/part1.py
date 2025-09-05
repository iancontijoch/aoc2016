from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    # this one is all gpt generated; i was saturated with assembunny
    def assembunny_sim(start_a: int, max_outputs: int = 20) -> list[int]:
        """
        Simulates the assembunny program.
        start_a: initial value of register a
        max_outputs: how many 'out' values to produce before stopping
        """
        # Step 1: initialization
        a = start_a
        d = a
        b = 643

        # Step 2: d = a + 643*4
        d = a + 643 * 4

        # Step 3: copy back
        a = d

        outputs: list[int] = []

        # Step 4: main output loop
        while len(outputs) < max_outputs:
            b = a      # copy current number
            a = 0      # reset a

            # Simulate: while b > 0: a, b = divmod(b, 2)
            while b > 0:
                if b >= 2:
                    # subtract 2 repeatedly
                    count = b // 2
                    a += count
                    b -= 2 * count
                else:
                    # remainder left
                    break

            # At this point:
            #   a = original_b // 2
            #   b = original_b % 2

            # out b
            outputs.append(b)

            # loop condition: jnz a -19 / jnz 1 -21
            if a == 0:
                break
            # continue with new a
        return outputs

    curr_a = 0
    span = 10
    while True:
        out = (assembunny_sim(curr_a, span))
        if out == [0, 1] * (span // 2):
            break
        curr_a += 1
    return curr_a


INPUT_S = '''\

'''
EXPECTED = 1


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
