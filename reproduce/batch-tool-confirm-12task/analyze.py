#!/usr/bin/env python3
"""Reproduce the batch-tool-confirm-12task numbers from runs.csv (standard library only)."""
import csv, math, pathlib, statistics

ROWS = list(csv.DictReader(open(pathlib.Path(__file__).with_name('runs.csv'), newline='')))
TOOLS = ['loop-default', 'sentence', 'batch', 'codex']
LABEL = {'loop-default': 'loop default', 'sentence': 'sentence only', 'batch': 'batch tool', 'codex': 'Codex CLI'}
TASKS = list(dict.fromkeys(r['task'] for r in ROWS))
run = {(r['task'], r['tool']): r for r in ROWS}


def sign(a, b):
    """First lower / first higher, ties, exact two-sided sign test p."""
    lo = sum(x < y for x, y in zip(a, b)); hi = sum(x > y for x, y in zip(a, b)); n = lo + hi
    p = 1. if n == 0 else min(1., 2 * sum(math.comb(n, i) for i in range(min(lo, hi) + 1)) / 2 ** n)
    return lo, hi, len(a) - n, p


def usd_score(r):  # a failed run is worse than any passed run; two failures tie
    return float(r['cost_usd']) if r['passed'] == '1' else math.inf


METRIC = {
    'cost per pass': usd_score,
    'requests': lambda r: int(r['requests']),
    'operations per request': lambda r: int(r['operations']) / int(r['requests']),
    'wall s': lambda r: float(r['wall_s']),
    'pass': lambda r: int(r['passed']),
}

print(f'runs: {len(ROWS)}; passed: {sum(r["passed"] == "1" for r in ROWS)}; tasks: {len(TASKS)}')
print()
print('tool | pass | USD total | USD per pass | requests | mean requests | operations per request | reasoning tokens per request | median wall s | max upstream gap s')
for t in TOOLS:
    rs = [run[(k, t)] for k in TASKS]
    n = sum(r['passed'] == '1' for r in rs)
    usd = sum(float(r['cost_usd']) for r in rs)
    req = sum(int(r['requests']) for r in rs)
    ops = sum(int(r['operations']) for r in rs)
    rea = sum(int(r['reasoning_tokens']) for r in rs)
    print(f"{LABEL[t]} | {n}/{len(rs)} | ${usd:.4f} | ${usd / n:.4f} | {req} | {req / len(rs):.2f} | {ops / req:.2f} | "
          f"{rea / req:.1f} | {statistics.median(float(r['wall_s']) for r in rs):.1f} | {max(float(r['max_upstream_gap_s']) for r in rs):.1f}")
print()
b = [run[(k, 'batch')] for k in TASKS]
print(f"batch tool used (a call ran 2 or more operations): {sum(r['activated'] == '1' for r in b)}/{len(b)} runs; "
      f"{sum(int(r['new_tool_calls']) for r in b)} calls, {sum(int(r['new_tool_calls_2plus']) for r in b)} with 2+ operations")
print()
print('Paired by task: first lower / first higher, ties, exact two-sided sign test (ties dropped)')
for a, c in [('batch', 'sentence'), ('sentence', 'loop-default'), ('batch', 'loop-default'),
             ('loop-default', 'codex'), ('sentence', 'codex'), ('batch', 'codex')]:
    print(f'{LABEL[a]} vs {LABEL[c]} ({len(TASKS)} tasks)')
    for m, f in METRIC.items():
        lo, hi, ti, p = sign([f(run[(k, a)]) for k in TASKS], [f(run[(k, c)]) for k in TASKS])
        print(f'  {m}: {lo}/{hi}, {ti} ties, p={p:.4f}')
