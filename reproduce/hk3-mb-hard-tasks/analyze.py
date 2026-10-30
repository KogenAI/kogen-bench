#!/usr/bin/env python3
"""Reproduce the numbers on the page from runs.csv (standard library only).

Pass is the protected final-tree grade (evaluation all_passed), never the lanes report class.
"""
import csv, math, pathlib

HERE = pathlib.Path(__file__).parent
ROWS = list(csv.DictReader(open(HERE / 'runs.csv', newline='')))
TASKS = list(dict.fromkeys(r['task'] for r in ROWS))
ALONE = next(r['arm'] for r in ROWS if r['arm'] != 'kogen')
ARMS = ['kogen', ALONE]
run = {(r['task'], r['arm']): r for r in ROWS}
USAGE = 'usd_list' in ROWS[0]


def wilson(k, n, z=1.959964):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0., c - h), min(1., c + h)


def sign2(lo, hi):
    n = lo + hi
    return 1. if n == 0 else min(1., 2 * sum(math.comb(n, i) for i in range(min(lo, hi) + 1)) / 2 ** n)


def sign1(wins, losses):
    """One-sided exact p that Kogen wins at least this often (ties dropped)."""
    n = wins + losses
    return 1. if n == 0 else sum(math.comb(n, i) for i in range(wins, n + 1)) / 2 ** n


def fisher(a, b, c, d):
    """Two-sided Fisher exact on [[a,b],[c,d]] (sum of tables no likelier than the observed one)."""
    r1, r2, c1, n = a + b, c + d, a + c, a + b + c + d
    pr = lambda x: math.comb(r1, x) * math.comb(r2, c1 - x) / math.comb(n, c1)
    p0 = pr(a)
    return min(1., sum(pr(x) for x in range(max(0, c1 - r2), min(r1, c1) + 1) if pr(x) <= p0 * (1 + 1e-9)))


def ok(arm, t):
    return run[(t, arm)]['passed'] == '1'


def passblock(tasks, title):
    n = len(tasks)
    print(title)
    ks = {arm: sum(ok(arm, t) for t in tasks) for arm in ARMS}
    for arm in ARMS:
        lo, hi = wilson(ks[arm], n)
        print(f'{arm}: {ks[arm]}/{n} = {ks[arm] / n:.2f} [{lo:.2f}, {hi:.2f}] (Wilson 95%)')
    both = sum(ok('kogen', t) and ok(ALONE, t) for t in tasks)
    ko = sum(ok('kogen', t) and not ok(ALONE, t) for t in tasks)
    al = sum(ok(ALONE, t) and not ok('kogen', t) for t in tasks)
    print(f'paired: both pass {both}, only Kogen {ko}, only {ALONE} {al}, both fail {n - both - ko - al}')
    print(f'exact paired test (McNemar, two-sided binomial on the {ko + al} discordant tasks): p={sign2(ko, al):.4f}')
    print(f'Fisher exact (2x2 pass/fail by setup, two-sided): p={fisher(ks["kogen"], n - ks["kogen"], ks[ALONE], n - ks[ALONE]):.4f}')


def paired(name, f, tasks):
    ts = [t for t in tasks if f(run[(t, 'kogen')]) is not None and f(run[(t, ALONE)]) is not None]
    a = [f(run[(t, 'kogen')]) for t in ts]; b = [f(run[(t, ALONE)]) for t in ts]
    lo = sum(x < y for x, y in zip(a, b)); hi = sum(x > y for x, y in zip(a, b))
    print(f'{name}: Kogen lower/higher {lo}/{hi}, {len(ts) - lo - hi} ties, {len(ts)} tasks measured for both, '
          f'exact two-sided p={sign2(lo, hi):.4f}; totals Kogen {sum(a):.1f}, {ALONE} {sum(b):.1f}')


def num(key, cast=float):
    return lambda r: cast(r[key]) if r[key] != '' else None


