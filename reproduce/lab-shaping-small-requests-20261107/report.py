#!/usr/bin/env python3
"""report.py <pack dir>: prints the per-round and held-out tables of this finding from data/cells.json.

Each record of data/cells.json is one shape-only cell: round, arm, request id, outcome (ready / refused / deadline),
attempts (refused submissions plus the accepted one), refusals (attempt, gate, problem-line count, kind), wall seconds
and the coding agent's reported list-equivalent cost in USD.
"""
import collections, json, os, sys

d = sys.argv[1] if len(sys.argv) > 1 else '.'
cells = json.load(open(os.path.join(d, 'data', 'cells.json')))
reqs = json.load(open(os.path.join(d, 'data', 'requests.json')))
kinds = {r['id']: r['kind'] for k in ('climb', 'held') for r in reqs[k]}

def summary(rows):
    by = collections.OrderedDict()
    for c in rows:
        a = by.setdefault(c['arm'], collections.Counter())
        a['cells'] += 1
        a['ready'] += c['outcome'] == 'ready'
        a['first'] += c['outcome'] == 'ready' and c['attempts'] == 1
        a['deadline'] += c['outcome'] == 'deadline'
        a['cost'] += c['cost_usd']
        for x in c['refusals']:
            a['gate ' + x['gate']] += 1
    return by

for rnd in sorted({c['round'] for c in cells}, key=lambda r: (r == 'held-out', r)):
    rows = [c for c in cells if c['round'] == rnd]
    print(f'== {rnd}: {len(rows)} cells')
    for arm, a in summary(rows).items():
        gates = ', '.join(f'{k[5:]} {v}' for k, v in sorted(a.items()) if k.startswith('gate '))
        print(f"  {arm:<4} cells {a['cells']:>2}  ready {a['ready']:>2}  first-attempt {a['first']:>2}  deadline {a['deadline']}  "
              f"cost {a['cost']:.2f} USD  refusals: {gates or '-'}")
print('== per request and arm: R = ready at the first attempt, r = ready later, x = refused, d = deadline (in cell order)')
ORDER = ['A', 'S1', 'C1', 'C2', 'C3', 'C5', 'C6']
arms = sorted(dict.fromkeys(c['arm'] for c in cells), key=lambda a: ORDER.index(a) if a in ORDER else 99)
mark = lambda c: 'd' if c['outcome'] == 'deadline' else ('x' if c['outcome'] != 'ready' else ('R' if c['attempts'] == 1 else 'r'))
for rid in [r['id'] for k in ('climb', 'held') for r in reqs[k]]:
    row = [f"{arm}:{''.join(mark(c) for c in cells if c['request'] == rid and c['arm'] == arm) or '-'}" for arm in arms]
    print(f'  {rid:<4} {kinds[rid]:<28}', '  '.join(row))
print('== refusal kinds (problem lines) per arm, all rounds')
k = collections.defaultdict(collections.Counter)
for c in cells:
    for x in c['refusals']:
        for kind, n in x.get('kinds', {}).items():
            k[c['arm']][kind] += n
for arm, cnt in k.items():
    print(f'  {arm:<4}', dict(sorted(cnt.items())))
aor_path = os.path.join(d, 'data', 'aor-cells.json')
if os.path.exists(aor_path):
    print('== Rails refused-set tasks (candidate changes on release 3607552)')
    aor = json.load(open(aor_path))
    for c in aor:
        refs = '; '.join(f"{x['attempt']}: {x['gate']} {x['problem_lines']}" for x in c['refusals']) or '-'
        print(f"  {c['run']:<13} {c['task']}  {c['outcome'][:60]:<60} {refs}  wall {c['wall_s']} s  cost {c['cost_usd']:.2f}")
    valid = [c for c in aor if c['run'] == 'rerun']
    print('  ready:', sum(c['outcome'] == 'ready' for c in valid), 'of', len(valid), 'valid cells; Rails cost', round(sum(c['cost_usd'] for c in aor), 2), 'USD')
print('== total cost', round(sum(c['cost_usd'] for c in cells), 2), 'USD list-equivalent over', len(cells), 'small-request cells')
