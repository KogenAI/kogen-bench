#!/usr/bin/env python3
"""Reproduce the numbers on the page from runs.csv and runs-hk3-lm.csv (standard library only).

Pass is the protected final-tree grade (evaluation all_passed) together with a normal ending
(landed, ok or finished), never the lanes report class. Cells marked uncounted=1 were graded by a
defective instrument and are shown separately and never scored.
"""
import csv, math, pathlib

HERE = pathlib.Path(__file__).parent
ROWS = list(csv.DictReader(open(HERE / 'runs.csv', newline='')))
OLD = list(csv.DictReader(open(HERE / 'runs-hk3-lm.csv', newline='')))
ALONE = 'codex-alone'
ARMS = ['kogen', ALONE]
COUNTED = [r for r in ROWS if r['uncounted'] == '0']
UNCOUNTED = [r for r in ROWS if r['uncounted'] == '1']
TASKS = list(dict.fromkeys(r['task'] for r in COUNTED))
run = {(r['task'], r['arm']): r for r in COUNTED}
old = {(r['task'], r['arm']): r for r in OLD}


def wilson(k, n, z=1.959964):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0., c - h), min(1., c + h)


def sign2(lo, hi):
    n = lo + hi
    return 1. if n == 0 else min(1., 2 * sum(math.comb(n, i) for i in range(min(lo, hi) + 1)) / 2 ** n)


def fisher(a, b, c, d):
    """Two-sided Fisher exact on [[a,b],[c,d]] (sum of tables no likelier than the observed one)."""
    r1, r2, c1, n = a + b, c + d, a + c, a + b + c + d
    pr = lambda x: math.comb(r1, x) * math.comb(r2, c1 - x) / math.comb(n, c1)
    p0 = pr(a)
    return min(1., sum(pr(x) for x in range(max(0, c1 - r2), min(r1, c1) + 1) if pr(x) <= p0 * (1 + 1e-9)))


def ok(arm, t):
    return run[(t, arm)]['passed'] == '1'


def fmt(r):
    return f'{"pass" if r["passed"] == "1" else "fail"} ({r["tests_passed"] or "-"}/{r["tests_expected"] or "-"})'


def paired(name, f, tasks):
    ts = [t for t in tasks if f(run[(t, 'kogen')]) is not None and f(run[(t, ALONE)]) is not None]
    a = [f(run[(t, 'kogen')]) for t in ts]; b = [f(run[(t, ALONE)]) for t in ts]
    lo = sum(x < y for x, y in zip(a, b)); hi = sum(x > y for x, y in zip(a, b))
    print(f'{name}: Kogen lower/higher {lo}/{hi}, {len(ts) - lo - hi} ties, {len(ts)} tasks measured for both, '
          f'exact two-sided p={sign2(lo, hi):.4f}; totals Kogen {sum(a):,.1f}, {ALONE} {sum(b):,.1f}')


def num(key, cast=float):
    return lambda r: cast(r[key]) if r[key] != '' else None


print(f'cells: {len(ROWS)} run, {len(COUNTED)} counted on {len(TASKS)} tasks, {len(UNCOUNTED)} uncounted; one run per task and setup')
print()
print(f'Counted cells\ntask | Kogen outcome | Kogen passed (tests) | {ALONE} outcome | {ALONE} passed (tests)')
for t in TASKS:
    k, a = run[(t, 'kogen')], run[(t, ALONE)]
    print(f'{t} | {k["outcome"]} | {fmt(k)} | {a["outcome"]} | {fmt(a)}')
print()
print('Uncounted cells (grading never ran the acceptance suite, or the Linux-only revive fixture; not scored, shown for completeness)')
print('task | arm | outcome | grader passed/expected | Kogen build requests')
for r in UNCOUNTED:
    print(f'{r["task"]} | {r["arm"]} | {r["outcome"]} | {r["tests_passed"]}/{r["tests_expected"]} | {r["kogen_build_requests"] or "-"}')
print()

n = len(TASKS)
ks = {arm: sum(ok(arm, t) for t in TASKS) for arm in ARMS}
print('Pass by the protected final-tree grade and a normal ending (counted tasks):')
for arm in ARMS:
    lo, hi = wilson(ks[arm], n)
    print(f'{arm}: {ks[arm]}/{n} = {ks[arm] / n:.2f} [{lo:.2f}, {hi:.2f}] (Wilson 95%)')
