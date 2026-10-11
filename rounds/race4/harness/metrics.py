#!/usr/bin/python3
# metrics.py — per-arm race 4 metrics after the race: score curve, time to 75/90/100 % (of N), wall time, turns, tokens, CPU time,
# build/test command time, build-output size, lines of code, test definitions, audit flags. Writes out/METRICS.md and out/metrics.json.
import json, os, re, glob, subprocess, collections, math
from pathlib import Path
from scoring_config import counts
from tokens_at import TOKEN_FIELDS, usage_at, snapshot_time
COUNTS, EXCLUSIONS = counts()
N = COUNTS["N_scored"]; N_total = COUNTS["N_total"]; TARGET = COUNTS["target"]
T75 = math.ceil(0.75 * N); T90 = math.ceil(0.90 * N)
R = os.path.dirname(os.path.abspath(__file__)); O = R + '/out'
arms = open(R + '/ARMS').read().split(); start = int(open(R + '/START').read())
scores = collections.defaultdict(dict)
for l in open(O + '/scores.tsv'):
    f = l.rstrip('\n').split('\t')
    if len(f) < 5: continue
    lab, a = f[:2]
    full = int(f[2].split('/')[0]) if f[2].split('/')[0].isdigit() else None
    ex = int(f[3].split()[1].split('/')[0])
    m = re.match(r'T\+(\d+)m', lab); mins = int(m.group(1)) if m else None
    if lab.startswith('TARGET-'):
        mins = (int(open(R + '/snapshots/' + lab + '/TAKEN_EPOCH').read()) - start) / 60
    if lab == 'FINAL':
        mins = (int(open(R + '/DEADLINE').read()) - start) / 60
    scores[a][lab] = (mins, full, ex)
def first_reach(a, k):
    pts = sorted((v[0], v[2]) for v in scores[a].values() if v[0] is not None)
    for mins, ex in pts:
        if ex >= k: return mins
    return None
BUILD = re.compile(r'\b(cargo (build|check|test|clippy|nextest|fmt)|go (build|test|vet)|golangci-lint|gofmt|bun (test|run|build)|tsc|biome|gleam (build|test|check|format)|mix (compile|test|credo|format)|kogen-conformance run)\b')
res = {}
for a in arms:
    d = O + '/' + a; turns = sorted(glob.glob(d + '/turn-*.jsonl'))
    cpu = 0.0; cpu_seen = False
    for e in glob.glob(d + '/turn-*.err'):
        for l in open(e, errors='ignore'):
            m = re.match(r'\s*([\d.]+) real\s+([\d.]+) user\s+([\d.]+) sys', l)
            if m: cpu += float(m.group(2)) + float(m.group(3)); cpu_seen = True
    bt = collections.Counter()
    for t in glob.glob(d + '/turn-*.jsonl'):
        cmds = {}
        for l in open(t, errors='ignore'):
            try: e = json.loads(l)
            except Exception: continue
            it = e.get('item') or {}
            if it.get('type') == 'command_execution': cmds[it.get('id')] = it.get('command') or ''
        tsf = t[:-6] + '.ts'; st = {}
        if os.path.exists(tsf):
            for l in open(tsf):
                ep, typ, iid, ityp = (l.rstrip('\n').split('\t') + ['', '', '', ''])[:4]
                if ityp != 'command_execution': continue
                if typ == 'item.started': st[iid] = float(ep)
                elif typ == 'item.completed' and iid in st:
                    m = BUILD.search(cmds.get(iid, '')); bt['build_test_s' if m else 'other_cmd_s'] += float(ep) - st[iid]
    wall = 0.0
    for tsf in glob.glob(d + '/turn-*.ts'):
        tt = [float(l.split('\t')[0]) for l in open(tsf) if l.strip()]
        if tt: wall += tt[-1] - tt[0]
    timing_seen = bool(glob.glob(d + '/turn-*.ts'))
    cmd_total = sum(bt.values()); model_wait = max(0.0, wall - cmd_total)
    bt.setdefault('build_test_s', 0); bt.setdefault('other_cmd_s', 0)
    tok = usage_at(Path(R), a)
    # Official per-snapshot both-pass scores choose the boundary, never watcher counts.
    qualifying = [(v[0], label) for label, v in scores[a].items()
                  if v[0] is not None and v[2] >= TARGET]
    token_snapshot = min(qualifying)[1] if qualifying else 'FINAL'
    token_time = snapshot_time(Path(R), token_snapshot)
    token_target = usage_at(Path(R), a, token_time) if token_time is not None else dict.fromkeys(TOKEN_FIELDS)
    fin = R + '/snapshots/FINAL/' + a; loc = 0; tests = 0
    ext = {'rust': ('.rs',), 'go': ('.go',), 'ts': ('.ts', '.tsx'), 'gleam': ('.gleam',), 'ex': ('.ex', '.exs')}[a]
    tpat = {'rust': r'#\[test\]', 'go': r'^func Test', 'ts': r'\b(test|it)\(', 'gleam': r'pub fn \w+_test\(', 'ex': r'^\s*test "'}[a]
    for root, dirs, files in os.walk(fin):
        dirs[:] = [x for x in dirs if x not in ('spec', 'conformance', 'target', 'build', '_build', 'deps', 'node_modules', '.git', '.cache', '.kitcache')]
        for fn in files:
            if fn.endswith(ext):
                try: txt = open(os.path.join(root, fn), errors='ignore').read()
                except Exception: continue
                loc += sum(1 for x in txt.splitlines() if x.strip()); tests += len(re.findall(tpat, txt, re.M))
    size = 0
    for sub in ('target', 'build', '_build', 'bin', 'dist'):
        p = fin + '/' + sub
        if os.path.isdir(p): size += int(subprocess.run(['du', '-sk', p], capture_output=True, text=True).stdout.split()[0] or 0)
    end = None
    for l in open(O + '/arms.log'):
        m = re.match(r'arm %s ended turns=\d+ (\d\d:\d\d:\d\d)' % a, l)
        if m: end = m.group(1)
    fs = scores[a].get('FINAL', (None, None, None))
    stalls = [int(l.split()[1]) for l in open(d + '/stalls.log')] if os.path.exists(d + '/stalls.log') else []
    def adj(mins):  # minutes with quota/rate-limit stall waits (60 s each) before that time removed
        if mins is None: return None
        cut = start + mins * 60; return round(mins - sum(60 for e in stalls if e < cut) / 60, 1)
    res[a] = dict(curve={k: v[1:] for k, v in sorted(scores[a].items(), key=lambda kv: (kv[1][0] is None, kv[1][0] or 0))},
                  final_total=fs[1], final_scored=fs[2], t75=first_reach(a, T75), t90=first_reach(a, T90), t_target=first_reach(a, TARGET), t100=first_reach(a, N),
                  ended=end or 'n/a (no arm exit recorded)', turns=len(turns), cpu_s=round(cpu) if cpu_seen else 'n/a (no time -l CPU record)',
                  tokens={k: tok[k] if tok[k] is not None else 'n/a (no session token receipt)' for k in TOKEN_FIELDS},
                  tokens_to_target={k: token_target[k] if token_target[k] is not None else 'n/a (no timestamped token receipt)' for k in TOKEN_FIELDS},
                  tokens_to_target_snapshot=token_snapshot, tokens_to_target_at=token_time,
                  cmd_time_s={k: round(v) if timing_seen else 'n/a (no timestamped events)' for k, v in bt.items()},
                  turn_wall_s=round(wall) if timing_seen else 'n/a (no timestamped events)', model_wait_s=round(model_wait) if timing_seen else 'n/a (no timestamped events)',
                  quota_points='n/a (no registered token-to-quota conversion)',
                  build_output_kb=size, loc=loc, test_defs=tests,
                  stall_waits=len(stalls), t_target_adj=adj(first_reach(a, TARGET)), t75_adj=adj(first_reach(a, T75)), t90_adj=adj(first_reach(a, T90)), t100_adj=adj(first_reach(a, N)),
                  audit_flags=sum(1 for l in open(O + '/audit.txt') if l.startswith('FLAG ' + a + ' ')) if os.path.exists(O + '/audit.txt') else 'n/a (audit not run)')
    for key in ('final_total', 'final_scored'):
        if res[a][key] is None: res[a][key] = 'n/a (no official FINAL score)'
    for key in ('t75', 't90', 't_target', 't100', 't_target_adj', 't75_adj', 't90_adj', 't100_adj'):
        if res[a][key] is None: res[a][key] = 'n/a (threshold not reached in timed snapshots)'
