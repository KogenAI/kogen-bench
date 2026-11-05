#!/usr/bin/env python3
"""python3 -I report.py data : recount the L8 step 0 numbers from data/ and check them against replay.json."""
import collections, csv, json, os, re, sys
D = sys.argv[1]; here = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(D, 'step_files.json')))['rows']
sp = [r for r in rows if r['spawns_go_test']]
named = [r for r in sp if r['names']]
def klass(r):
    if r['missing']: return 'stale'
    if r['generated_by_step'] or r['driver_in_repo']: return 'driver'
    return 'repo_tests'
kc = collections.Counter(klass(r) for r in named)
s6 = collections.defaultdict(list)
for r in csv.DictReader(open(os.path.join(D, 'section6_names.tsv')), delimiter='\t'): s6[r['name']].append(r)
hits = []
for r in sp:
    for n in r['names']:
        for k, v in s6.items():
            if (k == n or (r['name_basis'] == 'run-argument' and len(n) >= 15 and k.startswith(n))) and any(x['verdict'] in ('DEL', 'REW', 'MOVE') for x in v):
                hits.append((r['repo'], r['file'], n, k, sorted({x['verdict'] for x in v})))
# Manual adjudication of the hits (read against the request's rows): these are not changes to a test the step file runs.
FALSE = {('kogen-shaping', 'features/steps/fix-k-shape-kill-group-zombie__steps.js', 'TestRunKillGroupOnExit'): 'it is the replacement the DEL row names, so it survives',
         ('kogen-setup', 'features/steps/k-setup-command-leaves-project-folder__validate.js', 'TestInit'): 'a prefix of a land-red list, not a verdict row'}
real = [h for h in hits if (h[0], h[1], h[2]) not in FALSE]
tr_b, tr_a = (open(os.path.join(D, f)).read() for f in ('spec_trace_before.txt', 'spec_trace_after.txt'))
summ = re.search(r'requirements (\d+), scenarios (\d+)', tr_b)
mv = dict(l.split() for l in open(os.path.join(D, 'moved_counts.txt')).read().splitlines())
res = dict(step_files_total=len(rows), step_files_go_test=len(sp), with_names=len(named), without_names=len(sp) - len(named),
           names_from_run_argument=sum(1 for r in named if r['name_basis'] == 'run-argument'), files_repo_tests=kc['repo_tests'], files_driver=kc['driver'], files_stale=kc['stale'],
           stale_on_run_argument=sum(1 for r in named if r['name_basis'] == 'run-argument' and klass(r) == 'stale'),
           section6_hit_files=len({(h[0], h[1]) for h in real}), section6_hits_del=sum('DEL' in h[4] for h in real), section6_hits_rew=sum('REW' in h[4] for h in real), section6_hits_move=sum('MOVE' in h[4] for h in real),
           requirements=int(summ[1]), scenarios=int(summ[2]), trace_identical=int(tr_b == tr_a), step_files_moved=int(mv['moved-all']))
for k, v in res.items(): print(f'{k:26} {v}')
print('without_names share: %.1f%%' % (100 * res['without_names'] / res['step_files_go_test']))
rp = json.load(open(os.path.join(here, 'replay.json')))
for arm, a in rp['arms'].items():
    for k, v in a['counts'].items(): assert res[k] == v, (arm, k, res[k], v)
print('replay.json matches')
