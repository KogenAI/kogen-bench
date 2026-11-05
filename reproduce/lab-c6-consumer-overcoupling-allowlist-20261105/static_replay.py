#!/usr/bin/env python3
"""static_replay.py: key-level replay (no Go run, no host). Is each recorded red diff key masked by the deny-list of the consumer version of its
window, and ignored by the allow-list projection of budget_allow_test.go? Reads data/deny-lists.json and data/recorded-diffs.json."""
import json, os
h = os.path.dirname(os.path.abspath(__file__)); D = json.load(open(h + '/data/deny-lists.json')); R = json.load(open(h + '/data/recorded-diffs.json'))
masked = lambda v, k: k in D[v]['volatile_keys'] or any(k.endswith(s) for s in D[v]['volatile_suffixes'])
ALLOW = {'event', 'role', 'repair', 'pass', 'name', 'tool', 'outcome', 'count', 'limit'}
allow = lambda k: k in ALLOW or 'budget' in k
res = dict(keys=len(R), red_under_window_version=sum(not masked(r['version'], r['key']) for r in R), still_red_at_head=sum(not masked('HEAD', r['key']) for r in R),
           red_under_allow_list=sum(allow(r['key']) for r in R), mutation_key_kept_by_allow_list=allow('build_request_budget'),
           deny_list_versions_that_changed_the_mask=sum(1 for a, b in (('V0', 'V1'), ('V1', 'V2'), ('V2', 'V3')) if (D[a]['volatile_keys'], D[a]['volatile_suffixes']) != (D[b]['volatile_keys'], D[b]['volatile_suffixes'])))
for r in R: print(r['key'], r['windows'], r['version'], 'red under deny-list' if not masked(r['version'], r['key']) else 'masked', '| at head:', 'masked' if masked('HEAD', r['key']) else 'RED', '| allow-list:', 'ignored' if not allow(r['key']) else 'compared')
print(json.dumps(res))
json.dump(res, open(h + '/data/results.json', 'w'), indent=1)