both = sum(ok('kogen', t) and ok(ALONE, t) for t in TASKS)
ko = sum(ok('kogen', t) and not ok(ALONE, t) for t in TASKS)
al = sum(ok(ALONE, t) and not ok('kogen', t) for t in TASKS)
print(f'paired: both pass {both}, only Kogen {ko}, only {ALONE} {al}, both fail {n - both - ko - al}')
print(f'exact paired test (McNemar, two-sided binomial on the {ko + al} discordant tasks): p={sign2(ko, al):.4f}')
print(f'Fisher exact (2x2 pass/fail by setup, two-sided): p={fisher(ks["kogen"], n - ks["kogen"], ks[ALONE], n - ks[ALONE]):.4f}')
print()
print('Wall time as measured (s; all counted tasks have a recorded wall for both setups)')
paired('wall s', num('wall_s'), TASKS)
print()
print('Measured usage (tokens as recorded by each setup; input includes cache reads; reasoning tokens not added; no cost computed for this block)')
print('arm | input | cached input | output')
for arm in ARMS:
    rs = [run[(t, arm)] for t in TASKS]
    print(f'{arm} | {sum(int(r["input_tokens"]) for r in rs):,} | {sum(int(r["cached_input_tokens"]) for r in rs):,} | {sum(int(r["output_tokens"]) for r in rs):,}')
paired('input tokens', num('input_tokens', int), TASKS)
paired('output tokens', num('output_tokens', int), TASKS)
print('Requests are not compared: the alone setup records completed CLI turns (1 per cell), Kogen records model requests.')
print()
print('Kogen cells that ended before any build request (all 9 tasks): ' +
      str([(r['task'], r['outcome']) for r in ROWS if r['arm'] == 'kogen' and r['kogen_build_requests'] in ('0', 'none')]))
print('of those, counted: ' +
      str([(r['task'], r['outcome']) for r in COUNTED if r['arm'] == 'kogen' and r['kogen_build_requests'] in ('0', 'none')]))
print()
print('Descriptive comparison with hk3-lm (Kogen 18895e65, same tasks, same laptop; a different Kogen pin, one run each, no test applied)')
print('task | hk3-lm Kogen | hk4-lm Kogen | hk3-lm alone | hk4-lm alone | Kogen wall hk3-lm | Kogen wall hk4-lm')
for t in TASKS:
    o, k = old[(t, 'kogen')], run[(t, 'kogen')]
    oa, a = old[(t, ALONE)], run[(t, ALONE)]
    print(f'{t} | {o["outcome"]} {fmt(o)} | {k["outcome"]} {fmt(k)} | {oa["outcome"]} {fmt(oa)} | {a["outcome"]} {fmt(a)} | {float(o["wall_s"]):,.0f} | {float(k["wall_s"]):,.0f}')
for arm in ARMS:
    po = sum(old[(t, arm)]['passed'] == '1' for t in TASKS)
    print(f'{arm}: hk3-lm {po}/{n}, hk4-lm {ks[arm]}/{n}; same tasks pass: {all((old[(t, arm)]["passed"] == "1") == ok(arm, t) for t in TASKS)}')
ow = sum(float(old[(t, 'kogen')]['wall_s']) for t in TASKS); nw = sum(float(run[(t, 'kogen')]['wall_s']) for t in TASKS)
ow_a = sum(float(old[(t, ALONE)]['wall_s']) for t in TASKS if old[(t, ALONE)]['wall_s'] != ''); nw_a = sum(float(run[(t, ALONE)]['wall_s']) for t in TASKS if old[(t, ALONE)]['wall_s'] != '')
lo = sum(float(run[(t, 'kogen')]['wall_s']) < float(old[(t, 'kogen')]['wall_s']) for t in TASKS)
print(f'Kogen wall over the {n} tasks: hk3-lm {ow:,.0f} s, hk4-lm {nw:,.0f} s; shorter in hk4-lm on {lo} of {n} tasks')
print(f'{ALONE} wall over the 4 tasks with a wall in both cohorts (goose-labels-go left out: memory_cap in hk3-lm): hk3-lm {ow_a:,.0f} s, hk4-lm {nw_a:,.0f} s')
