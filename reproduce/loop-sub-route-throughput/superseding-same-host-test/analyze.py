"""routeab4 analysis: per host/probe median [IQR] of tokens/s after first output and time to first output;
paired ratios vs loop (per block) with an exact two-sided sign test. usage: analyze.py file.jsonl ..."""
import json, sys, statistics as S, math
def q(v):
    v = sorted(v); n = len(v)
    if n == 0: return None
    qs = S.quantiles(v, n=4, method='inclusive') if n > 1 else [v[0]] * 3
    return S.median(v), qs[0], qs[2]
def sign(pos, neg):
    n = pos + neg
    if n == 0: return 1.0
    k = min(pos, neg); p = 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, p)
def ok(r): return r.get('rate_out') and r.get('output') and r['output'] >= 300 and not r.get('error')
R = [json.loads(l) for f in sys.argv[1:] for l in open(f) if l.strip()]
for host in sorted({r['host'] for r in R}):
    H = [r for r in R if r['host'] == host]
    print('##', host, 'records', len(H), 'blocks', len({r['block'] for r in H}))
    probes = [p for p in ['Lc', 'Lr', 'C', 'P'] if any(r['probe'] == p for r in H)]
    for p in probes:
        X = [r for r in H if r['probe'] == p]; G = [r for r in X if ok(r)]
        rate = q([r['rate_out'] for r in G]); vis = q([r['rate_visible'] for r in G if r.get('rate_visible')])
        tt = q([r['first_out_s'] for r in G]); out = q([r['output'] for r in G])
        rs = sorted({r.get('reasoning') for r in G}, key=str); tiers = sorted({str(r.get('tier')) for r in G})
        bad = [(r['block'], r.get('error') or r.get('output')) for r in X if not ok(r)]
        ov = sum(1 for r in X if r.get('overlap_start') or r.get('overlap_end'))
        f = lambda t: '%.1f [%.1f, %.1f]' % t if t else '-'
        g = lambda t: '%.2f [%.2f, %.2f]' % t if t else '-'
        print(f'{p:3} n={len(G)}/{len(X)} rate {f(rate)} visible {f(vis)} ttfo_s {g(tt)} output {f(out)} reasoning {rs} tier {tiers} overlap {ov}/{len(X)} excluded {bad}')
    by = {}
    for r in H:
        if ok(r): by.setdefault(r['block'], {})[r['probe']] = r
    for base in ['Lc', 'Lr']:
        for p in [x for x in probes if x != base and not (base == 'Lr' and x == 'Lc')]:
            pr = [(b[p]['rate_out'] / b[base]['rate_out'], b[p]['first_out_s'] - b[base]['first_out_s']) for b in by.values() if p in b and base in b]
            if not pr: continue
            pos = sum(1 for x, _ in pr if x > 1); neg = sum(1 for x, _ in pr if x < 1)
            tp = sum(1 for _, d in pr if d > 0); tn = sum(1 for _, d in pr if d < 0)
            print(f'  {p}/{base}: paired rate ratio median {S.median([x for x,_ in pr]):.3f} IQR {q([x for x,_ in pr])[1]:.3f}-{q([x for x,_ in pr])[2]:.3f}, n={len(pr)}, {p} faster in {pos}, slower in {neg}, sign p={sign(pos,neg):.3g}; '
                  f'TTFO diff median {S.median([d for _,d in pr]):+.2f}s ({p} later {tp}/earlier {tn}, sign p={sign(tp,tn):.3g})')
