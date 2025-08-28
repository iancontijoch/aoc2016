from __future__ import annotations

import argparse
import os.path
from collections import defaultdict

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str, val1: int, val2: int) -> int:
    lines = s.splitlines()
    actions = []
    answer = 0
    bots: dict[int, list[int]] = defaultdict(list)
    outputs = defaultdict(list)

    def do(from_bot: int, to_entity: str, to_id: int, val_type: str) -> bool:
        microchips = bots[from_bot]
        hi, lo = max(microchips), min(microchips)
        flag = val1 in microchips and val2 in microchips

        if val_type == 'lo':
            bots[from_bot].remove(lo)
            if to_entity == 'output':
                outputs[to_id].append(lo)
            else:
                bots[to_id].append(lo)
        else:
            bots[from_bot].remove(hi)
            if to_entity == 'output':
                outputs[to_id].append(hi)
            else:
                bots[to_id].append(hi)

        return flag

    # assign initial values
    for line in lines:
        words = line.split()
        if 'value' in line:
            val, bot = (int(x) for x in words if x.isnumeric())
            bots[bot].append(val)

    # collect actions
    for line in lines:
        words = line.split()
        if 'low' in line or 'high' in line:
            from_bot, low_to_entity, low_to_id, hi_to_entity, hi_to_id = (
                int(words[1]),
                words[5],
                int(words[6]),
                words[10],
                int(words[11]),
            )
            actions.append((from_bot, low_to_entity, low_to_id, 'lo'))
            actions.append((from_bot, hi_to_entity, hi_to_id, 'hi'))

    # execute actions
    ready_bots = [k for k, v in bots.items() if len(v) == 2]
    done = set()
    while ready_bots:
        for bot in ready_bots:
            bot_actions = [
                action for action in actions
                if action[0] == bot and action not in done
            ]
            for action in bot_actions:
                flag = do(*action)
                done.add(action)
                if flag:
                    answer = bot
        ready_bots = [k for k, v in bots.items() if len(v) == 2]
    return answer


INPUT_S = """\
value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2
"""
EXPECTED = 2


@pytest.mark.parametrize(
    ('input_s', 'val1', 'val2', 'expected'),
    ((INPUT_S, 2, 5, EXPECTED),),
)
def test(input_s: str, val1: int, val2: int, expected: int) -> None:
    assert compute(input_s, val1, val2) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read(), val1=61, val2=17))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
