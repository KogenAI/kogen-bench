#!/usr/bin/env python3
"""Reproduce the shell-yield-eu2 numbers from runs.csv (standard library only)."""
import csv, math, pathlib, statistics

ROWS = list(csv.DictReader(open(pathlib.Path(__file__).with_name('runs.csv'), newline='')))
ARMS = ['loop-default', 'shell-yield', 'codex']
LABEL = {'loop-default': 'loop default', 'shell-yield': 'loop shell-yield', 'codex': 'Codex CLI'}
COUNTED = [r for r in ROWS if r['stratum'] == 'counted']
run = {}
for r in COUNTED:
    run[(r['task'], int(r['rep']), r['arm'])] = {
        'pass': r['passed'] == '1', 'timeout': r['outcome'] == 'timeout', 'budget': r['request_budget_stop'] == '1',
        'wall': float(r['wall_s']), 'shell': float(r['shell_s']), 'requests': int(r['requests']), 'usd': float(r['cost_usd']),
        'yields': int(r['yields']), 'waits': int(r['session_calls']), 'stops': int(r['stops'])}
TASKS = list(dict.fromkeys(r['task'] for r in COUNTED))
# complete blocks: all three arms ran (the last block, kogen-shell-bound r2, has only the Codex cell)
BLOCKS = [(t, r) for r in (1, 2) for t in TASKS if all((t, r, a) in run for a in ARMS)]
INF = math.inf


def p90(v):
    v = sorted(v)
    return v[max(0, math.ceil(.9 * len(v)) - 1)]


def test(w, l, n_all):
    n = w + l
    p = 1. if n == 0 else min(1., 2 * sum(math.comb(n, i) for i in range(min(w, l) + 1)) / 2 ** n)
    return w, l, n_all - n, p


def sign(a, b):
    return test(sum(x < y for x, y in zip(a, b)), sum(x > y for x, y in zip(a, b)), len(a))


def cpp(x):  # cost per pass of one cell: a failed cell is worse than any passed one, two failures tie
    return x['usd'] if x['pass'] else INF


print('Per arm, gpt-6.1-terra high, counted cells only (dry cell excluded; Codex includes its unpaired kogen-shell-bound r2 cell)')
print('arm | pass/launched (deadline timeouts, request-limit stops) | shell s total / median | wall s mean / median / p90 | requests | USD total / per pass | yields / waits / stops')
for a in ARMS:
    xs = [v for (t, r, aa), v in run.items() if aa == a]
    n = sum(x['pass'] for x in xs)
    u = sum(x['usd'] for x in xs)
    print(f"{LABEL[a]} | {n}/{len(xs)} ({sum(x['timeout'] for x in xs)}, {sum(x['budget'] for x in xs)}) | "
          f"{sum(x['shell'] for x in xs):,.1f} / {statistics.median(x['shell'] for x in xs):,.1f} | "
          f"{statistics.mean(x['wall'] for x in xs):,.1f} / {statistics.median(x['wall'] for x in xs):,.1f} / {p90([x['wall'] for x in xs]):,.1f} | "
          f"{sum(x['requests'] for x in xs)} | ${u:.4f} / ${u / n:.4f} | {sum(x['yields'] for x in xs)} / {sum(x['waits'] for x in xs)} / {sum(x['stops'] for x in xs)}")
print()
print(f'Paired by task and rep, {len(BLOCKS)} complete blocks (lower is better): first-arm wins / second-arm wins, ties, exact two-sided sign test p')
METRICS = [('shell_s', 'shell'), ('wall', 'wall'), ('usd_per_pass', None), ('usd', 'usd'), ('requests', 'requests')]
for a, b in [('shell-yield', 'loop-default'), ('shell-yield', 'codex'), ('loop-default', 'codex')]:
    print(f'{LABEL[a]} vs {LABEL[b]}')
    for name, key in METRICS:
        f = cpp if key is None else (lambda x, k=key: x[k])
        w, l, ti, p = sign([f(run[(t, r, a)]) for t, r in BLOCKS], [f(run[(t, r, b)]) for t, r in BLOCKS])
        print(f'  {name}: {w}/{l}, {ti} ties, p={p:.4f}')
    da = [run[(t, r, a)]['pass'] for t, r in BLOCKS]
    db = [run[(t, r, b)]['pass'] for t, r in BLOCKS]
    w, l, ti, p = test(sum(x and not y for x, y in zip(da, db)), sum(y and not x for x, y in zip(da, db)), len(BLOCKS))
    print(f'  pass (discordant, first-only/second-only): {w}/{l}, {ti} ties, p={p:.4f}')
    for name, key in (('shell', 'shell'), ('wall', 'wall'), ('requests', 'requests')):
        print(f'  {name} total ratio: {sum(run[(t, r, a)][key] for t, r in BLOCKS) / sum(run[(t, r, b)][key] for t, r in BLOCKS):.3f}')
    ua = sum(run[(t, r, a)]['usd'] for t, r in BLOCKS) / max(1, sum(run[(t, r, a)]['pass'] for t, r in BLOCKS))
    ub = sum(run[(t, r, b)]['usd'] for t, r in BLOCKS) / max(1, sum(run[(t, r, b)]['pass'] for t, r in BLOCKS))
    print(f'  USD per pass: ${ua:.4f} vs ${ub:.4f}')
print()
print('By task (counted cells): agent wall s / shell s / longest shell s, pass; one line per cell')
for t in TASKS:
    for r in (1, 2):
        cells = []
        for a in ARMS:
            x = run.get((t, r, a))
            cells.append(f"{LABEL[a]} not run" if x is None else
                         f"{LABEL[a]} {x['wall']:,.1f}/{x['shell']:,.1f} {'pass' if x['pass'] else 'fail'}{' timeout' if x['timeout'] else ''}{' request-limit' if x['budget'] else ''}")
        print(f'{t} r{r}: ' + '; '.join(cells))
