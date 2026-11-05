#!/usr/bin/env python3
"""orch.py <stage>: Lab k-verify-tests-isolated-parallel-safe Stage 1 driver (EU, user lanes, no model).
Stages: v4 (serial full-suite repeats), plan (derive mutants + slice from repeat 1), mut (40 mutants: serial + V2 pair),
slice (V2 stability slice: 1 serial + 10 pairs), full (1 full-suite V2 pair). Idempotent: a finished run (its .scen.json) is skipped.
Before every run it waits until no foreign suite runs on the host (guard); the waits are logged."""
import os, sys, json, time, subprocess, random, re, shutil
W = os.environ['LABW']; sys.path.insert(0, W + '/bin')
import msg
R = W + '/runs'; os.makedirs(R, exist_ok=True)
LOG = open(W + '/orch.log', 'a', buffering=1)
def log(*a): print(time.strftime('%H:%M:%SZ', time.gmtime()), *a, file=LOG)
HAZ = {'k-repin-adapt-f2e30a4', 'deterministic-check-gate'}
COPIES = {'A': W + '/copyA', 'B': W + '/copyB'}
INTENTS = lambda c: c + '/.kogen/intents'

def foreign():
    out = []
    me = os.getpid()
    for pid in os.listdir('/proc'):
        if not pid.isdigit() or int(pid) == me: continue
        try:
            comm = open(f'/proc/{pid}/comm').read().strip()
            if not (comm in ('go', 'node', 'beam.smp', 'cucumber-js') or comm.endswith('.test')): continue  # r4: idle kogen model-waiters of delivery Builds no longer block; compute processes do
            cwd = os.readlink(f'/proc/{pid}/cwd'); cmd = open(f'/proc/{pid}/cmdline').read().replace('\0', ' ')
            if 'lab-s1-verify' in cwd or 'lab-s1-verify' in cmd: continue
            out.append(f'{pid}:{comm}')
        except Exception: pass
    return out
def cpu_busy(sec=6):
    def rd():
        v = list(map(int, open('/proc/stat').readline().split()[1:9])); return sum(v) - v[3] - v[4], sum(v)  # busy (excl idle, iowait), total
    b0, t0 = rd(); time.sleep(sec); b1, t1 = rd(); return (b1 - b0) / max(1, t1 - t0)
def guard():
    """r5: wait until the host is quiet by measurement: CPU busy < 35% over 6 s on two consecutive looks and load1 < 2.0 (idle go/kogen.test shells of delivery Builds do not block)."""
    t = time.time(); waited = 0; ok = 0
    while True:
        la = float(open('/proc/loadavg').read().split()[0]); u = cpu_busy()
        if u < 0.35: ok += 1
        else: ok = 0
        if ok >= 2: break
        if not waited: log('GUARD busy cpu=%.2f load1=%.2f' % (u, la), foreign()[:4])
        waited = 1; time.sleep(4)
        if time.time() - t > 5400: log('GUARD gave up after 90 min'); sys.exit(3)
    if waited: log(f'GUARD free after {time.time()-t:.0f}s')
    return time.time() - t

def start(copy, feat, name, order, extra='', kenv=''):
    rep = f'{R}/{name}.ndjson'
    env = dict(os.environ, KENV=kenv)
    cmd = ['bash', W + '/bin/runsuite.sh', copy, feat, rep, order, f'{R}/tmp-{name}'] + ([extra] if extra else [])
    return subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE, text=True, start_new_session=True), rep
def finish(p, rep, name, extra_meta=None):
    out = p.communicate()[0].strip().splitlines()[-1]
    m = re.match(r'WALL ([\d.]+) RC (\d+)', out); wall, rc = float(m.group(1)), int(m.group(2))
    sc = msg.load(rep)
    json.dump(dict(name=name, wall=wall, rc=rc, scen=sc, **(extra_meta or {})), open(f'{R}/{name}.scen.json', 'w'))
    for suffix in ('', '.stdout'):  # keep only the parsed result; the raw report is large
        pass
    try: os.remove(rep)
    except OSError: pass
    shutil.rmtree(f'{R}/tmp-{name}', ignore_errors=True)
    log(f'DONE {name} wall={wall:.1f}s rc={rc} scen={len(sc)} fail={sum(1 for s in sc if s["status"]!="PASSED")}')
    return wall, rc, sc
