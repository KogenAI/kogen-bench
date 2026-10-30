#!/usr/bin/env python3
"""Reproduce the route-same-host-throughput numbers from runs.csv.

Per host and client: median [IQR] of output tokens/s after first output and of time to first output (TTFO),
then paired ratios against the loop binary (Lc) and against loop raw HTTP (Lr), per block, with an exact
two-sided sign test (ties dropped). A request counts only if it has a rate, >= 300 output tokens and a
successful outcome. Usage: analyze.py [runs.csv]
"""
import csv, math, os, statistics as S, sys

path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'runs.csv')
R = list(csv.DictReader(open(path)))
fl = lambda x: float(x) if x != '' else None


def q(v):
    v = sorted(v)
    qs = S.quantiles(v, n=4, method='inclusive') if len(v) > 1 else [v[0]] * 3
    return S.median(v), qs[0], qs[2]


def sign(pos, neg):
    n = pos + neg
    if n == 0:
        return 1.0
    k = min(pos, neg)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)


def ok(r):
    return fl(r['tok_s']) and r['output_tokens'] and int(r['output_tokens']) >= 300 and r['outcome'] in ('completed', 'stop')


for host, st in [('eu2', 'A'), ('EU', 'A'), ('Studio', 'A'), ('Studio', 'B')]:
    H = [r for r in R if r['host'] == host and r['set'] == st]
    print('##', host if st == 'A' else '%s set %s' % (host, st), 'requests', len(H), 'blocks', len({r['block'] for r in H}))
    clients = [c for c in ['Lc', 'Lr', 'C', 'P'] if any(r['client'] == c for r in H)]
    for c in clients:
        X = [r for r in H if r['client'] == c]
        G = [r for r in X if ok(r)] or [r for r in X if r['outcome'] == 'completed' or fl(r['tok_s'])]
        G = [r for r in G if fl(r['tok_s']) and int(r['output_tokens']) >= 300]
        rate = q([fl(r['tok_s']) for r in G]); tt = q([fl(r['ttfo_s']) for r in G])
        pooled = sum(int(r['output_tokens']) for r in G) / sum(fl(r['stream_s']) for r in G)
        print('%-3s n=%d/%d tok/s %.1f [%.1f, %.1f]  TTFO_s %.2f [%.2f, %.2f]  pooled %.1f' % ((c, len(G), len(X)) + rate + tt + (pooled,)))
    by = {}
    for r in H:
        if fl(r['tok_s']) and r['output_tokens'] and int(r['output_tokens']) >= 300:
            by.setdefault(int(r['block']), {})[r['client']] = r
    for base in ['Lc', 'Lr']:
        for c in [x for x in clients if x != base and not (base == 'Lr' and x == 'Lc')]:
            pr = [(fl(b[c]['tok_s']) / fl(b[base]['tok_s']), fl(b[c]['ttfo_s']) - fl(b[base]['ttfo_s']))
                  for b in by.values() if c in b and base in b]
            if not pr:
                continue
            pos = sum(1 for x, _ in pr if x > 1); neg = sum(1 for x, _ in pr if x < 1)
            tl = sum(1 for _, d in pr if d > 0); te = sum(1 for _, d in pr if d < 0)
            m, lo, hi = q([x for x, _ in pr])
            print('  %s/%s: paired rate ratio median %.3f IQR %.3f-%.3f, n=%d, %s faster %d / slower %d, sign p=%.2g; '
                  'TTFO diff median %+.2fs (%s later %d / earlier %d, sign p=%.2g)'
                  % (c, base, m, lo, hi, len(pr), c, pos, neg, sign(pos, neg), S.median([d for _, d in pr]), c, tl, te, sign(tl, te)))
