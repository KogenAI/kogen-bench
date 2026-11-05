#!/usr/bin/env python3
"""analyze_c6.py <probes.jsonl> <setup.tsv> : tables for Lab C6. stdlib only.
Labels: R.. red-window trees, G.. green producer mains, *-M01 mutation tree. Levels: quiet, load. Arms: current, allow."""
import collections, csv, json, statistics, sys
P = [json.loads(l) for l in open(sys.argv[1])]
S = {r['label']: r for r in csv.DictReader(open(sys.argv[2]), delimiter='\t')}
mut = lambda l: l.endswith('-M01')
cell = collections.defaultdict(lambda: [0, 0])      # (arm, level, kind) -> [fails, n]
per_tree = collections.defaultdict(lambda: [0, 0])  # (label, arm, level)
for p in P:
    k = 'mutation' if mut(p['label']) else ('R' if p['label'].startswith('R') else 'G')
    c = cell[(p['arm'], p['level'], k)]; c[1] += 1; c[0] += p['rc'] != 0
    t = per_tree[(p['label'], p['arm'], p['level'])]; t[1] += 1; t[0] += p['rc'] != 0
# deterministic breaks: a tree where BOTH arms fail every probe at both levels is not a flake
labels = sorted({p['label'] for p in P if not mut(p['label'])})
det = [l for l in labels if all(per_tree[(l, a, v)][1] and per_tree[(l, a, v)][0] == per_tree[(l, a, v)][1] for a in ('current', 'allow') for v in ('quiet', 'load') if per_tree[(l, a, v)][1])
       and any(per_tree[(l, a, v)][1] for a in ('current', 'allow') for v in ('quiet', 'load'))]
out = {}
print('| arm | level | trees R: fails/n | trees G: fails/n | all unmutated (excl. deterministic) | mutation: caught/n |')
print('|---|---|---|---|---|---|')
for a in ('current', 'allow'):
    for v in ('quiet', 'load'):
        r, g, m = cell[(a, v, 'R')], cell[(a, v, 'G')], cell[(a, v, 'mutation')]
        ex = [p for p in P if p['arm'] == a and p['level'] == v and not mut(p['label']) and p['label'] not in det]
        f = sum(p['rc'] != 0 for p in ex)
        print(f'| {a} | {v} | {r[0]}/{r[1]} | {g[0]}/{g[1]} | {f}/{len(ex)} | {m[0]}/{m[1]} |')
        out[f'{a}-{v}'] = dict(false_reds=f, n=len(ex), red_window_fails=r[0], red_window_n=r[1], green_fails=g[0], green_n=g[1], mutation_caught=m[0], mutation_n=m[1])
print('\ndeterministic breaks (both arms red on every probe), excluded above:', det or 'none')
for v in ('quiet', 'load'):
    l1 = [p['load_before'] for p in P if p['level'] == v]
    if l1: print(f'load1 before probe, {v}: median {statistics.median(l1):.2f}, max {max(l1):.2f}, n {len(l1)}')
    w = [p['wall'] for p in P if p['level'] == v and p['rc'] == 0]
    if w: print(f'wall of passing probes, {v}: median {statistics.median(w):.1f} s, max {max(w):.1f} s')
print('\nsetup status:', dict(collections.Counter(r['status'] for r in S.values())))
print('\nred probes by tree/arm/level (non-mutation):')
for (l, a, v), (f, n) in sorted(per_tree.items()):
    if f and not mut(l): print(f'  {l} {a} {v}: {f}/{n}', next((p['detail'][:140] for p in P if p['label'] == l and p['arm'] == a and p['level'] == v and p['rc']), ''))
json.dump(out, open('/dev/stdout' if False else sys.argv[1] + '.summary.json', 'w'), indent=1)
