#!/usr/bin/env python3
"""Rebuild the HK2 hard-task selection and host allocation from runs.csv.

Standard library only. Prints the selection tables; compare with expected-output.txt.
"""
import collections, csv, hashlib, pathlib

HERE = pathlib.Path(__file__).resolve().parent
with open(HERE / 'runs.csv', newline='') as f:
    runs = list(csv.DictReader(f))
QUALIFIED = [l.strip() for l in open(HERE / 'qualified.txt') if l.strip() and not l.startswith('#')]


def counts(r):
    # An attempt counts when it was evaluated with a complete grade and executed command receipts,
    # and had no infrastructure or provider error (a capacity error counts even if the grade said none).
    return (r['evaluated'] == 'True' and r['complete'] == 'True' and r['receipts'] == 'True'
            and r['infrastructure'] == 'False' and r['error_class'] == '')


def record(effort):
    tot = collections.defaultdict(lambda: [0, 0])
    per = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0]))
    for r in runs:
        if r['effort'] != effort or not counts(r):
            continue
        p = r['passed'] == 'True'
        tot[r['task']][0] += p; tot[r['task']][1] += 1
        c = per[r['task']][(r['venue'], r['round'])]; c[0] += p; c[1] += 1
    return tot, per


high, high_per = record('high')
medium, _ = record('medium')
selected = sorted(t for t in QUALIFIED if t in high and high[t][0] < high[t][1])
# Medium fallback applies only to tasks with no evaluated high attempts.
fallback = sorted(t for t in QUALIFIED if t not in high and t in medium and medium[t][0] < medium[t][1])
selected += fallback

out = []
P = out.append
P(f"Codex records read: {len(runs)}; counted high attempts: {sum(n for _, n in high.values())}")
P(f"Selected tasks: {len(selected)} (medium-only fallback: {len(fallback)})")
P('')
P('| Selected task | All Codex-high passes / attempts | Full round evidence (st = Studio, mb = MacBook) |')
P('| --- | --- | --- |')
for t in selected:
    ev = '; '.join(f"{h}/{rd}: {p}/{n}" for (h, rd), (p, n) in sorted(high_per[t].items()))
    P(f"| {t} | {high[t][0]}/{high[t][1]} | {ev} |")
P('')
P('| Excluded recovered task | High passes / evaluated non-infrastructure attempts | Reason |')
P('| --- | --- | --- |')
for t in sorted(high):
    if t in selected:
        continue
    p, n = high[t]
    if p < n:
        reason = 'Failed but has no recorded qualification'
    elif t in medium and medium[t][0] < medium[t][1]:
        reason = 'No high coding failure; medium failure cannot substitute because high data exists'
    else:
        reason = 'No evaluated high coding failure'
    P(f"| {t} | {p}/{n} | {reason} |")
P('')
for r in runs:
    if r['error_class'] == 'provider-capacity':
        P(f"Provider-capacity attempt not counted: {r['task']} {r['venue']}/{r['round']} {r['rep']} "
          f"(requests {r['requests']}, wall {r['wall_s']} s, grade passed={r['passed']})")
P('')
order = sorted(selected, key=lambda t: hashlib.sha256(t.encode()).hexdigest())
bridge, rest = order[:3], order[3:]
alloc = {'hk2-st': bridge + rest[0::2], 'hk2-mb': bridge + rest[1::2]}
P('SHA-256 order: ' + ', '.join(order))
P('Bridge tasks (both hosts): ' + ', '.join(bridge))
for k, v in alloc.items():
    P(f"{k}: {', '.join(v)} ({2 * len(v)} main runs)")
P(f"Main runs total: {sum(2 * len(v) for v in alloc.values())}; one-sided sign test p if all {len(selected)} task differences favour one tool: 1/{2 ** len(selected)}")
print('\n'.join(out))
