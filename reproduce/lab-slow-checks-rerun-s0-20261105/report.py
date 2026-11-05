#!/usr/bin/env python3
"""Stage 0 replay report: python3 -I report.py data/builds.json [results.json]. Model-free; reads only the dataset."""
import collections, json, random, statistics as S, sys
D = json.load(open(sys.argv[1]))
OUT = sys.argv[2] if len(sys.argv) > 2 else None
HEAVY = 180.0
res = {}
def chk(c): return dict(name=c[0], klass=c[1], cmd=c[2], secs=c[3], red=bool(c[4]))
RAW = [b for b in D if b['group'] == 'delivery' and b['raw_logs']]
DEL = [b for b in D if b['group'] == 'delivery']
CELL = [b for b in D if b['group'] == 'cell']
res['coverage'] = dict(
    stored_builds=len(D), delivery_builds=len(DEL), delivery_raw_logs=len(RAW), delivery_profile_rows_only=len(DEL) - len(RAW), climb_cell_logs=len(CELL),
    delivery_with_verify_pass=sum(1 for b in DEL if b['passes']), delivery_with_2plus_passes=sum(1 for b in DEL if len(b['passes']) >= 2),
    raw_with_tree_digest=sum(1 for b in RAW if any(p['tree'] for p in b['passes'])), identity_events_in_any_log=sum(b['identity_events'] for b in D),
    by_source=dict(collections.Counter(b['source'] for b in D)),
    date_range=[min(b['t0'] for b in D), max(b['t0'] for b in D)])
res['climb_cells_max_check_secs'] = max((c[3] for b in CELL for p in b['passes'] for c in p['checks']), default=0)

# ---- tree labels (strict): review digest; else inherit when no builder event and no fix command lay between two passes
def trees(b):
    lab = []
    for i, p in enumerate(b['passes']):
        t = p['tree']
        if t is None and i > 0 and b['passes'][i - 1]['gap'] and b['passes'][i - 1]['gap']['builder_events'] == 0 and b['passes'][i - 1]['gap']['fix_cmds'] == 0:
            t = lab[i - 1]
        lab.append(t or 'unk-%d' % i)
    return lab

# ---- U0: exact reuse inside one Build
def u0(b, thr):
    lab = trees(b); seen = set(); n = collections.Counter(); saved = 0.0; hits = 0; rx = 0; rxs = 0.0; flips = 0
    for i, p in enumerate(b['passes']):
        for c in map(chk, p['checks']):
            key = (lab[i], c['cmd'])
            if c['secs'] >= thr and key in seen:
                n[key] += 1
                if n[key] % 3 == 0: rx += 1; rxs += c['secs']
                else:
                    saved += c['secs']; hits += 1
                    if c['red']: flips += 1
            if not c['red']: seen.add(key)
    return saved, hits, rx, rxs, flips
spans = [b['span'] for b in RAW]; med = S.median(spans)
res['U0'] = {}
for thr in (60, 120, 300):
    t = [u0(b, thr) for b in RAW]
    tot = sum(x[0] for x in t)
    res['U0'][str(thr)] = dict(builds=len(RAW), builds_with_hit=sum(1 for x in t if x[1]), hits=sum(x[1] for x in t), seconds_saved=round(tot),
                               pct_of_total_wall=round(100 * tot / sum(spans), 2), per_build_s=round(tot / len(RAW), 1),
                               mean_saving_as_pct_of_median_wall=round(100 * tot / len(RAW) / med, 2), median_build_wall_s=round(med),
                               median_per_build_saving_s=S.median([x[0] for x in t]), every3rd_reexecutions=sum(x[2] for x in t),
                               reuse_where_stored_rerun_was_red=sum(x[4] for x in t))
random.seed(7); vals = [(u0(b, 60)[0], b['span']) for b in RAW]; bs = []
for _ in range(2000):
    s = [random.choice(vals) for _ in vals]
    bs.append(100 * (sum(x[0] for x in s) / len(s)) / S.median([x[1] for x in s]))