print(f'cells: {len(ROWS)}; tasks: {len(TASKS)}; one run per task and setup')
print()
print(f'task | Kogen outcome | Kogen passed (tests) | {ALONE} outcome | {ALONE} passed (tests)')
for t in TASKS:
    k, a = run[(t, 'kogen')], run[(t, ALONE)]
    fmt = lambda r: f'{"pass" if r["passed"] == "1" else "fail"} ({r["tests_passed"] or "-"}/{r["tests_expected"] or "-"})'
    print(f'{t} | {k["outcome"]} | {fmt(k)} | {a["outcome"]} | {fmt(a)}')
print()
passblock(TASKS, 'Pass by the protected final-tree grade (evaluation all_passed):')
infra = [t for t in TASKS if any(run[(t, a)]['infrastructure'] for a in ARMS)]
if infra:
    print()
    print('Cells with no final tree to grade (infrastructure column):',
          [(t, a, run[(t, a)]['outcome'], run[(t, a)]['infrastructure']) for t in infra for a in ARMS if run[(t, a)]['infrastructure']])
    passblock([t for t in TASKS if t not in infra], f'Sensitivity, those tasks dropped ({len(TASKS) - len(infra)} tasks):')
print()
print('Wall time as measured (s; tasks with a recorded wall for both setups)')
paired('wall s', num('wall_s'), TASKS)
if USAGE:
    print()
    print('Measured usage (Claude Code session records read the same way for both setups; USD at list price, not plan price)')
    ok_t = [t for t in TASKS if all(run[(t, a)]['usd_list'] != '' for a in ARMS)]
    print(f'tasks with usage for both setups: {len(ok_t)} of {len(TASKS)}; left out: {[t for t in TASKS if t not in ok_t]}')
    print('arm | requests | fresh input | cache write | cache read | output | USD list | USD per pass')
    for arm in ARMS:
        rs = [run[(t, arm)] for t in ok_t]
        usd = sum(float(r['usd_list']) for r in rs); n = sum(r['passed'] == '1' for r in rs)
        print(f'{arm} | {sum(int(r["requests"]) for r in rs)} | {sum(int(r["fresh_input"]) for r in rs)} | '
              f'{sum(int(r["cache_write"]) for r in rs)} | {sum(int(r["cache_read"]) for r in rs)} | '
              f'{sum(int(r["output"]) for r in rs)} | {usd:.4f} | {"n/a" if n == 0 else f"{usd / n:.4f}"}')
    paired('USD list', num('usd_list'), TASKS)
    paired('requests', num('requests', int), TASKS)
    paired('output tokens', num('output', int), TASKS)
else:
    print()
    print('Usage and cost: not measured (the harness recorded none for the Kogen lane, and the session-record reader covers Claude Code only).')

mb = HERE / 'runs-mb.csv'
if mb.exists():
    print()
    print('Registered pooled analysis (hk3.md: per-task mean over the host observations at the same pins; one-sided exact sign test that Kogen wins)')
    obs = {}
    for src in (ROWS, list(csv.DictReader(open(mb, newline='')))):
        for r in src:
            obs.setdefault((r['task'], 'kogen' if r['arm'] == 'kogen' else 'alone'), []).append(int(r['passed']))
    wins = losses = ties = 0
    for t in TASKS:
        k, a = obs[(t, 'kogen')], obs[(t, 'alone')]
        mk, ma = sum(k) / len(k), sum(a) / len(a)
        wins += mk > ma; losses += mk < ma; ties += mk == ma
        print(f'{t} | observations {len(k)} | Kogen mean {mk:.2f} | alone mean {ma:.2f} | diff {mk - ma:+.2f}')
    md = sum(sum(obs[(t, 'kogen')]) / len(obs[(t, 'kogen')]) - sum(obs[(t, 'alone')]) / len(obs[(t, 'alone')]) for t in TASKS) / len(TASKS)
    print(f'wins {wins}, losses {losses}, ties {ties}; mean paired difference {md:+.3f}; exact one-sided sign p={sign1(wins, losses):.4f}')
