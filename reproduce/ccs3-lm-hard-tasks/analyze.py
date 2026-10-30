#!/usr/bin/env python3
"""Reproduce the ccs3-lm-hard-tasks numbers from runs.csv (standard library only)."""
import csv, math, pathlib

ROWS = list(csv.DictReader(open(pathlib.Path(__file__).with_name('runs.csv'), newline='')))
ARMS = ['kogen', 'claude-code-alone']
LABEL = {'kogen': 'Kogen driving Claude Code', 'claude-code-alone': 'Claude Code alone'}
TASKS = list(dict.fromkeys(r['task'] for r in ROWS))
run = {(r['task'], r['arm']): r for r in ROWS}


def wilson(k, n, z=1.959964):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0., c - h), min(1., c + h)


def sign(a, b):
    """First lower / first higher, ties, exact two-sided sign test p."""
    lo = sum(x < y for x, y in zip(a, b)); hi = sum(x > y for x, y in zip(a, b)); n = lo + hi
    p = 1. if n == 0 else min(1., 2 * sum(math.comb(n, i) for i in range(min(lo, hi) + 1)) / 2 ** n)
    return lo, hi, len(a) - n, p


def col(arm, f):
    return [f(run[(t, arm)]) for t in TASKS]


print(f'cells: {len(ROWS)}; tasks: {len(TASKS)}; one run per task and arm')
print()
print('task | Kogen passed (tests) | alone passed (tests)')
for t in TASKS:
    k, a = run[(t, 'kogen')], run[(t, 'claude-code-alone')]
    print(f'{t} | {"pass" if k["passed"] == "1" else "fail"} ({k["tests_passed"]}/{k["tests_expected"]}) | '
          f'{"pass" if a["passed"] == "1" else "fail"} ({a["tests_passed"]}/{a["tests_expected"]})')
print()
print('Pass by the protected final-tree grade (evaluation all_passed):')
for arm in ARMS:
    k = sum(col(arm, lambda r: r['passed'] == '1'))
    lo, hi = wilson(k, len(TASKS))
    print(f'{LABEL[arm]}: {k}/{len(TASKS)} = {k / len(TASKS):.2f} [{lo:.2f}, {hi:.2f}] (Wilson 95%)')
print()
print('Pass as the lanes report table printed it (class "correct" only):')
for arm in ARMS:
    k = sum(col(arm, lambda r: r['reported_class'] == 'correct'))
    lo, hi = wilson(k, len(TASKS))
    print(f'{LABEL[arm]}: {k}/{len(TASKS)} = {k / len(TASKS):.2f} [{lo:.2f}, {hi:.2f}]; '
          f'outcomes: {sorted(set(col(arm, lambda r: r["outcome"])))}')
print()
both = sum(r['passed'] == '1' and run[(r['task'], 'claude-code-alone')]['passed'] == '1' for r in ROWS if r['arm'] == 'kogen')
print(f'Paired by task: both pass {both}, both fail {len(TASKS) - both - sum(a != b for a, b in zip(col("kogen", lambda r: r["passed"]), col("claude-code-alone", lambda r: r["passed"])))}, '
      f'only Kogen {sum(a > b for a, b in zip(col("kogen", lambda r: r["passed"]), col("claude-code-alone", lambda r: r["passed"])))}, '
      f'only alone {sum(a < b for a, b in zip(col("kogen", lambda r: r["passed"]), col("claude-code-alone", lambda r: r["passed"])))}')
lo, hi, tie, p = sign(col('kogen', lambda r: int(r['passed'])), col('claude-code-alone', lambda r: int(r['passed'])))
print(f'pass sign test (Kogen lower / higher, ties, exact two-sided p; ties dropped): {lo}/{hi}, {tie} ties, p={p:.4f}')
print()
print('Measured usage (Claude Code session records; USD at list price, not plan price)')
print('arm | requests | fresh input | cache write | cache read | output | USD list | USD per pass | wall s')
for arm in ARMS:
    rs = [run[(t, arm)] for t in TASKS]
    n = sum(r['passed'] == '1' for r in rs)
    usd = sum(float(r['usd_list']) for r in rs)
    print(f'{arm} | {sum(int(r["requests"]) for r in rs)} | {sum(int(r["fresh_input"]) for r in rs)} | '
          f'{sum(int(r["cache_write"]) for r in rs)} | {sum(int(r["cache_read"]) for r in rs)} | '
          f'{sum(int(r["output"]) for r in rs)} | {usd:.4f} | {usd / n:.4f} | {sum(float(r["wall_s"]) for r in rs):.1f}')
print('lanes-recorded requests (Kogen lane: none recorded):',
      {arm: sum(int(r['lanes_requests']) for r in ROWS if r['arm'] == arm) for arm in ARMS})
print()
print('Paired by task, Kogen against alone: Kogen lower / higher, ties, exact two-sided p')
for name, f in [('USD list', lambda r: float(r['usd_list'])), ('requests', lambda r: int(r['requests'])),
                ('wall s', lambda r: float(r['wall_s'])), ('output tokens', lambda r: int(r['output']))]:
    lo, hi, tie, p = sign(col('kogen', f), col('claude-code-alone', f))
    print(f'{name}: {lo}/{hi}, {tie} ties, p={p:.4f}')
