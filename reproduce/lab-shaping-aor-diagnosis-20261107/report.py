#!/usr/bin/env python3
"""report.py <pack dir>: prints every table of this finding from data/.

data/c6-aor-attempts.json   stage 3's C6 cells on the five Rails tasks: per attempt the gate, problem-line count, kinds and class
data/release-aor-attempts.json  the release's stored cells of the same tasks
data/replay.json            the model-free replay: per case and tree (pin, C6, C7) refused or not, problem lines, equal to the recorded refusal
data/c7-aor-cells.json      C7 on the five Rails tasks (one rep, 1800 s)
data/c7-heldout-cells.json  C7 on stage 3's five held-out small requests x 2 (900 s)
data/stage3-heldout.json    stage 3's stored held-out cells (C6 and release) for comparison
"""
import collections, json, os, sys

d = sys.argv[1] if len(sys.argv) > 1 else '.'
load = lambda n: json.load(open(os.path.join(d, 'data', n)))

def attempts_line(c):
    return '; '.join(f"{a['attempt']}: {a['gate'].replace('_', ' ')} {a['problem_lines']}" + (f" ({','.join(a['classes'])})" if a.get('classes') else '')
                     for a in c.get('attempts', []) if a['gate'] != 'none (accepted)') or 'none'

print('== C6 on the Rails tasks (stage 3 run), per attempt: gate, problem lines (class a/b/c)')
for c in load('c6-aor-attempts.json'):
    rounds = ', '.join(f"{a['shaper_round_s']} s/{a['shaper_tool_calls']} calls" for a in c['attempts'])
    print(f"  {c['task']}: {c['outcome']:<8} {c['wall_s']:>5} s  {c['cost_usd']:>5} USD  {attempts_line(c)}  | shaper rounds: {rounds}")
kinds = collections.Counter()
for c in load('c6-aor-attempts.json'):
    for a in c['attempts']:
        kinds.update(a['kinds'])
print('  problem lines by kind:', dict(kinds))

print('== release on the same tasks (stored), per attempt: gate, problem lines; decisions lists submitted')
for c in load('release-aor-attempts.json'):
    print(f"  {c['task']}: {c['outcome']:<8} {c['wall_s']:>5} s  " + '; '.join(f"{a['attempt']}: {a['gate'].replace('_', ' ')} {a['problem_lines']}" for a in c['attempts'])
          + f"  | decisions submitted: {sum(a['decisions_submitted'] for a in c['attempts'])}")

print('== model-free replay (refused/problem lines; = equals the recorded refusal)')
rp = load('replay.json')
for case, arms in rp['cases'].items():
    cells = '  '.join(f"{arm}: {'refused' if v['refused'] else 'passes'} {v['problem_lines']}{' =' if v['same_as_recorded'] else ''}" for arm, v in arms.items())
    print(f'  {case:<64} {cells}')

print('== C7 on the Rails tasks (one rep, 1800 s)')
aor = load('c7-aor-cells.json')
for c in aor:
    if 'wall_s' not in c:
        print(f"  {c['task']}: {c['outcome']}"); continue
    first = c['attempts'][0] if c['attempts'] else {}
    print(f"  {c['task']}: {c['outcome']:<8} {c['wall_s']:>5} s  {c['cost_usd']:>5} USD  refusals: {attempts_line(c)}  | first package files {first.get('files', '-')}, "
          f"round 1 {first.get('shaper_round_s', '-')} s/{first.get('shaper_tool_calls', '-')} calls; wrong-implementation checks {c['wrong_implementation_checks'] or '-'}"
          + (f"; shaper round {c['unfinished_shaper_round']} unfinished at the deadline" if c.get('unfinished_shaper_round') else ''))
ready = sum(c['outcome'] in ('ok', 'ready') for c in aor)
print(f'  ready {ready} of {len(aor)} (rule: at least 2)')

print('== C7 on the held-out small requests (5 x 2, 900 s)')
hv = load('c7-heldout-cells.json')
for c in hv:
    print(f"  {c['cell']:<12} {c['outcome']:<8} attempts {c['attempts_used']}  {c['wall_s']:>4} s  {c['cost_usd']:>5} USD  refusals: {attempts_line(c)}")
hr = sum(c['outcome'] == 'ready' for c in hv); hf = sum(c['outcome'] == 'ready' and c['attempts_used'] == 1 for c in hv)
print(f'  ready {hr} of {len(hv)} (rule: at least 9), first attempt {hf}')
s3 = load('stage3-heldout.json')
for arm in ('C6', 'A'):
    rows = [c for c in s3 if c['arm'] == arm]
    print(f"  stage 3 {arm}: ready {sum(c['outcome'] == 'ready' for c in rows)} of {len(rows)}, first attempt {sum(c['outcome'] == 'ready' and c['attempts'] == 1 for c in rows)}")
print('== cost (Claude Code reported, USD): Rails', round(sum(c.get('cost_usd') or 0 for c in aor), 2), ' held-out', round(sum(c['cost_usd'] for c in hv), 2))
