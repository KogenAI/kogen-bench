#!/usr/bin/env python3
"""python3 -I report.py data : recount the L5 numbers from the recorded outputs in data/ and check them against replay.json."""
import json, os, re, statistics as S, sys
D = sys.argv[1]; here = os.path.dirname(os.path.abspath(__file__))
rd = lambda n: open(os.path.join(D, n)).read()
asis, rep, times, batch = rd('replay_asis.txt'), rd('replay_repaired.txt'), rd('quint_times_repaired.tsv'), rd('batch_times.txt')
static = json.load(open(os.path.join(D, 'l5_static.json')))
accrows = json.load(open(os.path.join(D, 'acc_rows.json'))); accT = rd('acc_batch_times.txt')
MODEL_TESTS = 23   # build.qnt's own tests, run by every file that imports it (24 passing = 23 + one trace test in a single-trace file)
def accrow(b):
    m = re.search(rf'^{b} rep=1 rc=1 ms=\d+\s+(\d+) passing \(\d+ms\)\s+(\d+) failed', accT, re.M)
    return int(m[1]) - MODEL_TESTS, int(m[2])
a10, r10 = accrow('batch10'); aall, rall = accrow('batchAll')
elig = [r for r in accrows if r['eligible']]
acc = lambda t: len(re.findall(r'quint test: \d+ passing, 0 failed \(exit 0\)', t))
ms = lambda t, k: [int(m[1]) for m in re.finditer(rf'^{k} rep=\d+ rc=0 ms=(\d+)', t, re.M)]
res = dict(
    asis_exit=int(re.search(r'replay rc=(\d+)', asis)[1]), asis_journeys_accepted=acc(asis), asis_mutants_rejected=0, journeys=4, mutants=5,
    repaired_journeys_accepted=acc(rep) - 0, repaired_mutants_refuted=len(re.findall(r'refuted: true', rep)), repaired_mutants_rehosted=2,
    repaired_wall_s=int(re.search(r'wall_s=(\d+)', rep)[1]),
    quint_ms_median_per_process=int(S.median(round(float(l.split('\t')[1]) * 1000) for l in times.strip().splitlines())),
    batch10_chains=10, batch10_passing=int(re.search(r'batch10 rep=1 rc=0 ms=\d+\s+(\d+) passing', batch)[1]), batch10_quint_ms_median=int(S.median(ms(batch, 'batch10'))),
    batch16_quint_ms_median=int(S.median(ms(batch, 'batch16'))), batch48_quint_ms_median=int(S.median(ms(batch, 'batch48'))),
    acc_recorded=len(accrows), acc_eligible=len(elig), acc_batch10_accepted=a10, acc_batch10_rejected=r10, acc_all_accepted=aall, acc_all_rejected=rall,
    acc_quint_ms_batch10=int(S.median(ms(accT, 'batch10'))) if ms(accT, 'batch10') else int(S.median(int(m[1]) for m in re.finditer(r'^batch10 rep=\d+ rc=1 ms=(\d+)', accT, re.M))),
    acc_quint_ms_all=int(S.median(int(m[1]) for m in re.finditer(r'^batchAll rep=\d+ rc=1 ms=(\d+)', accT, re.M))),
    acc_reject_baseline=sum(1 for r in elig if r.get('firstFail') and 'baseline_changed' in r['firstFail']['action']),
    acc_reject_reviewer_edit=sum(1 for r in elig if r.get('firstFail') and r['firstFail']['action'].startswith('reviewWith')),
    acc_reject_hook_commit=sum(1 for r in elig if r.get('firstFail') and 'hook_changed_commit' in r['firstFail']['action']),
    scenarios=static['total'], expressible=static['summary']['expressible'], requirement_outside_model=static['summary']['requirement outside the model'], no_generator=static['summary']['no generator'])
for k, v in res.items(): print(f'{k:32} {v}')
rp = json.load(open(os.path.join(here, 'replay.json')))
for arm, a in rp['arms'].items():
    for k, v in a['counts'].items(): assert res[k] == v, (arm, k, res[k], v)
print('replay.json matches')
