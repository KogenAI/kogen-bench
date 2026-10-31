#!/usr/bin/env python3
"""Build the timing tables from the published, anonymised data files.   Usage: python3 -I report.py DATADIR > tables.md   (DATADIR holds cells.jsonl.gz and reqs.jsonl.gz)"""
import json, sys, os, gzip, statistics as S, collections

out = sys.argv[1]
cells = [json.loads(l) for l in gzip.open(os.path.join(out, 'cells.jsonl.gz'), 'rt')]
reqs = [json.loads(l) for l in gzip.open(os.path.join(out, 'reqs.jsonl.gz'), 'rt')]
SINCE = os.environ.get('FPH_SINCE')  # e.g. 2026-10-29: keep cells started on/after (cells without a start time are kept)
if SINCE:
    cells = [c for c in cells if not c.get('started') or c['started'] >= SINCE]
    keep = {c['cell'] for c in cells}
    reqs = [r for r in reqs if r['cell'] in keep]

HC = {'mac-desktop': 'Mac desktop', 'laptop': 'laptop', 'linux-a': 'Linux host A', 'linux-b': 'Linux host B', 'macbook-delivery': 'MacBook delivery'}
HORDER = ['macbook-delivery', 'mac-desktop', 'laptop', 'linux-a', 'linux-b']


def pct(v, p):
    v = sorted(v)
    if not v:
        return None
    k = (len(v) - 1) * p
    f = int(k)
    c = min(f + 1, len(v) - 1)
    return v[f] + (v[c] - v[f]) * (k - f)


def f(x, d=0):
    return '-' if x is None else (f'{x:.{d}f}' if d else f'{x:.0f}')


def table(head, rows):
    o = ['| ' + ' | '.join(head) + ' |', '|' + '---|' * len(head)]
    for r in rows:
        o.append('| ' + ' | '.join(str(x) for x in r) + ' |')
    return '\n'.join(o)


# real builds: at least one build-role request; seeded/review-only separated
rq_by = collections.defaultdict(list)
for r in reqs:
    rq_by[r['cell']].append(r)


def is_real_build(c):
    L = c.get('log') or {}
    return c['phase'] == 'build' and not L.get('seeded') and (any(r['role'] == 'build' for r in rq_by[c['cell']]) or L.get('exec_rounds', 0) > 0)


BPH = ['startup', 'build', 'verifying', 'review', 'committing']
SPH = ['setup', 'preparation', 'model', 'probe', 'readiness', 'shape']


def decomp(sel, phases, key):
    """per host class: n, wall median/p90, per-phase median s/p90 and share of total wall (sum phase / sum wall)."""
    rows = []
    for h in HORDER:
        cs = [c for c in sel if c['host'] == h and c.get('wall_s') and c.get(key)]
        if not cs:
            continue
        walls = [c['wall_s'] for c in cs]
        tw = sum(walls)
        row = [HC[h], len(cs), f(S.median(walls)), f(pct(walls, .9))]
        acc = 0
        for p in phases:
            v = [c[key]['phases'].get(p, 0) for c in cs]
            acc += sum(v)
            row.append(f'{f(S.median(v))}/{f(pct(v, .9))} ({100*sum(v)/tw:.0f}%)')
        row.append(f'{100*(tw-acc)/tw:.0f}%')
        rows.append(row)
    return rows


