#!/usr/bin/env python3
"""L4 step 0 input: per-repo suite wall times from the existing heavy-lock logs (end rc=N Ss <cmd path>), window 3 Nov 09Z - 5 Nov 09Z.
usage: heavy_suites.py <heavy log dir> <slug-to-repo tsv (slug, repo columns)> <out.json> <host-class map json: {"<host name substring>": "<class>"}>"""
import csv, datetime as dt, glob, json, os, re, statistics as S, sys, collections
bs, stats, out, cmap = sys.argv[1:5]
cmap = json.load(open(cmap))
REPO = {'loop': 'kogen-loop'}
T0 = dt.datetime(2026, 11, 3, 9, tzinfo=dt.timezone.utc); T1 = dt.datetime(2026, 11, 5, 9, tzinfo=dt.timezone.utc)
repo_of = {r['slug']: REPO.get(r['repo'], r['repo']) for r in csv.DictReader(open(stats), delimiter='\t')}
res = collections.defaultdict(list)
for f in sorted(glob.glob(os.path.join(bs, 'heavy-*.log'))):
    name = os.path.basename(f)[6:-4]; host = next((c for k, c in cmap.items() if k in name), name); L = open(f).read().splitlines()
    end = dt.datetime.strptime(L[-1].split()[1], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=dt.timezone.utc)
    day = end.date(); prev = None; recs = []
    for l in reversed(L[:-1]):
        m = re.match(r'(\d\d):(\d\d):(\d\d)Z (\d+) (\S+) (.*)', l)
        if not m: continue
        s = int(m[1]) * 3600 + int(m[2]) * 60 + int(m[3])
        if prev is not None and s > prev + 3600: day -= dt.timedelta(days=1)
        prev = s
        t = dt.datetime.combine(day, dt.time(), tzinfo=dt.timezone.utc) + dt.timedelta(seconds=s)
        if t < T0 - dt.timedelta(hours=3): break
        recs.append((t, m[4], m[5], m[6]))
    for t, pid, ev, rest in recs:
        if ev == 'end' and T0 <= t <= T1:
            m2 = re.match(r'rc=(\d+) (\d+)s (.*)', rest)
            if not m2: continue
            m3 = re.search(r'heavy-cmds/([^/]+)/(go-test|test)\.sh', m2[3])
            if m3 and repo_of.get(m3[1]): res[(repo_of[m3[1]], m3[2], host)].append((int(m2[2]), int(m2[1])))
rows = []
for (repo, script, host), v in sorted(res.items()):
    ds = sorted(d for d, rc in v)
    rows.append(dict(repo=repo, script=script, host_class=host, n=len(v), median_s=S.median(ds), p90_s=ds[max(0, int(len(ds) * .9 + .5) - 1)], max_s=ds[-1], min_s=ds[0], fails=sum(1 for d, rc in v if rc)))
json.dump(rows, open(out, 'w'), indent=1)
for r in rows:
    if r['n'] >= 3: print(f"{r['repo']:20} {r['script']:8} {r['host_class'][-18:]:18} n={r['n']:4} med={r['median_s']:6.0f} p90={r['p90_s']:6.0f} min={r['min_s']:5} max={r['max_s']:6} fail={r['fails']}")