bs.sort(); res['U0']['bootstrap_mean_over_median_pct_60s'] = [round(bs[50], 2), round(bs[1000], 2), round(bs[1950], 2)]
# where did the exact-tree repeats come from?
kinds = collections.Counter(); pairs = 0
for b in RAW:
    lab = trees(b)
    for i in range(1, len(lab)):
        if lab[i] == lab[i - 1] and not lab[i].startswith('unk'):
            pairs += 1; kinds['prev pass reviewed approve' if b['passes'][i - 1]['verdict'] == 'approve' else 'other'] += 1
res['U0']['identical_tree_consecutive_passes'] = dict(total=pairs, **kinds)

# ---- U1: green baseline check reused across restarted Builds (surrogate key: slug + start head + command)
def u1(thr):
    green = set(); n = collections.Counter(); saved = collections.defaultdict(float); rx = 0; rxs = 0.0
    for b in sorted(DEL, key=lambda x: x['t0']):
        if not b['start_head']: continue
        mine = []
        for c in map(chk, b['baseline']):
            key = (b['slug'], b['start_head'], c['cmd'])
            if key in green and c['secs'] >= thr:
                n[key] += 1
                if n[key] % 3 == 0: rx += 1; rxs += c['secs']
                else: saved[b['id']] += c['secs']
            if not c['red']: mine.append(key)
        green.update(mine)
    return saved, rx, rxs
sp = [b['span'] for b in DEL]; medd = S.median(sp)
res['U1'] = {}
for thr in (60, 120, 300):
    sv, rx, rxs = u1(thr); tot = sum(sv.values())
    res['U1'][str(thr)] = dict(builds=len(DEL), builds_with_hit=len(sv), seconds_saved=round(tot), pct_of_total_wall=round(100 * tot / sum(sp), 2),
                               per_build_s=round(tot / len(DEL), 1), mean_saving_as_pct_of_median_wall=round(100 * tot / len(DEL) / medd, 2),
                               median_build_wall_s=round(medd), every3rd_reexecutions=rx)
res['U2'] = dict(status='not measurable', reason='no stored log carries a run-identity event', identity_events=res['coverage']['identity_events_in_any_log'])

# ---- k-round-full-suite: where do slow checks (>=180 s) run in verify passes?
def heavy_class(b):
    k = collections.Counter()
    for p in b['passes']:
        for c in map(chk, p['checks']):
            if c['secs'] >= HEAVY: k[c['klass']] += c['secs']
    for c in map(chk, b['baseline']):
        if c['secs'] >= HEAVY: k[c['klass']] += c['secs']
    return max(k, key=k.get) if k else None
cat = collections.defaultdict(collections.Counter); catn = collections.defaultdict(collections.Counter); per = []
for b in DEL:
    g = heavy_class(b); grp = g if g in ('elixir', 'go') else ('node/other' if g else 'no heavy check')
    lab = trees(b) if b['raw_logs'] else None; seen = set(); n = len(b['passes'])
    base = sum(c[3] for c in b['baseline'] if c[3] >= HEAVY); pool = 0.0; ver = 0.0; led = 0.0; red_used = red_n = 0
    for i, p in enumerate(b['passes']):
        for c in map(chk, p['checks']):
            key = (lab[i], c['cmd']) if lab else None
            removed = bool(key and key in seen)
            if key and not c['red']: seen.add(key)
            ver += c['secs']
            if c['secs'] < HEAVY: continue
            if removed: kind = 'ledger-removed (shipped 3 Nov)'; led += c['secs']
            elif i == n - 1: kind = 'final pass, red' if c['red'] else 'final pass, green (kept)'
            elif c['red']:
                kind = 'non-final red (repair signal)'; pool += c['secs']; red_n += 1
                g_ = p['gap']; red_used += bool(g_ and (g_['write_events'] > 0 or g_['fix_cmds'] > 0))
            else: kind = 'non-final green, tree changed later'; pool += c['secs']
            cat[grp][kind] += c['secs']; catn[grp][kind] += 1
    cat[grp]['_wall'] += b['span']; cat[grp]['_builds'] += 1; cat[grp]['_baseline_heavy'] += base
    per.append(dict(id=b['id'], grp=grp, span=b['span'], npass=n, pool=pool, ver=ver, led=led, red_used=red_used, red_n=red_n, outcome=b['outcome']))
