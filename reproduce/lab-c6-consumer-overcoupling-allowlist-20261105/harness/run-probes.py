#!/usr/bin/env python3
"""run-probes.py <W> <level> <reps> <deadline_epoch> <label>...   (Lab C6, on the Linux host as lanes, no model)
One probe = one run of one test in one prebuilt test binary, working directory = that tree's build/ package. Arms: current =
TestBuildRequestBudgetOff (the tree's own test), allow = TestBuildRequestBudgetOffAllow (arm A projection). Loop order: rep, tree, arm
(arm order alternates per tree+rep), so any prefix of the schedule is balanced. Appends one JSON line per probe to W/out/probes.jsonl."""
import json, os, subprocess, sys, time
W, level, reps, deadline = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4]); labels = sys.argv[5:]
ARMS = {'current': 'TestBuildRequestBudgetOff', 'allow': 'TestBuildRequestBudgetOffAllow'}
out = open(f'{W}/out/probes.jsonl', 'a')
def load1(): return float(open('/proc/loadavg').read().split()[0])
avail = {}
for l in labels:
    b = f'{W}/bin/{l}.test'
    if not os.path.exists(b): continue
    r = subprocess.run([b, '-test.list', '^TestBuildRequestBudgetOff'], cwd=f'{W}/trees/{l}/build', capture_output=True, text=True)
    avail[l] = [a for a, n in ARMS.items() if n in r.stdout.split()]
n = 0
for rep in range(reps):
    for ti, l in enumerate(labels):
        arms = avail.get(l, [])
        if (ti + rep) % 2: arms = arms[::-1]
        for a in arms:
            if time.time() > deadline or os.path.exists(f'{W}/out/STOP'): print('cap or STOP at', n, 'probes'); sys.exit(0)
            l0 = load1(); t = time.time()
            r = subprocess.run([f'{W}/bin/{l}.test', '-test.run', '^' + ARMS[a] + '$', '-test.count=1', '-test.timeout=180s'],
                               cwd=f'{W}/trees/{l}/build', capture_output=True, text=True, env=dict(os.environ, TMPDIR=f'{W}/tmp'))
            w = time.time() - t
            txt = (r.stdout + r.stderr)
            detail = ''
            if r.returncode:
                keep = [x for x in txt.splitlines() if 'differs' in x or 'omitted' in x or 'zero:' in x or '--- FAIL' in x or 'panic' in x or 'budget' in x]
                detail = ' | '.join(keep)[:400] or txt[-300:]
            out.write(json.dumps(dict(label=l, arm=a, level=level, rep=rep, rc=r.returncode, wall=round(w, 2), load_before=l0, load_after=load1(), t=int(t), detail=detail)) + '\n'); out.flush()
            n += 1
print('done', n, 'probes')