print('## 1. Delivery-path timing decomposition\n')
print('Cells: Kogen build cells with a builder request ("real builds"), from run-log/log.jsonl `phase_duration` events. Each phase cell shows median/p90 seconds (share of summed wall). Last column = wall not inside any logged phase (process start, queue/setup outside Kogen, grading, gaps).\n')
real = [c for c in cells if is_real_build(c) and 'log' in c]
print('### 1a. Real builds (builder or executor ran; not seeded), all outcomes\n')
print(table(['host class', 'n', 'wall med s', 'wall p90 s'] + BPH + ['unlogged'], decomp(real, BPH, 'log')))
print('\n### 1b. Real builds, outcome = landed only\n')
print(table(['host class', 'n', 'wall med s', 'wall p90 s'] + BPH + ['unlogged'], decomp([c for c in real if c['outcome'] == 'landed'], BPH, 'log')))
print('\n### 1c. Seeded/review-only builds (no builder request; verification+review replay cells)\n')
seeded = [c for c in cells if c['phase'] == 'build' and 'log' in c and not is_real_build(c)]
print(table(['host class', 'n', 'wall med s', 'wall p90 s'] + BPH + ['unlogged'], decomp(seeded, BPH, 'log')))
print('\n### 1d. Shape cells\n')
shp = [c for c in cells if c['phase'] == 'shape' and 'shape_log' in c and c['shape_log']['phases']]
rows = []
for h in HORDER:
    cs = [c for c in shp if c['host'] == h and c['shape_log']['phases'].get('shape')]
    if not cs:
        continue
    env = [c['shape_log']['phases']['shape'] for c in cs]
    te = sum(env)
    row = [HC[h], len(cs), f(S.median(env)), f(pct(env, .9))]
    sub = ['setup', 'preparation', 'model', 'probe', 'readiness']
    acc = 0
    for p in sub:
        v = [c['shape_log']['phases'].get(p, 0) for c in cs]
        acc += sum(v)
        row.append(f'{f(S.median(v))}/{f(pct(v, .9))} ({100*sum(v)/te:.0f}%)')
    row.append(f'{100*(te-acc)/te:.0f}%')
    rows.append(row)
print(table(['host class', 'n', 'shape envelope med s', 'p90 s', 'setup', 'preparation', 'model', 'probe', 'readiness', 'other in envelope (tool loop / gaps)'], rows))
print('\nShape envelope = the `shape` phase_duration (whole shaping session); sub-phases are shares of the summed envelope. Sub-phases may overlap (probe/readiness run inside the model loop), so "other" is a lower bound.\n')

# result.json stage level (includes approve, uses all cells incl. no log)
print('### 1e. result.json stage walls (all Kogen build cells, any host; approve = exact approval/ setup stage)\n')
rows = []
for h in HORDER:
    cs = [c for c in cells if c['host'] == h and c['phase'] == 'build' and c.get('wall_s') and c['stages']]
    if not cs:
        continue
    tw = sum(c['wall_s'] for c in cs)
    row = [HC[h], len(cs), f(S.median([c['wall_s'] for c in cs])), f(pct([c['wall_s'] for c in cs], .9))]
    for st in ('approve', 'build', 'review'):
        v = [c['stages'].get(st, {}).get('wall_s', 0) for c in cs]
        row.append(f'{f(S.median(v))}/{f(pct(v, .9))} ({100*sum(v)/tw:.0f}%)')
    rows.append(row)
print(table(['host class', 'n', 'wall med', 'wall p90', 'approve', 'build (incl. verify)', 'review'], rows))

# outcomes
print('\n### 1f. Outcome mix by phase\n')
oc = collections.Counter((c['phase'], c['outcome']) for c in cells)
print(table(['phase', 'outcome', 'n'], [(a, b, n) for (a, b), n in sorted(oc.items(), key=lambda x: -x[1])]))

# ---- 2. triggers
print('\n## 2. Task -> trigger index\n')
TR = ['red_start', 'long_shell_300', 'review_repair', 'deadline', 'no_submit_refusal', 'large_review_150', 'repeat_verif', 'provider_stall']


def triggers(c):
    t = {}
    L = c.get('log')
    if L:
        if L['red_start']:
            t['red_start'] = 'baseline cmd red at start'
        if L['long_cmds']:
            t['long_shell_300'] = ','.join(f'{n}:{d}s' for n, d in L['long_cmds'][:3])
        if L['review_repair']:
            t['review_repair'] = f"{L['review_repair']}/{L['nreviews']} reviews with findings"
        if L['parts_max'] >= 100:
            t['large_review_150'] = f"{L['parts_max']} parts"
        if L['repeat_verif']:
            t['repeat_verif'] = f"{L['repeat_verif']} repeats w/o edit"
        slow = [r['wall_ms'] for r in rq_by[c['cell']] if (r.get('wall_ms') or 0) >= 180000]
        if slow or L['nprov'] > len([r for r in rq_by[c['cell']]]) + 0 and L['nprov'] - len(rq_by[c['cell']]) >= 2:
            t['provider_stall'] = (f'{len(slow)} req>=180s max {max(slow)/1000:.0f}s' if slow else f"{L['nprov']-len(rq_by[c['cell']])} extra attempts")
        if L['blockers']:
            t['no_submit_refusal'] = 'builder_blocker'
    oc = c['outcome'] or ''
    if oc in ('timeout',):
        t['deadline'] = f'outcome=timeout wall {c.get("wall_s") and round(c["wall_s"])}s'
    if oc in ('refused', 'invalid_response', 'questions_pending', 'no_progress', 'review_invalid') or (c.get('shape_log') or {}).get('sub_refused'):
        t['no_submit_refusal'] = oc or 'sub_refused'
    for r in rq_by[c['cell']]:
        if (r.get('wall_ms') or 0) >= 180000 and c['phase'] == 'shape':
            t['provider_stall'] = f"shape req {r['wall_ms']/1000:.0f}s"
    return t