def done(name): return os.path.exists(f'{R}/{name}.scen.json')
def get(name): return json.load(open(f'{R}/{name}.scen.json'))
def run1(name, copy, feat, order='defined', extra='', kenv=''):
    if done(name): return get(name)
    guard(); log('RUN', name); p, rep = start(copy, feat, name, order, extra, kenv); finish(p, rep, name); return get(name)
def run2(name, feat, seeds, extra='', kenv='', metas=None, g=True):
    """V2 pair: both copies concurrently, one guard check for the pair."""
    if done(name + '-A') and done(name + '-B'): return
    if g: guard()
    log('RUN', name, 'pair', seeds)
    t0 = time.time()
    pa, ra = start(COPIES['A'], feat, name + '-A', f'random:{seeds[0]}', extra, kenv)
    pb, rb = start(COPIES['B'], feat, name + '-B', f'random:{seeds[1]}', extra, kenv)
    finish(pa, ra, name + '-A'); finish(pb, rb, name + '-B')
    json.dump(dict(pair_wall=time.time() - t0), open(f'{R}/{name}.pair.json', 'w')); log(f'PAIR {name} wall={time.time()-t0:.1f}s')

def salvage(stop_epoch, start_epoch):
    """v4-r1 was stopped before the end: build v4-r1.scen.json from the partial report. Only Intents whose every pickle finished are kept."""
    rep = f'{R}/v4-r1.ndjson'; sc = msg.load(rep); exp = {}; fin = {}
    pk = {}
    for line in open(rep, errors='replace'):
        try: m = json.loads(line)
        except Exception: continue
        if 'pickle' in m: exp[m['pickle']['uri']] = exp.get(m['pickle']['uri'], 0) + 1
    for x in sc: fin[x['uri']] = fin.get(x['uri'], 0) + 1
    complete = {u for u in exp if fin.get(u, 0) >= exp[u]}
    keep = [x for x in sc if x['uri'] in complete]
    json.dump(dict(name='v4-r1', wall=stop_epoch - start_epoch, rc=-15, partial=True, intents_total=len(exp), intents_complete=len(complete), scen_finished=len(sc), scen_kept=len(keep), scen=keep), open(f'{R}/v4-r1.scen.json', 'w'))
    log('SALVAGE v4-r1', dict(intents_total=len(exp), intents_complete=len(complete), scen_finished=len(sc), scen_kept=len(keep)))
def merge_r1():
    a = get('v4-r1'); b = get('v4-r1b'); ex = {'go-core-migration'}
    sc = [x for x in a['scen'] if x['intent'] not in ex] + b['scen']
    m = dict(name='v4-merged', wall=(a['wall'] - sum(x['wall'] for x in a['scen'] if x['intent'] in ex) - 0) * 0 + b['wall'], rc=b['rc'], partial=False,
             seg_a_wall_excl_gocore=None, scen=sc)
    # readiness time T = wall of the segment run b plus the part of segment a that was spent on the kept Intents (sum of their scenario walls)
    m['T_seg_b'] = b['wall']; m['T_seg_a_kept_scen_sum'] = sum(x['wall'] for x in a['scen'] if x['intent'] not in ex)
    m['wall'] = b['wall'] + m['T_seg_a_kept_scen_sum']
    json.dump(m, open(f'{R}/v4-merged.scen.json', 'w')); log('MERGED', len(sc), 'scenarios', len({x["intent"] for x in sc}), 'intents T~%.0fs' % m['wall']); return m
def per_intent(sc):
    d = {}
    for s in sc['scen']: x = d.setdefault(s['intent'], dict(wall=0, n=0, bad=0, max=0)); x['wall'] += s['wall']; x['n'] += 1; x['bad'] += s['status'] != 'PASSED'; x['max'] = max(x['max'], s['wall'])
    return d

