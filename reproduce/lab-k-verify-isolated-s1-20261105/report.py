#!/usr/bin/env python3
"""analyze.py <runs dir> <mutants dir> -> metrics.json + printed tables. Reads the *.scen.json / *.pair.json files written by orch.py."""
import sys, os, json, glob, statistics as st, collections, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v1prime
RUNS, MUT = sys.argv[1], sys.argv[2]
HAZ = {'k-repin-adapt-f2e30a4', 'deterministic-check-gate'}
BUD = [5, 10, 20, 30]
def L(name):
    p = f'{RUNS}/{name}.scen.json'
    return json.load(open(p)) if os.path.exists(p) else None
def keyed(sc):
    c = collections.Counter(); out = {}
    for s in sc['scen']:
        k = (s['uri'][s['uri'].find('.kogen/'):], s['name']); c[k] += 1; out[(k, c[k])] = s
    return out
M = {}
# ---- V4 on the real suite ----
reps = [L(f'v4-r{k}') for k in range(1, 4)]; reps = [r for r in reps if r]
GOCORE = [s for r in reps[:1] for s in r['scen'] if s['intent'] == 'go-core-migration']
for r in reps:
    r['T_sample'] = sum(s['wall'] for s in r['scen'] if s['intent'] != 'go-core-migration'); r['scen'] = [s for s in r['scen'] if s['intent'] != 'go-core-migration']
v4 = dict(repeats=len(reps), run_wall_s=[round(r['wall'], 1) for r in reps], T_median=round(st.median([r['T_sample'] for r in reps]), 1) if reps else None, T_note='sum of scenario walls of the sampled Intents (go-core-migration excluded)', go_core_migration=dict(scenarios=len(GOCORE), wall_s=round(sum(s['wall'] for s in GOCORE), 1), longest_s=round(max((s['wall'] for s in GOCORE), default=0), 1)))
if reps:
    r1 = reps[0]; v4['scenarios'] = len(r1['scen']); v4['intents'] = len({s['intent'] for s in r1['scen']})
    red = collections.defaultdict(int)
    for s in r1['scen']:
        if s['status'] != 'PASSED': red[s['intent']] += 1
    v4['red_intents'] = len(red); v4['red_scenarios'] = sum(red.values())
    per = {}
    for b in BUD:
        sets = []
        for r in reps:
            f = {s['intent'] for s in r['scen'] if s['wall'] > b}
            sets.append(f)
        green1 = {s['intent'] for s in r1['scen']} - set(red)
        per[b] = dict(flagged_per_repeat=[len(x) for x in sets], known_hazards_flagged=[sorted(HAZ & x) for x in sets], known_hazards_in_sample=sorted(HAZ & {s['intent'] for s in r1['scen']}),
                      false_refusals_any_repeat=len(set().union(*sets) - HAZ), false_refusals_all_repeats=len(set.intersection(*sets) - HAZ) if sets else 0,
                      false_refusals_green_only=len((set().union(*sets) & green1) - HAZ),
                      same_set_all_repeats=all(x == sets[0] for x in sets), fr_intents=sorted(set().union(*sets) - HAZ)[:60])
    v4['by_budget'] = per
    slow = sorted(r1['scen'], key=lambda s: -s['wall'])[:25]
    v4['slowest'] = [dict(intent=s['intent'], wall=round(s['wall'], 1), status=s['status'], name=s['name'][:70]) for s in slow]
    for h in HAZ:
        v4.setdefault('hazard_walls', {})[h] = [round(s['wall'], 1) for s in r1['scen'] if s['intent'] == h and s['wall'] > 5]
M['v4'] = v4
# ---- mutants ----
def hazname(n): return f'Lab hazard lab{n:02d}'
rows = []
for f in sorted(glob.glob(f'{RUNS}/mut*-serial.scen.json')):
    name = os.path.basename(f)[:-len('-serial.scen.json')]; n = int(name[3:5]); cls = name.split('-')[1]
    ser = L(name + '-serial'); a = L(name + '-v2-A'); b = L(name + '-v2-B'); pj = f'{RUNS}/{name}-v2.pair.json'
    hz = [s for s in ser['scen'] if s['name'].startswith(hazname(n))]
    row = dict(n=n, cls=cls, intent=hz[0]['intent'] if hz else None, valid=bool(hz) and all(s['status'] == 'PASSED' for s in hz),
               serial_hazard_wall=round(max((s['wall'] for s in hz), default=0), 1), serial_other_red=sum(1 for s in ser['scen'] if s['status'] != 'PASSED' and not s['name'].startswith(hazname(n))))
    row['v4_flag'] = {str(bv): row['serial_hazard_wall'] > bv for bv in BUD}
    row['v4_flag_other_scenarios'] = {str(bv): sum(1 for s in ser['scen'] if not s['name'].startswith(hazname(n)) and s['wall'] > bv) for bv in BUD}
    ref = {k: v['status'] for k, v in keyed(ser).items()}
    if a and b:
        det, other, wins = False, [], []
        for lab, r in (('A', a), ('B', b)):
            for k, s in keyed(r).items():
                if s['status'] != 'PASSED' and ref.get(k) == 'PASSED':
                    if s['name'].startswith(hazname(n)): det = True
                    else: other.append((lab, s['name'][:50]))
            for s in r['scen']:
                if s['name'].startswith(hazname(n)): wins.append((s['start'], s['end']))
        row['v2_detect'] = det; row['v2_other_new_failures'] = other[:5]; row['v2_n_other'] = len(other)
        if len(wins) >= 2:
            (s1, e1), (s2, e2) = wins[0], wins[-1]; row['overlap_s'] = round(max(0, min(e1, e2) - max(s1, s2)), 2)
        row['v2_pair_wall'] = round(json.load(open(pj))['pair_wall'], 1) if os.path.exists(pj) else None; row['serial_wall'] = round(ser['wall'], 1)
    text = open(f'{MUT}/{name}.js').read() + open(f'{MUT}/{name}.feature.add').read() if os.path.exists(f'{MUT}/{name}.js') else ''
    row['v1p_flag'] = bool(v1prime.scan_text(text))
    rows.append(row)