cnt = collections.Counter()
by_task = collections.defaultdict(lambda: collections.defaultdict(list))
tot = collections.Counter()
index_rows = []
for c in cells:
    t = triggers(c)
    ph = c['phase']
    scope = ('real build' if is_real_build(c) else ph)
    tot[(c['host'], scope)] += 1
    for k in t:
        cnt[(scope, k)] += 1
    task = c['cell'].split('/')[2] if c['host'] != 'macbook-delivery' else c['cell'].split('/')[1]
    for k, v in t.items():
        by_task[k][task].append((c['cell'], v))
    if t:
        index_rows.append((c['cell'], scope, c['outcome'], t))

print('Trigger definitions: red_start = a `before_change` command (baseline/setup check) exits non-zero; long_shell_300 = a logged command (command->command_result) >300 s; review_repair = a review verdict event with non-empty findings; deadline = outcome `timeout`; no_submit_refusal = outcome refused/invalid_response/questions_pending/no_progress/review_invalid, shaping submission_refused, or builder_blocker; large_review_150 = review_source/material parts >=100 (NO log has >150; max observed 119, so strictly 0 cells); repeat_verif = same non-baseline verification command re-run with no write_file AND no builder shell call in between (strict lower bound; looser definition ignoring shell calls gives the `repeat_loose` count in 2d); provider_stall = a request with wall >=180 s, or >=2 provider attempts beyond requests.\n')
rows = []
for scope in ('real build', 'build', 'shape'):
    n = sum(v for (h, s), v in tot.items() if s == scope)
    row = [scope + ('' if scope != 'build' else ' (seeded/replay)'), n]
    for k in TR:
        row.append(cnt[(scope, k)])
    rows.append(row)
print(table(['cell class', 'n cells'] + TR, rows))
print('\n### 2b. Trigger incidence by host class (real builds + shape)\n')
rows = []
for h in HORDER:
    cs = [c for c in cells if c['host'] == h and (is_real_build(c) or c['phase'] == 'shape')]
    if not cs:
        continue
    row = [HC[h], len(cs)]
    ctr = collections.Counter()
    for c in cs:
        for k in triggers(c):
            ctr[k] += 1
    for k in TR:
        row.append(ctr[k])
    rows.append(row)
print(table(['host class', 'n'] + TR, rows))

print('\n### 2c. Task -> trigger index (tasks with each trigger; task = slug; counts are cells; up to 6 example cells each)\n')
for k in TR:
    d = by_task[k]
    print(f'**{k}** — {sum(len(v) for v in d.values())} cells across {len(d)} tasks')
    for task, lst in sorted(d.items(), key=lambda x: -len(x[1]))[:25]:
        ex = '; '.join(f'{cl} [{v}]' for cl, v in lst[:2])
        print(f'- `{task}` x{len(lst)}: {ex}')
    print()


# ---- 3. D/E growth attribution
print('\n## 3. D/E byte / history-growth attribution (per request)\n')
print('Source: `request` events (usage input/cached/output, wall_ms, role, build_round|review_round) and shaping `provider_call`; request_bytes exists only in newer builds.\n')
rr = collections.defaultdict(list)
for r in reqs:
    if r.get('inp') is None:
        continue
    rr[r['role']].append(r)
rows = []
for role in ('shape', 'build', 'review'):
    v = rr.get(role, [])
    if not v:
        continue
    inp = [r['inp'] + (r['cached'] or 0) if False else r['inp'] for r in v]
    cached = sum(r['cached'] or 0 for r in v)
    tin = sum(r['inp'] for r in v)
    out_ = sum(r['out'] or 0 for r in v)
    wall = sum((r['wall_ms'] or 0) for r in v) / 1000
    bytes_ = [r['bytes'] for r in v if r.get('bytes')]
    rows.append([role, len(v), f(S.median(inp)), f(pct(inp, .9)), f"{100*cached/max(tin,1):.0f}%", f"{tin/1e6:.1f}M", f"{out_/1e6:.2f}M", f(S.median([r['wall_ms'] or 0 for r in v]) / 1000, 1), f(pct([r['wall_ms'] or 0 for r in v], .9) / 1000, 1), f"{wall/3600:.1f}h", f(S.median(bytes_)) if bytes_ else '-'])