ranking = sorted(arms, key=lambda a: (not isinstance(res[a]['t_target'], (int, float)),
                 res[a]['t_target'] if isinstance(res[a]['t_target'], (int, float)) else float('inf'),
                 -res[a]['final_scored'] if isinstance(res[a]['final_scored'], int) else 0))
for rank, arm in enumerate(ranking, 1):
    res[arm]['rank'] = rank
json.dump(ranking, open(O + '/ranking.json', 'w'), indent=1)
json.dump(res, open(O + '/metrics.json', 'w'), indent=1)
with open(O + '/METRICS.md', 'w') as w:
    columns = ['arm', f'FINAL /{N_total}', f'/{N}', 't75', 't90', f't_target({TARGET})', 't100', 't75 adj', 't90 adj', 't_target adj', 't100 adj', 'ended', 'turns', 'CPU s', 'build/test s', 'other command s', 'turn wall s', 'model wait s', 'stall waits', 'quota points', 'in', 'cached', 'out', 'reasoning', 'total', 'token snapshot', 'tokens-to-target in', 'tokens-to-target cached', 'tokens-to-target out', 'tokens-to-target reasoning', 'tokens-to-target total', 'build KB', 'LOC', 'tests', 'audit']
    w.write('| ' + ' | '.join(columns) + ' |\n|' + '---|' * len(columns) + '\n')
    for a, r in res.items():
        t = r['tokens']; c = r['cmd_time_s']
        row = [a] + [r[k] for k in ('final_total', 'final_scored', 't75', 't90', 't_target', 't100', 't75_adj', 't90_adj', 't_target_adj', 't100_adj', 'ended', 'turns', 'cpu_s')]
        row += [c['build_test_s'], c['other_cmd_s'], r['turn_wall_s'], r['model_wait_s'], r['stall_waits'], r['quota_points']]
        row += [t[k] for k in TOKEN_FIELDS]
        row += [r['tokens_to_target_snapshot']] + [r['tokens_to_target'][k] for k in TOKEN_FIELDS]
        row += [r[k] for k in ('build_output_kb', 'loc', 'test_defs', 'audit_flags')]
        w.write('| ' + ' | '.join(str(value) for value in row) + ' |\n')
print(open(O + '/METRICS.md').read())