# ---------- mutants ----------
def feat_path(c, i): return f'{INTENTS(c)}/{i}/acceptance.feature'
def mutant_files(cls, k, n):
    """returns (appended feature text, step-file js). k = mutant index within its class (0..9), n = global id"""
    nm = f'lab{n:02d}'
    hdr = "const { When, Then } = require('@cucumber/cucumber');\nconst net = require('node:net'); const fs = require('node:fs');\nconst sleep = ms => new Promise(r => setTimeout(r, ms));\n"
    if cls == 'port':
        port = 47100 + k
        feat = f"\n  Scenario: Lab hazard {nm} fixed port\n    When the lab hazard {nm} service serves on its fixed port\n"
        js = hdr + f"When('the lab hazard {nm} service serves on its fixed port', {{ timeout: 120000 }}, async function () {{\n  const srv = net.createServer(); await new Promise((res, rej) => {{ srv.once('error', rej); srv.listen({port}, 'localhost', res); }});\n  await sleep(2000); await new Promise(r => srv.close(r));\n}});\n"
    elif cls == 'path':
        p = f'/tmp/lab-s1-fixed-{k}'
        feat = f"\n  Scenario: Lab hazard {nm} fixed path\n    When the lab hazard {nm} step uses its fixed directory\n"
        js = hdr + f"When('the lab hazard {nm} step uses its fixed directory', {{ timeout: 120000 }}, async function () {{\n  fs.mkdirSync('{p}');\n  try {{ await sleep(2000); }} finally {{ fs.rmSync('{p}', {{ recursive: true, force: true }}); }}\n}});\n"
    elif cls == 'shared':
        feat = (f"\n  Scenario: Lab hazard {nm} shared state set\n    When the lab hazard {nm} fixture is prepared\n"
                f"\n  Scenario: Lab hazard {nm} shared state use one\n    Then the lab hazard {nm} fixture is ready\n"
                f"\n  Scenario: Lab hazard {nm} shared state use two\n    Then the lab hazard {nm} fixture is ready\n")
        js = hdr + f"let prepared_{nm} = false;\nWhen('the lab hazard {nm} fixture is prepared', function () {{ prepared_{nm} = true; }});\nThen('the lab hazard {nm} fixture is ready', function () {{ if (!prepared_{nm}) throw new Error('fixture not prepared: depends on scenario order'); }});\n"
    else:
        sec = [11, 12, 13, 15, 18, 20, 25, 30, 40, 45][k]
        feat = f"\n  Scenario: Lab hazard {nm} fixed wait\n    When the lab hazard {nm} step waits {sec} seconds\n"
        js = hdr + f"When('the lab hazard {nm} step waits {sec} seconds', {{ timeout: 180000 }}, async function () {{ await sleep({sec * 1000}); }});\n"
    return feat, js
