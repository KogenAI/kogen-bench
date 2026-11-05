#!/usr/bin/env python3
"""L4 step 0 extraction (reads private delivery state; its output data/*.json is what the pack publishes).
usage: extract_inputs.py <delivery dir> <data dir>"""
import glob, json, os, re, statistics as S, subprocess, sys, collections
dl, out = sys.argv[1:3]
# adoption step seconds, 3 Nov 16Z .. 5 Nov (window of the heavy-lock extract)
st = collections.defaultdict(list)
for f in sorted(glob.glob(os.path.join(dl, 'state/adoptions/202611*T*.json'))):
    if os.path.basename(f) < '20261103T160000Z': continue
    d = json.load(open(f))
    for s in d.get('steps', []):
        st[(('final' if s['label'] == 'final' else 'variant'), s['name'])].append(s['seconds'])
steps = [dict(label=k[0], step=k[1], n=len(v), median_s=S.median(v), min_s=min(v), max_s=max(v)) for k, v in sorted(st.items())]
json.dump(steps, open(os.path.join(out, 'adoption_steps.json'), 'w'), indent=1)
# package-level ok/FAIL seconds from adoption and land logs of the window
import time
pk = collections.defaultdict(list)
for f in glob.glob(os.path.join(dl, 'logs/adopt/*-go.out')) + glob.glob(os.path.join(dl, 'logs/land/*.log')):
    if os.path.getmtime(f) < time.mktime((2026, 11, 3, 16, 0, 0, 0, 0, 0)): continue
    for l in open(f, errors='replace'):
        m = re.match(r'(ok|FAIL)\s+(\S+)\s+([\d.]+)s\b', l)
        if m: pk[m[2].replace('github.com/KogenAI/', '')].append(float(m[3]))
pkgs = [dict(package=k, n=len(v), median_s=round(S.median(v), 1), max_s=max(v)) for k, v in sorted(pk.items(), key=lambda kv: -S.median(kv[1])) if len(v) >= 3 and S.median(v) >= 2]
json.dump(pkgs, open(os.path.join(out, 'package_times.json'), 'w'), indent=1)
# static counts at each repo's main snapshot
rows = []
for r in ['kogen', 'kogen-build', 'kogen-shaping', 'kogen-verification', 'kogen-review', 'kogen-loop', 'kogen-coordinator', 'kogen-setup', 'kogen-executor']:
    g = lambda *a: subprocess.run(['git', '-C', os.path.join(dl, r)] + list(a), capture_output=True, text=True).stdout
    tests = len(g('grep', '-h', '^func Test', 'HEAD', '--', '*_test.go').splitlines())
    par = len(g('grep', '-h', 't.Parallel()', 'HEAD', '--', '*_test.go').splitlines())
    rows.append(dict(repo=r, sha=g('rev-parse', 'HEAD').strip(), tests=tests, parallel_calls=par))
json.dump(rows, open(os.path.join(out, 'static_counts.json'), 'w'), indent=1)
print(len(steps), len(pkgs), len(rows))