print(table(['role', 'requests', 'input tok med', 'p90', 'cached share (of input)', 'input total', 'output total', 'req wall med s', 'p90 s', 'summed req wall', 'req bytes med'], rows))
print('\n(`input` as logged is total prompt tokens; `cached` is the cached part of it.)\n')

# growth per round: per cell, per round, median input
print('### 3b. Prompt growth per round (builder and reviewer): median input tokens and cached share by round index\n')
rows = []
for role in ('build', 'review'):
    byr = collections.defaultdict(list)
    for r in rr.get(role, []):
        if r.get('round'):
            byr[min(r['round'], 12)].append(r)
    for k in sorted(byr):
        v = byr[k]
        c = sum(x['cached'] or 0 for x in v)
        t = sum(x['inp'] for x in v)
        rows.append([role, k if k < 12 else '12+', len(v), f(S.median([x['inp'] for x in v])), f"{100*c/max(t,1):.0f}%", f(S.median([x['out'] or 0 for x in v])), f(S.median([x['wall_ms'] or 0 for x in v]) / 1000, 1)])
print(table(['role', 'round', 'n', 'input tok med', 'cached share', 'output tok med', 'req wall med s'], rows))

# per-cell growth: first vs last request, growth per round
print('\n### 3c. Per-cell history growth (cells with >=4 builder requests)\n')
g = []
for cid, v in rq_by.items():
    b = sorted([r for r in v if r['role'] == 'build' and r.get('inp') and r.get('round')], key=lambda r: r['round'])
    if len(b) >= 4:
        g.append((cid, len(b), b[0]['inp'], b[-1]['inp'], (b[-1]['inp'] - b[0]['inp']) / (len(b) - 1), sum(x['inp'] for x in b), sum(x['cached'] or 0 for x in b)))
if g:
    print(f'n={len(g)} cells; first-request input median {f(S.median([x[2] for x in g]))}, last-request median {f(S.median([x[3] for x in g]))}; growth per round median {f(S.median([x[4] for x in g]))} tok (p90 {f(pct([x[4] for x in g], .9))}); builder rounds median {f(S.median([x[1] for x in g]))} p90 {f(pct([x[1] for x in g], .9))}.')
    print('\nTop 10 cells by total builder input tokens:\n')
    print(table(['cell', 'rounds', 'first in', 'last in', 'growth/round', 'total in', 'cached share'], [[x[0], x[1], x[2], x[3], f(x[4]), x[5], f"{100*x[6]/max(x[5],1):.0f}%"] for x in sorted(g, key=lambda x: -x[5])[:10]]))

# whole-corpus totals by role: tokens and request wall, share of cell wall
print('\n### 3d. Request wall vs cell wall (real builds): how much of wall is waiting on provider responses, by role\n')
rows = []
for h in HORDER:
    cs = [c for c in real if c['host'] == h and c.get('wall_s')]
    if not cs:
        continue
    tw = sum(c['wall_s'] for c in cs)
    row = [HC[h], len(cs)]
    for role in ('build', 'review'):
        w = sum((r['wall_ms'] or 0) for c in cs for r in rq_by[c['cell']] if r['role'] == role) / 1000
        row.append(f'{100*w/tw:.0f}%')
    cmdw = sum(c['log']['verif_cmd_s'] for c in cs)
    setw = sum(c['log']['setup_cmd_s'] for c in cs)
    row += [f'{100*cmdw/tw:.0f}%', f'{100*setw/tw:.0f}%']
    rows.append(row)
print(table(['host class', 'n', 'builder request wall / cell wall', 'review request wall / cell wall', 'verification commands / wall', 'setup commands / wall'], rows))

