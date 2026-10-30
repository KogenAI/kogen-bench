#!/usr/bin/env python3
"""Reproduce the batch-tool short-test numbers from runs.csv (stdlib only)."""
import csv, math, pathlib, statistics

HERE = pathlib.Path(__file__).resolve().parent
TOOLS = ['loop-default', 'batch', 'exec', 'codex']
LABEL = {'loop-default': 'loop default', 'batch': 'batch', 'exec': 'exec', 'codex': 'Codex CLI'}

rows = list(csv.DictReader((HERE / 'runs.csv').open()))
by = {(r['task'], r['tool']): r for r in rows}
tasks = list(dict.fromkeys(r['task'] for r in rows))


def sign_p(a, b):
    n = a + b
    if n == 0:
        return 1.0
    k = min(a, b)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)


def per_req(r, k):
    return float(r[k]) / int(r['requests'])


print(f'runs: {len(rows)}; passed: {sum(r["passed"] == "1" for r in rows)}; tasks: {len(tasks)}')
print()
print('| Tool | Pass | USD total | USD per pass | Requests | Operations per request | Reasoning tokens per request | Median wall s |')
for t in TOOLS:
    rs = [r for r in rows if r['tool'] == t]
    passes = sum(r['passed'] == '1' for r in rs)
    usd = sum(float(r['cost_usd']) for r in rs)
    req = sum(int(r['requests']) for r in rs)
    ops = sum(int(r['operations']) for r in rs)
    rea = sum(int(r['reasoning_tokens']) for r in rs)
    wall = statistics.median(float(r['wall_s']) for r in rs)
    print(f'| {LABEL[t]} | {passes}/{len(rs)} | ${usd:.4f} | ${usd / passes:.4f} | {req} | {ops / req:.2f} | '
          f'{rea / req:.1f} | {wall:.1f} |')
print()
print('Activation (a run used the new tool when one call ran 2 or more operations):')
for t in ['batch', 'exec']:
    rs = [r for r in rows if r['tool'] == t]
    print(f'{t}: {sum(r["activated"] == "1" for r in rs)}/{len(rs)} runs; '
          f'{sum(int(r["new_tool_calls"]) for r in rs)} calls, {sum(int(r["new_tool_calls_2plus"]) for r in rs)} with 2+ operations')
print()
print('Paired by task: runs where the first tool is lower / higher than the second; exact two-sided sign test, ties excluded.')
metrics = [('Operations per request', lambda r: int(r['operations']) / int(r['requests'])),
           ('Requests', lambda r: int(r['requests'])),
           ('Reasoning per request', lambda r: per_req(r, 'reasoning_tokens')),
           ('USD', lambda r: float(r['cost_usd'])),
           ('Wall', lambda r: float(r['wall_s'])),
           ('Pass', lambda r: int(r['passed']))]
print('| Comparison | ' + ' | '.join(m for m, _ in metrics) + ' |')
for a, b in [('batch', 'loop-default'), ('batch', 'codex'), ('exec', 'loop-default')]:
    cells = []
    for _, f in metrics:
        lo = sum(f(by[(t, a)]) < f(by[(t, b)]) for t in tasks)
        hi = sum(f(by[(t, a)]) > f(by[(t, b)]) for t in tasks)
        cells.append(f'{lo}/{hi}, p={sign_p(lo, hi):.3f}')
    print(f'| {LABEL[a]} vs {LABEL[b]} | ' + ' | '.join(cells) + ' |')