res['k_round'] = {}
for g in ('elixir', 'go', 'node/other', 'no heavy check'):
    bs_ = [x for x in per if x['grp'] == g]
    r_ = dict(builds=cat[g]['_builds'], wall_h=round(cat[g]['_wall'] / 3600, 1), baseline_heavy_s=round(cat[g]['_baseline_heavy']))
    for kind in ('final pass, green (kept)', 'final pass, red', 'ledger-removed (shipped 3 Nov)', 'non-final red (repair signal)', 'non-final green, tree changed later'):
        r_[kind] = dict(executions=catn[g][kind], seconds=round(cat[g][kind]), pct_of_wall=round(100 * cat[g][kind] / cat[g]['_wall'], 1) if cat[g]['_wall'] else 0)
    pool = sum(x['pool'] for x in bs_); wall = sum(x['span'] for x in bs_)
    r_['A2_pool_s'] = round(pool); r_['A2_pool_pct_of_wall'] = round(100 * pool / wall, 1) if wall else 0
    r_['builds_with_pool_ge_15pct_of_own_wall'] = sum(1 for x in bs_ if x['span'] and x['pool'] / x['span'] >= .15)
    r_['builds_with_pool'] = sum(1 for x in bs_ if x['pool'] > 0)
    r_['red_nonfinal_heavy_executions'] = sum(x['red_n'] for x in bs_); r_['of_which_followed_by_builder_write_or_fix'] = sum(x['red_used'] for x in bs_)
    m2 = [x for x in bs_ if x['npass'] >= 2]
    r_['builds_2plus_passes'] = len(m2)
    for f in (0.1, 0.3, 0.5):
        rat = [x['pool'] * (1 - f) / max(x['ver'] - x['led'], 1) for x in m2]; sec = [x['pool'] * (1 - f) for x in m2]
        r_['A2_f%.1f' % f] = dict(saved_s=round(sum(x['pool'] for x in bs_) * (1 - f)), pct_of_wall=round(100 * pool * (1 - f) / wall, 1) if wall else 0,
                                  median_verify_wall_saving_pct=round(100 * S.median(rat), 0) if rat else None, median_saved_s=round(S.median(sec)) if sec else None,
                                  builds_ge_25pct_and_180s=sum(1 for a, s in zip(rat, sec) if a >= .25 and s >= 180))
    res['k_round'][g] = r_
# A3 / A1 as operationally definable: a red pass whose failing check is cheap (<60 s) and that ran a >=60 s check first
cheap_after_heavy = cheap_fail = heavy_fail = 0
for b in DEL:
    for p in b['passes']:
        if p['green']: continue
        cs = [chk(c) for c in p['checks']]; fl = [c for c in cs if c['red']]
        if not fl: continue
        f = fl[0]
        if f['secs'] < 60:
            cheap_fail += 1
            if any(c['secs'] >= 60 and not c['red'] for c in cs[:cs.index(f)]): cheap_after_heavy += 1
        else: heavy_fail += 1
res['A3_fail_fast_order'] = dict(red_passes_failing_on_cheap_check=cheap_fail, red_passes_failing_on_slow_check=heavy_fail, cheap_failures_that_followed_a_slow_check=cheap_after_heavy)
# literal Lab gate: slow-check time >=15% of Build wall in >=10 non-Go Builds
el = [x for x in per if x['grp'] == 'elixir']
gate = 0
for b in DEL:
    if heavy_class(b) == 'elixir':
        h_ = sum(c[3] for p in b['passes'] for c in p['checks'] if c[3] >= HEAVY) + sum(c[3] for c in b['baseline'] if c[3] >= HEAVY)
        gate += (h_ / b['span'] >= .15) if b['span'] else 0
res['gate_literal_non_go_elixir_builds_with_slow_check_ge_15pct_of_wall'] = gate
txt = json.dumps(res, indent=1)
print(txt)
if OUT: open(OUT, 'w').write(txt + '\n')