# ---- 2d repeats
print('\n### 2d. Repeated verification of an unchanged tree (real builds; strict = no write_file and no builder shell call between two runs of the same non-baseline gate command)\n')
rows = []
for h in HORDER:
    cs = [c for c in real if c['host'] == h and c.get('wall_s')]
    if not cs:
        continue
    tw = sum(c['wall_s'] for c in cs)
    rs = sum(c['log'].get('repeat_s', 0) for c in cs)
    n1 = sum(1 for c in cs if c['log'].get('repeat_s', 0) > 0)
    rows.append([HC[h], len(cs), n1, sum(c['log'].get('repeat_verif', 0) for c in cs), sum(c['log'].get('repeat_loose', 0) for c in cs), f(rs / 3600, 1), f'{100*rs/tw:.1f}%'])
print(table(['host class', 'n', 'cells with strict repeat', 'strict repeat runs', 'loose repeat runs (ignoring shell calls)', 'strict repeat time h', 'share of wall'], rows))

# ---- 3e tool-output attribution
print('\n### 3e. Top contributors to history bytes: tool result bytes by role/tool (real builds, all hosts with logs)\n')
agg = collections.defaultdict(lambda: [0, 0, 0])
cellsn = 0
for c in real:
    tb = c['log'].get('tool_bytes') or {}
    if tb:
        cellsn += 1
    for k, v in tb.items():
        a = agg[k]
        a[0] += v[0]; a[1] += v[1]; a[2] += v[2]
tot = sum(v[1] for v in agg.values()) or 1
rows = []
for k, v in sorted(agg.items(), key=lambda x: -x[1][1]):
    rows.append([k, v[0], f'{v[1]/1e6:.1f} MB', f'{100*v[1]/tot:.0f}%', f(v[1] / max(v[0], 1)), f'{v[2]/1e6:.2f} MB'])
print(f'{cellsn} real-build cells with tool events.\n')
print(table(['role:tool', 'calls', 'result bytes', 'share', 'mean bytes/call', 'argument bytes'], rows))
cagg = collections.defaultdict(lambda: [0, 0])
for c in real:
    for k, v in (c['log'].get('cmd_out') or {}).items():
        cagg[k][0] += v[0]; cagg[k][1] += v[1]
print('\nVerification/setup command output bytes (Kogen-run gates; fed back to builder on red):\n')
ct = sum(v[1] for v in cagg.values()) or 1
print(table(['command class', 'runs', 'output bytes', 'share', 'mean bytes/run'], [[k, v[0], f'{v[1]/1e6:.1f} MB', f'{100*v[1]/ct:.0f}%', f(v[1] / max(v[0], 1))] for k, v in sorted(cagg.items(), key=lambda x: -x[1][1])[:10]]))

# ---- 3f provider latency/gap
print('\n### 3f. Provider liveness: slow requests by role and host (all request events)\n')
rows = []
for role in ('shape', 'build', 'review'):
    for h in HORDER:
        v = [r for r in reqs if r['role'] == role and r['host'] == h and r.get('wall_ms')]
        if not v:
            continue
        w = [r['wall_ms'] / 1000 for r in v]
        slow = [x for x in w if x >= 180]
        vslow = [x for x in w if x >= 300]
        errs = sum(1 for r in v if r.get('err'))
        rows.append([role, HC[h], len(v), f(S.median(w), 1), f(pct(w, .9), 1), f(pct(w, .99), 1), len(slow), len(vslow), f'{100*sum(slow)/sum(w):.0f}%', errs])
print(table(['role', 'host', 'requests', 'wall med s', 'p90', 'p99', '>=180 s', '>=300 s', 'share of request wall in >=180 s requests', 'errored'], rows))

