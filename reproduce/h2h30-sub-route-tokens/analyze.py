#!/usr/bin/env python3
"""Reproduce the h2h30-sub-route-tokens numbers from runs.csv (standard library only).

Comparisons are same model and same effort only: loop-medium vs Codex-medium,
loop-high vs Codex-high. Equivalent tokens = uncached input + 0.1 x cached input
+ 4 x output. Sign tests are two-sided exact binomial tests over tasks (ties dropped).
"""
import csv
import math
import os
import statistics as st
from decimal import Decimal, ROUND_HALF_UP

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    with open(os.path.join(HERE, 'runs.csv'), newline='') as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        for k in ('passed', 'input_tokens', 'cached_input_tokens', 'output_tokens', 'reasoning_tokens', 'requests'):
            r[k] = int(r[k])
        r['wall_s'] = float(r['wall_s'])
        r['uncached'] = r['input_tokens'] - r['cached_input_tokens']
        r['equivalent'] = r['uncached'] + 0.1 * r['cached_input_tokens'] + 4 * r['output_tokens']
    return rows


def sign_p(wins, losses):
    n = wins + losses
    if not n:
        return 1.0
    tail = sum(math.comb(n, k) for k in range(min(wins, losses) + 1)) / 2 ** n
    return min(1.0, 2 * tail)


def fmt_p(p):
    return f'{p:.2g}'


def half_up(x, places):
    # Round half away from zero, as the published tables do (40,746.5 -> 40,747).
    q = Decimal(1).scaleb(-places)
    return Decimal(repr(x)).quantize(q, rounding=ROUND_HALF_UP)


def main():
    rows = load()
    tasks = sorted({r['task'] for r in rows})
    print(f'tasks: {len(tasks)}  runs: {len(rows)}')
    for effort in ('medium', 'high'):
        by = {(r['tool'], r['task']): r for r in rows if r['effort'] == effort}
        loop = [by['loop', t] for t in tasks]
        codex = [by['codex', t] for t in tasks]
        print(f'\n== {effort} (loop vs Codex, same model and effort) ==')
        eqs = {}
        for name, rs in (('loop', loop), ('codex', codex)):
            passes = sum(r['passed'] for r in rs)
            inp = sum(r['input_tokens'] for r in rs)
            cached = sum(r['cached_input_tokens'] for r in rs)
            out = sum(r['output_tokens'] for r in rs)
            eq = (inp - cached + 0.1 * cached + 4 * out) / passes
            eqs[name] = eq
            walls = [r['wall_s'] for r in rs]
            print(f'{name:5} pass {passes}/{len(rs)}  wall median {half_up(st.median(walls), 2)} s  mean {st.mean(walls):.1f} s  '
                  f'eq tokens/pass {half_up(eq, 0):,}  uncached/pass {half_up((inp - cached) / passes, 0):,}  '
                  f'input total {inp / 1e6:.2f}M  output total {out / 1e3:.0f}k')
        print(f"loop/codex equivalent tokens per pass {eqs['loop'] / eqs['codex']:.1%}")
        pass_w = sum(a['passed'] > b['passed'] for a, b in zip(loop, codex))
        pass_l = sum(a['passed'] < b['passed'] for a, b in zip(loop, codex))
        print(f'pass per task loop/codex wins {pass_w}/{pass_l}, sign p={sign_p(pass_w, pass_l):.1f}')
        rel = [a['wall_s'] / b['wall_s'] - 1 for a, b in zip(loop, codex)]
        absd = [a['wall_s'] - b['wall_s'] for a, b in zip(loop, codex)]
        w = sum(a['wall_s'] < b['wall_s'] for a, b in zip(loop, codex))
        l = sum(a['wall_s'] > b['wall_s'] for a, b in zip(loop, codex))
        print(f'wall median paired delta {st.median(rel):+.1%} ({st.median(absd):+.1f} s); '
              f'task wins loop/codex {w}/{l}, p={fmt_p(sign_p(w, l))}')
        for key, label in (('equivalent', 'equivalent tokens'), ('uncached', 'uncached input')):
            w = sum(a[key] < b[key] for a, b in zip(loop, codex))
            l = sum(a[key] > b[key] for a, b in zip(loop, codex))
            print(f'{label}: task wins loop/codex {w}/{l}, p={fmt_p(sign_p(w, l))}')
        ratios = [a['equivalent'] / b['equivalent'] for a, b in zip(loop, codex)]
        print(f'equivalent tokens median paired delta {st.median(ratios) - 1:+.1%}; '
              f'per-task loop/codex ratio min {min(ratios):.3f} max {max(ratios):.3f}; '
              f'loop lower on {sum(x < 1 for x in ratios)}/{len(ratios)} tasks')


if __name__ == '__main__':
    main()
