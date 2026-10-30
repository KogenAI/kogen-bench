#!/usr/bin/env python3
"""Reproduce the loop-high-reasoning-api numbers from runs.csv (standard library only)."""
import csv, math, pathlib, statistics

ROWS = list(csv.DictReader(open(pathlib.Path(__file__).with_name('runs.csv'), newline='')))
TOOLS = ['loop', 'loop+reasoning-replay', 'codex']
TASKS = list(dict.fromkeys(r['task'] for r in ROWS))
M = {'wall': 'wall_s', 'requests': 'requests', 'reasoning': 'reasoning_tokens', 'output': 'output_tokens', 'usd': 'cost_usd'}
run = {(r['task'], r['tool']): {**{k: float(r[v]) for k, v in M.items()}, 'pass': r['passed'] == '1'} for r in ROWS}


def p90(v):
    v = sorted(v)
    return v[max(0, math.ceil(.9 * len(v)) - 1)]


def sign(a, b):
    w = sum(x < y for x, y in zip(a, b)); l = sum(x > y for x, y in zip(a, b)); n = w + l
    p = 1. if n == 0 else min(1., 2 * sum(math.comb(n, i) for i in range(min(w, l) + 1)) / 2 ** n)
    return w, l, len(a) - n, p


print('Per tool, gpt-6.1-terra high, one run per task (per pass = total / passes)')
print('tool | pass/launched | median wall s | p90 wall s | USD/pass | requests/pass | reasoning tokens/pass | output tokens/pass | wall s/pass')
for t in TOOLS:
    xs = [run[(k, t)] for k in TASKS]
    n = sum(x['pass'] for x in xs)
    tot = {m: sum(x[m] for x in xs) for m in M}
    print(f"{t} | {n}/{len(xs)} | {statistics.median(x['wall'] for x in xs):.3f} | {p90([x['wall'] for x in xs]):.3f} | "
          f"${tot['usd'] / n:.4f} | {tot['requests'] / n:.1f} | {tot['reasoning'] / n:,.0f} | {tot['output'] / n:,.0f} | {tot['wall'] / n:.1f}")
print()
print('Paired by task, lower is better: first-tool wins / second-tool wins, ties, exact two-sided sign test p')
for a, b in [('loop+reasoning-replay', 'loop'), ('loop+reasoning-replay', 'codex'), ('loop', 'codex')]:
    print(f'{a} vs {b} ({len(TASKS)} tasks)')
    for m in M:
        w, l, ti, p = sign([run[(k, a)][m] for k in TASKS], [run[(k, b)][m] for k in TASKS])
        print(f'  {m}: {w}/{l}, {ti} ties, p={p:.3f}')
