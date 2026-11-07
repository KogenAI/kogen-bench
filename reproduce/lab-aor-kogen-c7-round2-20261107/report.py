#!/usr/bin/env python3
"""report.py: rebuilds the per-task table of this finding from data/cells.tsv (one row per cell, both arms).

gain = (checks passed - start-tree floor) / (checks expected - start-tree floor), per cell; per task the mean over its cells.
Run: python3 report.py   (standard library only)
"""
import csv, os, statistics as st
here = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(here, 'data', 'cells.tsv')), delimiter='\t'))
valid = [r for r in rows if r['valid'] == 'yes']
tasks = sorted({r['task'] for r in valid})
arms = [('kogen', 'Kogen with the shaping fix'), ('alone', 'Claude Code alone'), ('kogen-3607552', 'Kogen before the fix (round 1)')]
print('| task | Kogen cells | Kogen mean gain | Kogen all-pass | alone cells | alone mean gain | alone all-pass | difference of mean gain (Kogen - alone) |')
print('|---|---|---|---|---|---|---|---|')
allk, alla = [], []
for t in tasks:
    k = [float(r['gain']) for r in valid if r['task'] == t and r['arm'] == 'kogen']
    a = [float(r['gain']) for r in valid if r['task'] == t and r['arm'] == 'alone']
    kp = sum(r['all_pass'] == 'yes' for r in valid if r['task'] == t and r['arm'] == 'kogen')
    ap = sum(r['all_pass'] == 'yes' for r in valid if r['task'] == t and r['arm'] == 'alone')
    allk += k; alla += a
    mk = st.mean(k) if k else None; ma = st.mean(a) if a else None
    d = f'{mk - ma:+.2f}' if k and a else 'n/a'
    print(f"| {t} | {len(k)} | {mk:.2f} | {kp} of {len(k)} | {len(a)} | {ma:.2f} | {ap} of {len(a)} | {d} |" if k else f"| {t} | 0 | n/a | n/a | {len(a)} | {ma:.2f} | {ap} of {len(a)} | n/a |")
print()
r1 = [float(r['gain']) for r in valid if r['arm'] == 'kogen-3607552']
for name, xs, arm in (('Kogen with the shaping fix (round 2)', allk, 'kogen'), ('Claude Code alone (round 1)', alla, 'alone'), ('Kogen release before the fix (round 1)', r1, 'kogen-3607552')):
    n = len(xs); ap = sum(r['all_pass'] == 'yes' for r in valid if r['arm'] == arm)
    print(f"{name}: {n} valid cells, mean gain {st.mean(xs):.3f}, all-pass {ap} of {n}" if n else f"{name}: no valid cell")
print()
print('paired per task (Kogen round-2 cell minus the mean of the 3 alone cells, tasks with a Kogen cell):', ', '.join(f"{t.replace('rails-ft-','')} {float([r for r in valid if r['task']==t and r['arm']=='kogen'][0]['gain']) - st.mean([float(r['gain']) for r in valid if r['task']==t and r['arm']=='alone']):+.2f}" for t in tasks if any(r['task']==t and r['arm']=='kogen' for r in valid)))
print('Kogen cells by outcome:', {o: sum(r['outcome'] == o for r in rows if r['arm'] == 'kogen') for o in sorted({r['outcome'] for r in rows if r['arm'] == 'kogen'})})
cost = {arm: sum(float(r['cost_usd'] or 0) for r in rows if r['arm'] == arm) for arm, _ in arms}
wall = {arm: [float(r['wall_s']) for r in rows if r['arm'] == arm] for arm, _ in arms}
for arm, label in arms:
    if wall[arm]: print(f"{label}: list-equivalent USD {cost[arm]:.2f} over {len(wall[arm])} cells; median wall {st.median(wall[arm]):.0f} s")
