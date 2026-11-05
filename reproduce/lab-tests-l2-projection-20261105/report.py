#!/usr/bin/env python3
"""python3 -I report.py data : recount the L2 step 0 table from data/l2.json and check it against replay.json."""
import json, os, sys
d = json.load(open(os.path.join(sys.argv[1], 'l2.json')))
rows = d['rows']; rec = [r for r in rows if r['key']]
def cnt(**kw): return sum(all(r[k] == v for k, v in kw.items()) for r in rec)
res = dict(windows_reported=14, windows_found=len(rows), windows_with_key=len(rec), keys_inside_projection=cnt(inside_projection=True),
           request_offset_ms=cnt(key='request_offset_ms'), load_average=cnt(key='load_average'), ms=cnt(key='ms'), status=cnt(key='status'),
           from_log_diff_lines=cnt(key_source='log diff lines'), from_cause_text=cnt(key_source='classified cause text'),
           no_key=len(rows) - len(rec))
for k, v in res.items(): print(f'{k:24} {v}')
print('controls inside projection:', {k: v for k, v in d['controls'].items()})
verdict = 'no' if res['keys_inside_projection'] else ('yes' if res['windows_with_key'] >= 8 and d['controls']['build_request_budget'] else 'unresolved')
print('verdict', verdict)
rp = json.load(open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), 'replay.json')))
c = rp['arms']['projection']['counts']
assert all(c[k] == res[k] for k in c), (c, res)
assert verdict == d['verdict'] == 'yes'
print('replay.json matches')
