#!/usr/bin/env python3
# analyze.py <runs dir> <fixtures.tsv> -> results.json + markdown table on stdout.
# Verdict = the final approve output (out2 if the approve call ran, else out1) with the run's own tree path,
# ISO timestamps and elapsed-second counters normalized; plus exit codes. Compared to arm A per fixture.
import json, os, re, sys, statistics as st, glob
runs, fxf = sys.argv[1], sys.argv[2]
fx = [l.split() for l in open(fxf) if l.strip() and not l.startswith('#')]
def norm(t, root):
    t = t.replace(root, '<ROOT>')
    t = re.sub(r'/[^\s]*/scratch/research/runs/e1-approve/[^/\s]+/tree', '<ROOT>', t)
    t = re.sub(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(\.\d+)?Z?', '<T>', t)
    t = re.sub(r'\(\d+ s\)', '(<n> s)', t)
    t = '\n'.join(l for l in t.splitlines() if not l.startswith('kogen: '))   # progress lines, not verdict
    return t.strip()
R = {}
for d in sorted(glob.glob(os.path.join(runs, '*.*.*'))):
    p = os.path.join(d, 'result.json')
    if '.aside-' in d or os.path.exists(os.path.join(d, 'killed')): continue   # stopped by me for host load
    if os.path.exists(p): r = json.load(open(p))
    elif os.path.basename(d) in os.environ.get('RECONSTRUCT', '').split(',') and os.path.exists(os.path.join(d, 'load0')) and os.path.exists(os.path.join(d, 'out1')):
        # run1.sh was overwritten in place under these runs (09:30Z), so their shell died after approve finished;
        # wall = last approve output mtime - load0 mtime (written just before t0), to the second.
        fx_, arm_, rep_ = os.path.basename(d).rsplit('.', 2)
        t0 = os.path.getmtime(os.path.join(d, 'load0'))
        o1 = os.path.getmtime(os.path.join(d, 'out1'))
        o2 = os.path.join(d, 'out2')
        txt1 = open(os.path.join(d, 'out1'), errors='replace').read()
        import re as _re
        H = (_re.findall(r'[0-9a-f]{64}', txt1) or [None])[-1]
        if H and not os.path.exists(o2): continue   # second call never ran: incomplete
        end = os.path.getmtime(o2) if os.path.exists(o2) else o1
        slug_ = dict((l.split()[0], l.split()[1]) for l in open(fxf) if l.strip() and not l.startswith('#'))[fx_]
        r = dict(fixture=fx_, slug=slug_, arm=arm_, rep=int(rep_), start=t0, wall_s=round(end - t0, 3), call1_s=round(o1 - t0, 3),
                 rc1=None, rc2=None, fallback=0, digest=H, reconstructed=1, digest_source='preview' if arm_ in ('A', 'B') else None)
    else: continue
    if r['rep'] < 1: continue
    if r['arm'] in ('C', 'BC') and r.get('digest_source') != 'labdigest': r['arm'] += '-rec'  # shape-record digest protocol (before 09:30Z)
    root = os.path.join(d, 'tree')
    fin = 'out2' if os.path.exists(os.path.join(d, 'out2')) else 'out1'
    txt = open(os.path.join(d, fin), errors='replace').read()
    r['final'] = fin
    r['verdict'] = norm(txt, root)
    r['verdict_last'] = r['verdict'].splitlines()[-1] if r['verdict'] else ''
    m = re.search(r'([a-z_]+/[a-z_]+): (.*)', r['verdict'])
    r['refusal'] = m.group(0) if m else None
    r['exit'] = r['rc2'] if fin == 'out2' else r['rc1']
    allout = ''.join(open(os.path.join(d, f), errors='replace').read() for f in ('out1', 'out2') if os.path.exists(os.path.join(d, f)))
    m2 = re.search(r'intent/step_ownership_collision: .*', allout)
    r['binding'] = norm(m2.group(0), root) if m2 else 'no collision'
    m3 = re.search(r'^([a-z_]+/[a-z_]+):', r['verdict'], re.M)
    r['outcome'] = m3.group(1) if m3 else ('approved' if re.search(r'^Approved', r['verdict'], re.M) or 'Next: kogen intent build' in r['verdict'] else 'other')
    R.setdefault(r['fixture'], []).append(r)
out = {'fixtures': [], 'runs': [r for v in R.values() for r in v]}
med = lambda xs: round(st.median(xs), 1) if xs else None
rows = []
for name, slug, pool, kind in fx:
    rs = R.get(name, [])
    by = {a: [r for r in rs if r['arm'] == a] for a in ['A', 'B', 'C', 'BC']}
    a = by['A'][0] if by['A'] else None
    ident = {}
    for arm in ['B', 'C', 'BC']:
        ident[arm] = None if not a or not by[arm] else all(r['verdict'] == a['verdict'] and (r['exit'] == a['exit'] or r.get('reconstructed') or a.get('reconstructed')) for r in by[arm])
    bident = {arm: (None if not a or not by[arm] else all(r['binding'] == a['binding'] for r in by[arm])) for arm in ['B', 'C', 'BC']}
    f = dict(binding_identical=bident, A_binding=a['binding'] if a else None, outcomes={k: [r['outcome'] for r in v] for k, v in by.items()},
             loads={k: [r['load0'].split()[0] if r.get('load0') else None for r in v] for k, v in by.items()}, fixture=name, slug=slug, kind=kind, n={k: len(v) for k, v in by.items()},
             median_s={k: med([r['wall_s'] for r in v]) for k, v in by.items()},
             walls={k: [r['wall_s'] for r in v] for k, v in by.items()},
             A_exit=a['exit'] if a else None, A_verdict_last=a['verdict_last'] if a else None, A_refusal=a['refusal'] if a else None,
             identical=ident, fallback={k: sum(r['fallback'] for r in v) for k, v in by.items()},
             cut_pct={k: (round(100 * (1 - med([r['wall_s'] for r in by[k]]) / a['wall_s']), 1) if a and by[k] else None) for k in ['B', 'C', 'BC']})
    out['fixtures'].append(f)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(fxf)), 'results.json'), 'w'), indent=1)
print('| fixture | kind | A s (n=1) | B median s (n) | C median s (n) | B+C median s (n) | cut B / C / B+C | outcome A / B / C / B+C | binding verdict identical B/C/B+C | final identical B/C/B+C |')
print('|---|---|---|---|---|---|---|---|---|---|')
for f in out['fixtures']:
    m, n, c, i = f['median_s'], f['n'], f['cut_pct'], f['identical']
    yn = lambda v: '-' if v is None else ('yes' if v else '**NO**')
    v = (f['A_refusal'] or (f['A_verdict_last'] or '-'))[:70]
    o = f['outcomes']; bi = f['binding_identical']
    oc = ' / '.join(','.join(sorted(set(o[k]))) or '-' for k in ['A', 'B', 'C', 'BC'])
    print(f"| {f['fixture']} | {f['kind']} | {m['A']} | {m['B']} ({n['B']}) | {m['C']} ({n['C']}) | {m['BC']} ({n['BC']}) | {c['B']}% / {c['C']}% / {c['BC']}% | {oc} | {yn(bi['B'])}/{yn(bi['C'])}/{yn(bi['BC'])} | {yn(i['B'])}/{yn(i['C'])}/{yn(i['BC'])} |")