# ---- 4 headroom numbers
print('\n## 4. Headroom arithmetic (inputs to the ranked list)\n')
rb = [c for c in real if c.get('wall_s')]
tw = sum(c['wall_s'] for c in rb)
nl = [c for c in rb if c['outcome'] != 'landed']
print(f'- Real builds: n={len(rb)}, summed wall {tw/3600:.1f} h. Non-landed: n={len(nl)} ({100*len(nl)/len(rb):.0f}% of cells) holding {100*sum(c["wall_s"] for c in nl)/tw:.0f}% of wall; timeouts alone {sum(1 for c in nl if c["outcome"]=="timeout")} cells / {sum(c["wall_s"] for c in nl if c["outcome"]=="timeout")/3600:.1f} h.')
sh = [c for c in cells if c['phase'] == 'shape' and c.get('wall_s')]
tws = sum(c['wall_s'] for c in sh)
bad = [c for c in sh if c['outcome'] != 'ok']
print(f'- Shape cells: n={len(sh)}, summed wall {tws/3600:.1f} h. outcome != ok: n={len(bad)} holding {100*sum(c["wall_s"] for c in bad)/tws:.0f}% of wall; refused {sum(1 for c in sh if c["outcome"]=="refused")}, questions_pending {sum(1 for c in sh if c["outcome"]=="questions_pending")}, timeout {sum(1 for c in sh if c["outcome"]=="timeout")}.')
rv = [c for c in rb if c['log']['phases'].get('review') is not None]
rep = [c for c in rv if c['log']['review_repair']]
nrep = [c for c in rv if not c['log']['review_repair']]
if rep and nrep:
    mr = S.median([c['log']['phases'].get('review', 0) for c in nrep])
    ex = sum(max(0, c['log']['phases'].get('review', 0) - mr) for c in rep)
    tr = sum(c['log']['phases'].get('review', 0) for c in rv)
    print(f'- Review: {len(rep)}/{len(rv)} real builds have a findings round; review phase total {tr/3600:.1f} h = {100*tr/sum(c["wall_s"] for c in rv):.0f}% of their wall; excess review time of finding-cells over the clean-cell median ({mr:.0f} s) = {ex/3600:.1f} h ({100*ex/sum(c["wall_s"] for c in rv):.1f}% of wall).')
    print(f'  Wall median with findings {S.median([c["wall_s"] for c in rep]):.0f} s vs clean {S.median([c["wall_s"] for c in nrep]):.0f} s.')
lc = [(n, d) for c in rb for n, d in c['log']['long_cmds']]
print(f'- Long shell (>300 s logged gate/setup command): {len(lc)} commands in {sum(1 for c in rb if c["log"]["long_cmds"])} cells; total {sum(d for n,d in lc)/3600:.1f} h, of which beyond 300 s {sum(d-300 for n,d in lc)/3600:.1f} h; by class: ' + ', '.join(f'{k} {v/3600:.1f}h' for k, v in sorted(collections.Counter({k: sum(d for n, d in lc if n.split("-")[0] == k) for k in {n.split("-")[0] for n, d in lc}}).items(), key=lambda x: -x[1])))
st = sum(c['log']['phases'].get('startup', 0) for c in rb)
print(f'- Startup (setup + baseline gates before the first builder turn): {st/3600:.1f} h = {100*st/tw:.0f}% of real-build wall (MacBook delivery median {S.median([c["log"]["phases"].get("startup",0) for c in rb if c["host"]=="macbook-delivery"] or [0]):.0f} s).')
vf = sum(c['log']['phases'].get('verifying', 0) for c in rb)
print(f'- Verification phase: {vf/3600:.1f} h = {100*vf/tw:.0f}% of wall; strict-repeat part {sum(c["log"].get("repeat_s",0) for c in rb)/3600:.1f} h.')
bt = collections.defaultdict(lambda: [0, 0, 0])
for r in reqs:
    if r.get('inp') is None:
        continue
    a = bt[r['role']]
    a[0] += r['inp']; a[1] += (r['cached'] or 0); a[2] += (r['out'] or 0)
print('- Token totals by role (input incl. cached / cached / output): ' + '; '.join(f'{k}: {v[0]/1e6:.0f}M / {v[1]/1e6:.0f}M ({100*v[1]/max(v[0],1):.0f}% cached) / {v[2]/1e6:.1f}M' for k, v in bt.items()))

# ---- 5. per-build delivery table (MacBook delivery runs; anonymised build numbers)
print('\n## 5. Delivery native builds (MacBook; seconds)\n')
rows = []
for i, c in enumerate([c for c in cells if c['host'] == 'macbook-delivery' and c.get('log')], 1):
    L = c['log']; P = L['phases']
    lc = ', '.join(f'{n} {d}' for n, d in L['long_cmds'][:2])
    rows.append([f'build {i}', f(c['wall_s']), f(P.get('startup', 0)), f(P.get('build', 0)), f(P.get('verifying', 0)), f(P.get('review', 0)), c['outcome'] or '(none logged)', L['exec_rounds'], lc or '-', f(L.get('repeat_s', 0))])
print(table(['build', 'wall', 'startup', 'builder/exec', 'verifying', 'review', 'outcome', 'executor rounds', 'longest gate commands (s)', 'strict repeat s'], rows))
