#!/usr/bin/env python3
"""Stage 1 gate report: python3 -I report.py data/gate.tsv data/targets.json [results.json]. Model-free; reads only the two data files."""
import json, sys
rows = [l.rstrip('\n').split('\t') for l in open(sys.argv[1]) if l.strip()]
T = json.load(open(sys.argv[2]))
out = sys.argv[3] if len(sys.argv) > 3 else None
secs = {}
for r in rows:
    secs[(r[0], r[1])] = dict(rc=int(r[2]), secs=int(r[3]), load1=float(r[4]))
res = {}
for t, v in T.items():
    full = secs[(t, 'full1')]['secs']
    d = dict(full_secs=full, tests_total=v['all_tests'], changed_lib_files=len(v['changed']))
    for form in ('wide', 'narrow'):
        files = v[form]
        d[form + '_files'] = len(files)
        s = secs.get((t, form))
        # a form with no mapped test, or not run because it equals the other form, is judged below
        d[form + '_secs'] = s['secs'] if s else None
        d[form + '_ratio'] = round(s['secs'] / full, 3) if s else None
    # fallback rule: a change that maps to no test runs the full suite (ratio 1.0); no check at all is not a cheaper check
    for form in ('wide', 'narrow'):
        r = d[form + '_ratio']
        if d[form + '_files'] == 0: r = 1.0
        elif r is None: r = d['wide_ratio']
        d[form + '_ratio_fallback'] = r
    res[t] = d
def passes(form, free_empty=False):
    n = 0
    for t, v in T.items():
        d = res[t]
        r = d[form + '_ratio_fallback']
        if free_empty and d[form + '_files'] == 0: r = 0.0
        n += r <= 0.5
    return n
res['_gate'] = dict(
    rule='targeted/full <= 0.5 on at least 3 of the 4 tasks',
    primary_form='wide (tests that mirror a changed file or reference a changed module)',
    wide_pass_count=passes('wide'), narrow_pass_count=passes('narrow'),
    wide_pass_count_if_unmapped_counts_free=passes('wide', True),
    verdict='PASS' if passes('wide') >= 3 else 'STOP: A2 no headroom')
print(json.dumps(res, indent=1))
if out: json.dump(res, open(out, 'w'), indent=1)
