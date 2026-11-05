#!/usr/bin/env python3
"""python3 -I report.py data : recompute the L4 step 0 projection from data/ and check it against replay.json."""
import json, os, subprocess, sys
D = sys.argv[1]
here = os.path.dirname(os.path.abspath(__file__))
out = subprocess.run([sys.executable, '-I', os.path.join(here, 'l4_model.py'), D], capture_output=True, text=True, check=True).stdout
print(out)
d = json.load(open(os.path.join(D, 'l4.json')))
b = [r for r in d['rows'] if r['host_class'] in ('macbook', 'linux-a')]
res = dict(repos=len({r['repo'] for r in d['rows']}), rows_budget_classes=len(b), rows_within_budget=sum(r['within_budget'] for r in b),
           rows_over_budget=sum(not r['within_budget'] for r in b), priced_savings_s=int(sum(sum(v.values()) for v in d['priced'].values())),
           stated_waits_that_are_parallel=len(d['floors']))
print(res, d['verdict'])
rp = json.load(open(os.path.join(here, 'replay.json')))
c = rp['arms']['projection']['counts']
assert all(c[k] == res[k] for k in c), (c, res)
assert rp['arms']['projection']['verdict'].startswith(d['verdict'])
print('replay.json matches')
