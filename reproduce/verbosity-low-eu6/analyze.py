#!/usr/bin/env python3
"""Reproduce the verbosity-low-eu6 numbers from runs.csv (standard library only)."""
import csv, math, pathlib, statistics

ROWS = list(csv.DictReader(open(pathlib.Path(__file__).with_name('runs.csv'), newline='')))
ARMS = ['api-replay', 'verbosity-low', 'codex']
LABEL = {'api-replay': 'api-replay', 'verbosity-low': 'api-replay + verbosity low', 'codex': 'Codex CLI'}
COUNTED = [r for r in ROWS if r['stratum'] == 'counted']
BLOCKS = list(dict.fromkeys((r['task'], int(r['rep'])) for r in COUNTED))
TASKS = list(dict.fromkeys(b[0] for b in BLOCKS))
run = {}
for r in COUNTED:
    run[(r['task'], int(r['rep']), r['arm'])] = {
        'pass': r['passed'] == '1', 'wall': float(r['wall_s']), 'requests': float(r['requests']), 'usd': float(r['cost_usd']),
        'nonreasoning': int(r['output_tokens']) - int(r['reasoning_tokens']), 'final_text_bytes': float(r['final_text_bytes'])}
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


def per_pass(arm, tasks=TASKS):
    xs = [run[(t, r, arm)] for (t, r) in BLOCKS if t in tasks]
    n = sum(x['pass'] for x in xs)
    return xs, n, sum(x['usd'] for x in xs) / n if n else None


print('Per arm, gpt-6.1-terra high, 3 fresh tasks x 6 reps, dry run excluded (per pass = total / passes)')
print('arm | pass/launched | non-reasoning output total | per run | final answer bytes/run | median wall s | p90 wall s | requests/run | USD total | USD/pass')
for a in ARMS:
    xs, n, u = per_pass(a)
    nr = sum(x['nonreasoning'] for x in xs)
    print(f"{LABEL[a]} | {n}/{len(xs)} | {nr:,} | {nr / len(xs):,.0f} | {sum(x['final_text_bytes'] for x in xs) / len(xs):,.0f} | "
          f"{statistics.median(x['wall'] for x in xs):.3f} | {p90([x['wall'] for x in xs]):.3f} | {sum(x['requests'] for x in xs) / len(xs):.1f} | "
          f"${sum(x['usd'] for x in xs):.6f} | ${u:.6f}")
print()
print('Paired by block (task, rep), lower is better: first-arm wins / second-arm wins, ties, exact two-sided sign test p')
METRICS = [('nonreasoning', 'nonreasoning'), ('usd_per_pass', None), ('wall', 'wall'), ('requests', 'requests'), ('final_text_bytes', 'final_text_bytes')]
for a, b in [('verbosity-low', 'api-replay'), ('verbosity-low', 'codex'), ('api-replay', 'codex')]:
    print(f'{LABEL[a]} vs {LABEL[b]} ({len(BLOCKS)} blocks)')
    for name, key in METRICS:
        f = cpp if key is None else (lambda x, k=key: x[k])
        w, l, ti, p = sign([f(run[(t, r, a)]) for t, r in BLOCKS], [f(run[(t, r, b)]) for t, r in BLOCKS])
        print(f'  {name}: {w}/{l}, {ti} ties, p={p:.4f}')
    da = [run[(t, r, a)]['pass'] for t, r in BLOCKS]
    db = [run[(t, r, b)]['pass'] for t, r in BLOCKS]
    w, l, ti, p = test(sum(x and not y for x, y in zip(da, db)), sum(y and not x for x, y in zip(da, db)), len(BLOCKS))
    print(f'  pass (discordant, first-only/second-only): {w}/{l}, {ti} ties, p={p:.4f}')
    for name, key in (('nonreasoning', 'nonreasoning'), ('usd', 'usd'), ('wall', 'wall')):
        lr = [math.log(run[(t, r, a)][key] / run[(t, r, b)][key]) for t, r in BLOCKS]
        print(f'  {name} geomean ratio: {math.exp(sum(lr) / len(lr)):.3f}')
    print(f'  USD per pass ratio: {per_pass(a)[2] / per_pass(b)[2]:.3f}')
print()
print('By task, api-replay + verbosity low vs api-replay')
for t in TASKS:
    bs = [(x, r) for x, r in BLOCKS if x == t]
    w, l, ti, p = sign([run[(x, r, 'verbosity-low')]['nonreasoning'] for x, r in bs], [run[(x, r, 'api-replay')]['nonreasoning'] for x, r in bs])
    ra = [math.log(run[(x, r, 'verbosity-low')]['nonreasoning'] / run[(x, r, 'api-replay')]['nonreasoning']) for x, r in bs]
    ru = [math.log(run[(x, r, 'verbosity-low')]['usd'] / run[(x, r, 'api-replay')]['usd']) for x, r in bs]
    passes = ' '.join(f"{LABEL[a]} {sum(run[(x, r, a)]['pass'] for x, r in bs)}/{len(bs)}" for a in ARMS)
    print(f"{t}: non-reasoning {w}/{l}, {ti} ties, p={p:.4f}, ratio {math.exp(sum(ra) / len(ra)):.3f}; USD ratio {math.exp(sum(ru) / len(ru)):.3f}; passes: {passes}")