CLASSES = ['port', 'path', 'shared', 'sleep']
def plan():
    r1 = get('v4-merged') if done('v4-merged') else get('v4-r1'); pi = per_intent({'scen': [x for x in r1['scen'] if x['intent'] != 'go-core-migration']})
    green = sorted(i for i, x in pi.items() if x['bad'] == 0)
    elig = sorted(i for i in green if pi[i]['wall'] <= 40 and i not in HAZ)
    pool = sorted(i for i in green if pi[i]['wall'] <= 60)
    rng = random.Random(20261105)
    if len(elig) >= 40: mut = rng.sample(elig, 40)
    else:  # r4: fewer than 40 distinct green fast Intents exist (most Intents are red on main): hosts are drawn per class, reused across classes
        mut = []
        for c in range(4): mut += rng.sample(elig, 10) if len(elig) >= 10 else rng.choices(elig, k=10)
    sl = random.Random(20261105).sample(pool, min(10, len(pool)))
    plan = dict(intents=len(pi), green=len(green), eligible=len(elig), slice_pool=len(pool), T=r1['wall'],
                mutants=[dict(n=n, cls=CLASSES[n // 10], k=n % 10, intent=i) for n, i in enumerate(mut)], slice=sl)
    json.dump(plan, open(W + '/plan.json', 'w'), indent=1); log('PLAN', {k: v for k, v in plan.items() if k not in ('mutants', 'slice')}); return plan
def stage_mut(pl):
    os.makedirs(W + '/mutants', exist_ok=True)
    for m in sorted(pl['mutants'], key=lambda m: (m['k'], m['n'])):  # r5: interleave classes so a time stop leaves every class covered
        n, cls, k, intent = m['n'], m['cls'], m['k'], m['intent']; name = f'mut{n:02d}-{cls}'
        feat, js = mutant_files(cls, k, n); stepf = f'{W}/mutants/{name}.js'; open(stepf, 'w').write(js)
        open(f'{W}/mutants/{name}.feature.add', 'w').write(feat)
        if done(name + '-serial') and done(name + '-v2-A') and done(name + '-v2-B'): continue
        for c in COPIES.values():
            subprocess.run(['git', '-C', c, 'checkout', '-q', '--', f'.kogen/intents/{intent}/acceptance.feature'], check=True)
            open(feat_path(c, intent), 'a').write(feat)
        try:
            run1(name + '-serial', COPIES['A'], feat_path(COPIES['A'], intent), 'defined', stepf)
            run2(name + '-v2', feat_path(COPIES['A'], intent), (101, 202), stepf, g=False)  # r5: one guard per mutant (serial then pair)
        finally:
            for c in COPIES.values(): subprocess.run(['git', '-C', c, 'checkout', '-q', '--', f'.kogen/intents/{intent}/acceptance.feature'], check=True)
def stage_slice(pl):
    sl = pl['slice']; fl = ' '.join(feat_path(COPIES['A'], i) for i in sl); kenv = INTENTS(COPIES['A'])
    run1('slice-serial', COPIES['A'], fl, 'defined', '', kenv)
    for k in range(1, 11):
        if os.environ.get('SLICE_DEADLINE') and time.time() > float(os.environ['SLICE_DEADLINE']): log('SLICE stop: past deadline before repeat', k); break
        run2(f'slice-v2-r{k:02d}', fl, (1000 + 2 * k, 1001 + 2 * k), '', kenv)
def ensure_copies():
    for c in COPIES.values():
        if not os.path.isdir(c): subprocess.run(['cp', '-a', W + '/kogen', c], check=True)

if __name__ == '__main__':
    st = sys.argv[1]; ensure_copies(); log('STAGE', st)
    full = INTENTS(COPIES['A'])
    if st == 'v4':
        reps = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        for k in range(1, reps + 1): run1(f'v4-r{k}', COPIES['A'], full, 'defined')
    elif st == 'auto':
        r1 = run1('v4-r1', COPIES['A'], full, 'defined'); pl = plan(); T = r1['wall']; reps = 3 if T <= 1200 else 2
        log('RULE T=%.0fs -> v4 reps %d, full-suite V2 pair %s' % (T, reps, 'yes' if T <= 1200 else 'no'))
        for k in range(2, reps + 1): run1(f'v4-r{k}', COPIES['A'], full, 'defined')
        stage_mut(pl); stage_slice(pl)
        if T <= 1200: run2('full-v2', full, (101, 202), '', full)
    elif st == 'quick':  # r5: delivery Builds kept EU busy; mutants and slice run on the Intents finished in repeat 1; r1b skipped
        r1 = get('v4-r1'); pl = plan(); log('QUICK mutants then slice; hosts', sorted({m['intent'] for m in pl['mutants']}))
        stage_mut(pl); stage_slice(pl)
    elif st == 'r1b':
        a = get('v4-r1'); done_u = {x['uri'] for x in a['scen']} | {'.kogen/intents/go-core-migration/acceptance.feature'}
        allf = sorted(os.listdir(INTENTS(COPIES['A']))); rest = [f'{INTENTS(COPIES["A"])}/{i}/acceptance.feature' for i in allf if f'.kogen/intents/{i}/acceptance.feature' not in done_u and os.path.exists(f'{INTENTS(COPIES["A"])}/{i}/acceptance.feature')]
        log('R1B intents', len(rest)); run1('v4-r1b', COPIES['A'], ' '.join(rest), 'defined', '', full); merge_r1()
    elif st == 'salvage': salvage(float(sys.argv[2]), float(sys.argv[3]))
    elif st == 'rest':  # after v4-r1: mutants first, then the second V4 repeat, then the slice (time-capped), then the full pair if the rule allows
        r1 = get('v4-merged'); T = r1['wall']; pl = plan()
        log('REST (r4): mutants then time-capped slice; no more full repeats')
        stage_mut(pl)
        stage_slice(pl)
    elif st == 'plan': plan()
    elif st == 'mut': stage_mut(json.load(open(W + '/plan.json')))
    elif st == 'slice': stage_slice(json.load(open(W + '/plan.json')))
    elif st == 'full': run2('full-v2', full, (101, 202), '', full)
    log('STAGE-END', st)
