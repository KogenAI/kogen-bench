#!/usr/bin/env python3
"""Reads data/ab/*.metrics.json (+ *.events.tsv) and data/census1/*, prints results.json. Usage: python3 -I report.py <data dir> [subdir=ab] [arms=ABC]"""
import csv, glob, json, os, re, statistics, sys, math
D = sys.argv[1]
SUB = sys.argv[2] if len(sys.argv) > 2 else 'ab'
ARMS = sys.argv[3] if len(sys.argv) > 3 else 'ABC'
M = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(D, SUB + '/*.metrics.json')))]
def pv(m): return all(x in m['verdict'] for x in ('--- PASS',)) and m['verdict'].count('--- PASS') == 3 and 'FAIL' not in m['verdict'] and m['rc'] == 0
res = {'arms': {}, 'rounds': {}}
_by = {}
for m in M:
    if not m['watched']: _by.setdefault(m['tag'], set()).add(m['arm'])
complete = [t for t, s in _by.items() if s == set(ARMS)]
unw = [m for m in M if not m['watched']]
wat = [m for m in M if m['watched'] and m['tag'] != 'w0']
for a in ARMS:
    u = [m for m in unw if m['arm'] == a and m['tag'] in {k for k in complete}]; w = [m for m in wat if m['arm'] == a]
    res['arms'][a] = dict(
        unwatched_runs=len(u), all_pass=sum(pv(m) for m in u), median_wall_s=round(statistics.median(m['wall'] for m in u), 2),
        median_fseventsd_cpu_s=round(statistics.median(m['fseventsd_cpu_s'] for m in u), 2),
        watched_runs=len(w), files_created_per_window=[m['files_created_events'] for m in w],
        files_created_per_test_run=round(statistics.mean(m['files_created_events'] for m in w) / 3, 0) if w else None)
for tag in sorted({m['tag'] for m in unw}, key=lambda t: int(t[1:])):
    rr = {m['arm']: dict(wall=m['wall'], cpu=m['fseventsd_cpu_s'], load5=m['load5_start']) for m in unw if m['tag'] == tag}
    if set(rr) == set(ARMS): res['rounds'][tag] = rr
def sign_p(k, n): return sum(math.comb(n, i) for i in range(k, n + 1)) / 2 ** n
for x in ARMS[1:]:
    lower = sum(1 for t, r in res['rounds'].items() if x in r and 'A' in r and r[x]['cpu'] < r['A']['cpu'])
    n = sum(1 for t, r in res['rounds'].items() if x in r and 'A' in r)
    fa = res['arms']['A']['files_created_per_test_run']; fx = res['arms'][x]['files_created_per_test_run']
    res['arms'][x].update(cpu_lower_rounds=f'{lower}/{n}', sign_test_p=round(sign_p(lower, n), 4), files_reduction_pct=round(100 * (1 - fx / fa), 1) if fa else None,
                          wall_ratio_vs_A=round(res['arms'][x]['median_wall_s'] / res['arms']['A']['median_wall_s'], 3),
                          cpu_ratio_vs_A=round(res['arms'][x]['median_fseventsd_cpu_s'] / res['arms']['A']['median_fseventsd_cpu_s'], 3))
# source-copy upper bound from the instrumented A runs
def comp(f):
    c = {}
    for r in list(csv.reader(open(f), delimiter='\t'))[1:]:
        if r[0] == '#TOTAL': continue
        c[r[0]] = c.get(r[0], 0) + int(r[1])
    return c
src = tot = 0
for f in glob.glob(os.path.join(D, SUB + '/A[w]*.events.tsv')):
    if f.endswith('Aw0.events.tsv'): continue
    c = comp(f); tot += sum(c.values()); src += sum(v for k, v in c.items() if re.search(r'TestAssemblyUsesThePinnedComponents//?(cli|docs|test|packaging)$', k))
res['source_copy_upper_bound_pct_of_A_files'] = round(100 * src / tot, 2) if tot else None
print(json.dumps(res, indent=1))
