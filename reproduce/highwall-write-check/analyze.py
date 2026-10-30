#!/usr/bin/env python3
"""Reproduce the highwall-write-check short-test numbers from runs.csv (stdlib only)."""
import csv, math, pathlib, statistics

HERE = pathlib.Path(__file__).resolve().parent
TOOLS = ['loop-default', 'write-check', 'codex']
LABEL = {'loop-default': 'loop-default', 'write-check': 'write-check', 'codex': 'Codex CLI'}

rows = list(csv.DictReader((HERE / 'runs.csv').open()))
counted = [r for r in rows if r['counted'] == '1']
by = {(r['task'], r['tool']): r for r in counted}


def num(v):
    return float(v) if '.' in v else int(v)


def p90(xs):
    xs = sorted(xs)
    return xs[math.ceil(0.9 * len(xs)) - 1]  # nearest rank



def sign_p(a, b):
    n = a + b
    if n == 0:
        return 1.0
    k = min(a, b)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)


print(f'runs counted: {len(counted)}; passed: {sum(r["passed"] == "1" for r in counted)}; '
      f'tasks: {len({r["task"] for r in counted})}; uncounted attempts: {len(rows) - len(counted)}')
print()
print('| Tool | Pass / runs | Median / p90 wall s | Median / p90 API requests | Reasoning tokens (total) | Output tokens (total) | USD total / USD per pass |')
for t in TOOLS:
    rs = [r for r in counted if r['tool'] == t]
    wall = [float(r['wall_s']) for r in rs]
    req = [int(r['requests']) for r in rs]
    passes = sum(r['passed'] == '1' for r in rs)
    usd = sum(float(r['cost_usd']) for r in rs)
    rmed = f'{statistics.median(req):g}'
    print(f'| {LABEL[t]} | {passes} / {len(rs)} | {statistics.median(wall):.3f} / {p90(wall):.3f} | '
          f'{rmed} / {p90(req)} | {sum(int(r["reasoning_tokens"]) for r in rs):,} | '
          f'{sum(int(r["output_tokens"]) for r in rs):,} | ${usd:.6f} / ${usd / passes:.6f} |')
print()
print('Paired by task; wins for write-check / wins for comparison (lower is better); exact two-sided sign test, ties excluded.')
metrics = [('Wall', 'wall_s'), ('Requests', 'requests'), ('Reasoning', 'reasoning_tokens'),
           ('Output', 'output_tokens'), ('USD', 'cost_usd')]
print('| Comparison | ' + ' | '.join(m for m, _ in metrics) + ' | Pass |')
for other in ['loop-default', 'codex']:
    tasks = [t for t in dict.fromkeys(r['task'] for r in counted) if (t, other) in by and (t, 'write-check') in by]
    cells = []
    for _, k in metrics:
        w = sum(num(by[(t, 'write-check')][k]) < num(by[(t, other)][k]) for t in tasks)
        l = sum(num(by[(t, 'write-check')][k]) > num(by[(t, other)][k]) for t in tasks)
        cells.append(f'{w}/{l}, p={sign_p(w, l):.3f}')
    ties = sum(by[(t, 'write-check')]['passed'] == by[(t, other)]['passed'] for t in tasks)
    w = sum(by[(t, 'write-check')]['passed'] > by[(t, other)]['passed'] for t in tasks)
    l = sum(by[(t, 'write-check')]['passed'] < by[(t, other)]['passed'] for t in tasks)
    cells.append(f'{w}/{l}, {ties} ties, p={sign_p(w, l):.3f}')
    print(f'| write-check vs {LABEL[other]} ({len(tasks)} tasks) | ' + ' | '.join(cells) + ' |')
print()
wc = [r for r in counted if r['tool'] == 'write-check']
active = sum(int(r['command_arg_calls']) > 0 for r in wc)
print(f'activation: {active}/{len(wc)} write-check runs used the write_file command argument '
      f'(write_file calls: {sum(int(r["write_file_calls"]) for r in wc)}); rate {active / len(wc):.0%}')
print(f'counted spend: ${sum(float(r["cost_usd"]) for r in rows):.6f} of $4 cap')
