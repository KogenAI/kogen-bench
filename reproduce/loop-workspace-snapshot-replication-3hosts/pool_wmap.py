#!/usr/bin/env python3
"""Pool the three wmap cohorts (registered rule: simple sum of paired blocks; host as stratum).
Usage: pool_wmap.py <out dir> eu=runs-eu.csv lm=runs-laptop.csv st=runs-studio.csv. Writes analysis.json and pairs.csv to <out dir>."""
import csv, json, sys, pathlib
out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
H = {}
for a in sys.argv[2:]:
    k, p = a.split('=', 1); H[k] = list(csv.DictReader(open(p)))
def num(x):
    try: return float(x)
    except Exception: return 0.0
def pairs_of(rows, host):
    by = {(r['task'], r['rep'], r['arm']): r for r in rows}
    P = []; cens = []
    for (t, rep, a), r in sorted(by.items()):
        if a != 'base': continue
        w = by.get((t, rep, 'wmap'))
        if w is None: cens.append((host, t, rep, 'wmap missing')); continue
        if 'agent_error' in (r['outcome'], w['outcome']): cens.append((host, t, rep, 'provider-dropped cell (agent_error), pair left out as registered')); continue
        P.append((host, t, rep, r, w))
    for (t, rep, a) in by:
        if a == 'wmap' and (t, rep, 'base') not in by: cens.append((host, t, rep, 'base missing'))
    return P, cens
allp = {}; cens = {}
for h, rows in H.items(): allp[h], cens[h] = pairs_of(rows, h)
# fired = tasks where wmap request-1 input exceeds base by >500 in every pair, per cohort; require same in all
fired_by = {}
for h, P in allp.items():
    d = {}
    for _, t, rep, b, w in P: d.setdefault(t, []).append(num(w['req1_input']) - num(b['req1_input']))
    fired_by[h] = {t for t, v in d.items() if min(v) > 500}
fired = set.intersection(*fired_by.values())
assert all(f == fired for f in fired_by.values()), fired_by
def agg(P):
    def s(key, arm, sel=lambda t: True): return sum(num(p[3 if arm == 'base' else 4][key]) for p in P if sel(p[1]))
    R = {}
    for name, sel in (('all', lambda t: True), ('fired', lambda t: t in fired), ('nofire', lambda t: t not in fired)):
        R[name] = {k: {'base': s(k, 'base', sel), 'wmap': s(k, 'wmap', sel)} for k in ('orient_pre', 'requests', 'input', 'output', 'usd', 'wall')}
    disc = [(p[0], p[1], p[2], p[3]['passed'], p[4]['passed']) for p in P if (p[3]['passed'] == 'True') != (p[4]['passed'] == 'True')]
    R['pairs'] = len(P)
    R['pass'] = {'base': sum(p[3]['passed'] == 'True' for p in P), 'wmap': sum(p[4]['passed'] == 'True' for p in P)}
    R['discordant'] = disc
    R['pairs_fewer'] = sum(num(p[4]['requests']) < num(p[3]['requests']) for p in P)
    R['pairs_equal'] = sum(num(p[4]['requests']) == num(p[3]['requests']) for p in P)
    R['pairs_more'] = sum(num(p[4]['requests']) > num(p[3]['requests']) for p in P)
    o = R['all']['orient_pre']; R['orient_reduction'] = 1 - o['wmap'] / o['base']
    f = R['fired']
    R['fired_orient_pre'] = f['orient_pre']
    R['fired_pairs'] = sum(p[1] in fired for p in P)
    R['rules'] = {'orientation_fall_ge_50pct': R['orient_reduction'] >= .5,
                  'pass_not_worse': sum(d[3] == 'True' and d[4] != 'True' for d in disc) <= sum(d[4] == 'True' and d[3] != 'True' for d in disc),
                  'input_not_up_fired': f['input']['wmap'] <= f['input']['base'],
                  'output_not_up_fired': f['output']['wmap'] <= f['output']['base']}
    R['input_fired_change_pct'] = 100 * (f['input']['wmap'] / f['input']['base'] - 1)
    R['output_fired_change_pct'] = 100 * (f['output']['wmap'] / f['output']['base'] - 1)
    return R
res = {h: agg(P) for h, P in allp.items()}
res['pooled'] = agg([p for P in allp.values() for p in P])
res['pooled_eu_lm'] = agg(allp['eu'] + allp['lm']) if 'eu' in allp and 'lm' in allp else None
res['pooled_eu_st'] = agg(allp['eu'] + allp['st']) if 'eu' in allp and 'st' in allp else None
res['fired_tasks'] = sorted(fired)
res['censored'] = cens
res['not_run'] = {h: sorted({(t, r) for t in {x['task'] for x in rows} for r in ('r1', 'r2')} - {(x['task'], x['rep']) for x in rows if x['arm'] == 'base'}) for h, rows in H.items()}
# per-task input on fired tasks, studio, and pooled per-pair input deltas for diagnostics
diag = []
for h, P in allp.items():
    for _, t, rep, b, w in P:
        if t in fired: diag.append({'host': h, 'task': t, 'rep': rep, 'base_in': num(b['input']), 'wmap_in': num(w['input']), 'base_req': num(b['requests']), 'wmap_req': num(w['requests']), 'd_in': num(w['input']) - num(b['input'])})
res['fired_pairs_input'] = diag
(out / 'analysis.json').write_text(json.dumps(res, indent=1))
with (out / 'pairs.csv').open('w', newline='') as f:
    w = csv.writer(f); w.writerow(['host', 'task', 'rep', 'fires', 'base_pass', 'wmap_pass', 'base_outcome', 'wmap_outcome', 'base_orient', 'wmap_orient', 'base_req', 'wmap_req', 'base_in', 'wmap_in', 'base_out', 'wmap_out', 'base_usd', 'wmap_usd', 'base_wall', 'wmap_wall'])
    for h, P in allp.items():
        for _, t, rep, b, x in P:
            w.writerow([h, t, rep, int(t in fired), b['passed'], x['passed'], b['outcome'], x['outcome']] + [v for k in ('orient_pre', 'requests', 'input', 'output', 'usd', 'wall') for v in (b[k], x[k])])
for h in list(allp) + ['pooled']:
    r = res[h]; print(h, r['pairs'], 'orient', r['all']['orient_pre'], round(100 * r['orient_reduction'], 1), 'req', r['all']['requests'], 'pass', r['pass'], 'disc', r['discordant'], 'fired in', r['fired']['input'], round(r['input_fired_change_pct'], 2), 'out', r['fired']['output'], round(r['output_fired_change_pct'], 2), 'fewer/eq/more', r['pairs_fewer'], r['pairs_equal'], r['pairs_more'], r['rules'])
print('censored', cens, 'fired', sorted(fired))