M['mutants'] = rows
_pw = [(r['v2_pair_wall'] - r['serial_wall']) / r['serial_wall'] for r in rows if r.get('v2_pair_wall') and r.get('serial_wall')]
M['v2_on_mutants'] = dict(n=len(_pw), added_wall_pct_median=round(100 * st.median(_pw), 1) if _pw else None, added_wall_pct_min=round(100 * min(_pw), 1) if _pw else None, added_wall_pct_max=round(100 * max(_pw), 1) if _pw else None,
                          other_new_failures_total=sum(r.get('v2_n_other', 0) for r in rows), mutants_run=len(rows), mutants_invalid=sum(not r['valid'] for r in rows))
agg = {}
for cls in ('port', 'path', 'shared', 'sleep'):
    rs = [r for r in rows if r['cls'] == cls]
    agg[cls] = dict(n=len(rs), valid=sum(r['valid'] for r in rs), v4_B10=sum(r['v4_flag']['10'] for r in rs), v4_B5=sum(r['v4_flag']['5'] for r in rs), v4_B20=sum(r['v4_flag']['20'] for r in rs), v4_B30=sum(r['v4_flag']['30'] for r in rs),
                    v2=sum(bool(r.get('v2_detect')) for r in rs), v2_with_overlap=sum(1 for r in rs if r.get('overlap_s', 0) > 0), v2_detect_given_overlap=sum(1 for r in rs if r.get('overlap_s', 0) > 0 and r.get('v2_detect')),
                    v1p=sum(r['v1p_flag'] for r in rs))
M['recall'] = agg
# ---- V2 slice stability + added wall ----
ss = L('slice-serial'); sl = dict(serial_wall=round(ss['wall'], 1) if ss else None)
if ss:
    ref = {k: v['status'] for k, v in keyed(ss).items()}; sets = []; walls = []; load_flags = collections.defaultdict(set)
    for p in sorted(glob.glob(f'{RUNS}/slice-v2-r*.pair.json')):
        base = os.path.basename(p)[:-len('.pair.json')]; a, b = L(base + '-A'), L(base + '-B')
        if not (a and b): continue
        bad = set()
        for lab, r in (('A', a), ('B', b)):
            for k, s in keyed(r).items():
                if s['status'] != 'PASSED' and ref.get(k) == 'PASSED': bad.add((s['intent'], s['name'][:60]))
            for s in r['scen']:
                for bv in BUD:
                    if s['wall'] > bv and s['intent'] not in HAZ: load_flags[bv].add(s['intent'])
        sets.append(bad); walls.append(json.load(open(p))['pair_wall'])
    sl.update(repeats=len(sets), refused_per_repeat=[len(x) for x in sets], stable=bool(sets) and all(x == sets[0] for x in sets), refused_union=sorted(set().union(*sets))[:20] if sets else [],
              pair_wall_median=round(st.median(walls), 1) if walls else None, pair_walls=[round(w, 1) for w in walls],
              added_wall_pct=round(100 * (st.median(walls) - ss['wall']) / ss['wall'], 1) if walls else None,
              v4_under_load_flagged_intents={str(bv): len(v) for bv, v in load_flags.items()},
              serial_red=sum(1 for v in ref.values() if v != 'PASSED'), serial_scen=len(ref))
M['slice'] = sl
fa, fb = L('full-v2-A'), L('full-v2-B'); pj = f'{RUNS}/full-v2.pair.json'
if fa and fb and reps:
    ref = {k: v['status'] for k, v in keyed(reps[0]).items()}; bad = set()
    for r in (fa, fb):
        for k, s in keyed(r).items():
            if s['status'] != 'PASSED' and ref.get(k) == 'PASSED': bad.add((s['intent'], s['name'][:60], s['err'][:100].replace('\n', ' ')))
    pw = json.load(open(pj))['pair_wall']
    M['full_v2'] = dict(pair_wall=round(pw, 1), serial_T_median=v4['T_median'], added_wall_pct=round(100 * (pw - v4['T_median']) / v4['T_median'], 1), new_failures=len(bad), new_failure_examples=sorted(bad)[:15],
                        v4_under_load={str(bv): len({s['intent'] for r in (fa, fb) for s in r['scen'] if s['wall'] > bv} - HAZ) for bv in BUD})
json.dump(M, open(sys.argv[3] if len(sys.argv) > 3 else 'metrics.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in M.items() if k != 'mutants'}, indent=1)[:9000])
