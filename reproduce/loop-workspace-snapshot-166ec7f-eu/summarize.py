#!/usr/bin/env python3
"""wmap registered readouts from runs.csv (analyze_wmap.py cells.csv). Usage: summarize.py runs.csv
Leaves out the censored pair (kogen-review-on-demand r1: base run ended on a provider HTTP 429, no replacement as registered).
Fired tasks = the 11 small kits where the snapshot is sent (request-1 input larger on wmap)."""
import csv, sys
rows = list(csv.DictReader(open(sys.argv[1]))); by = {(r['task'], r['rep'], r['arm']): r for r in rows}
CENS = {('kogen-review-on-demand', 'r1')}
pairs = sorted((t, rep) for (t, rep, a) in by if a == 'base' and (t, rep) not in CENS and (t, rep, 'wmap') in by)
fired = {t for t, rep in pairs if int(by[(t, rep, 'wmap')]['req1_input']) - int(by[(t, rep, 'base')]['req1_input']) > 500}
def tot(k, sel): return [sum(float(by[(t, rep, a)][k] or 0) for t, rep in pairs if sel(t)) for a in ('base', 'wmap')]
print('pair | orientation before first edit | requests | hidden pass base/wmap | wall s')
for t, rep in pairs:
    b, w = by[(t, rep, 'base')], by[(t, rep, 'wmap')]
    print(f"{t} {rep} | {b['orient_pre']} -> {w['orient_pre']} | {b['requests']} -> {w['requests']} | {b['passed']}/{w['passed']} | {float(b['wall']):.0f} -> {float(w['wall']):.0f}")
for name, sel in (('all', lambda t: True), ('fired (snapshot sent)', lambda t: t in fired), ('no snapshot (large repos)', lambda t: t not in fired)):
    print(f"\n{name}: pairs {sum(1 for t, r in pairs if sel(t))}")
    for k in ('orient_pre', 'requests', 'input', 'output', 'usd', 'wall'):
        b, w = tot(k, sel); print(f"  {k}: {b:.4g} -> {w:.4g} ({(w / b - 1) * 100 if b else 0:+.1f}%)")
disc = [(t, rep) for t, rep in pairs if by[(t, rep, 'base')]['passed'] != by[(t, rep, 'wmap')]['passed']]
print('\ndiscordant hidden-pass pairs:', disc or 'none')
