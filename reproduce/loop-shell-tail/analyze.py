#!/usr/bin/env python3
"""Rebuild the published loop-shell-tail tables from runs.csv, results.csv and tail-pool.csv.

Standard library only. Prints the tables; compare with expected-output.txt.
"""
import collections, csv, itertools, math, pathlib, statistics

HERE = pathlib.Path(__file__).resolve().parent


def load(name):
    with open(HERE / name, newline='') as f:
        return list(csv.DictReader(f))


runs = load('runs.csv')
results = load('results.csv')
pool = load('tail-pool.csv')

for r in runs:
    r['wall_s'] = float(r['wall_s'])
    r['passed'] = r['passed'] == 'True'
for t in results:
    t['bytes'] = int(t['bytes'])
    t['cut'] = t['cut'] == 'True'
    t['seconds_q'] = float(t['seconds_q']) if t['seconds_q'] else None
    t['later'] = int(t['later_provider_attempts']) if t['later_provider_attempts'] else 0
    t['kinds'] = t['categories'].split(';') if t['categories'] else []

def key(x):
    return (x['round'], x['effort'], x['task'], x['rep'])

res = collections.defaultdict(list)
for t in results:
    res[key(t) + (t['tool'],)].append(t)

# Pairs: one loop row and one Codex row per (round, effort, task, rep), in file order.
loops = [r for r in runs if r['tool'] == 'loop']
codex = {key(r): r for r in runs if r['tool'] == 'codex'}
pairs = [(l, codex[key(l)]) for l in loops]

# Tail: slowest ceil(n/4) baseline loop runs by agent wall per round/effort, chosen before pairing.
tail = set()
for g, v in itertools.groupby(sorted(pool, key=lambda r: (r['round'], r['effort'])), key=lambda r: (r['round'], r['effort'])):
    v = list(v)
    top = sorted(v, key=lambda r: (-float(r['wall_s']), r['task'], r['rep']))[:math.ceil(len(v) / 4)]
    tail.update(key(r) for r in top)
for l, _ in pairs:
    assert (key(l) in tail) == (l['tail'] == 'True'), key(l)

def L(p): return res[key(p[0]) + ('loop',)]
def C(p): return res[key(p[1]) + ('codex',)]
def sh(p): return [t for t in L(p) if t['name'] == 'shell']
def known(p): return [t for t in sh(p) if t['decoded'] == 'True']
def lower(tt): return sum(max(0, t['seconds_q'] - 1) for t in tt)
def upper(tt): return sum(t['seconds_q'] + 1 for t in tt)
def ssec(tt): return sum(t['seconds_q'] for t in tt)
def lbytes(p): return sum(t['bytes'] for t in L(p))
def cbytes(p): return sum(t['bytes'] for t in C(p))
def delta(p): return p[0]['wall_s'] - p[1]['wall_s']
def dups(tt, field='repeat_group'):
    seen = set(); out = []
    for t in tt:
        k = (t['name'], t[field])
        if k in seen: out.append(t)
        seen.add(k)
    return out
def crepeatbytes(p): return sum(t['bytes'] for t in dups(C(p)))
def num(x): return f'{x:,.1f}'
def integer(x): return f'{x:,}'
def table(head, rows):
    return '\n'.join(['| ' + ' | '.join(head) + ' |', '|' + '|'.join(['---'] * len(head)) + '|'] +
                     ['| ' + ' | '.join(map(str, r)) + ' |' for r in rows]) + '\n'
def label(g): return ('EU' if g[0].startswith('eu-api') else g[0]) + ' ' + g[1]

grp = lambda p: (p[0]['round'], p[0]['effort'])
groups = [(g, list(v)) for g, v in itertools.groupby(sorted(pairs, key=grp), grp)]
out = []
P = lambda s='': out.append(s)

both = [p for p in pairs if p[0]['passed'] and p[1]['passed']]
P(f'Both-pass pairs: {len(both)}; both-false pairs: {len(pairs) - len(both)}')
allsh = [t for p in pairs for t in sh(p)]
unk = [t for t in allsh if t['decoded'] != 'True']
P(f'Decoded loop shells: {len(allsh) - len(unk)}/{len(allsh):,} invocations, {num(ssec(allsh) - ssec(unk))}/{num(ssec(allsh))} quantized shell s; unclassified {len(unk)} / {num(ssec(unk))} s')
fewer = [label(g) for g, pp in groups if sum(len(sh(p)) for p in pp) < sum(len(C(p)) for p in pp)]
fewb = [label(g) for g, pp in groups if sum(map(lbytes, pp)) < sum(map(cbytes, pp))]
P(f'Cohorts with fewer loop shells than Codex commands: {len(fewer)}/{len(groups)}')
P(f'Cohorts with fewer loop output bytes than Codex saved bytes: {", ".join(fewb)}')
P()
rr = []
for g, pp in groups:
    rr.append([label(g) + (' (both false)' if not pp[0][0]['passed'] else ''), len(pp), sum(p[0]['tail'] == 'True' for p in pp),
               f"{sum(len(sh(p)) for p in pp)}/{sum(len(C(p)) for p in pp)}", f"{sum(len(known(p)) for p in pp)}/{sum(len(sh(p)) for p in pp)}",
               num(sum(ssec(sh(p)) for p in pp)), num(sum(map(delta, pp))), integer(sum(map(lbytes, pp))), integer(sum(map(cbytes, pp))),
               f"{sum(map(lbytes, pp)) - sum(map(cbytes, pp)):+,}"])
P(table(['Round/effort', 'Pairs', 'Tail pairs', 'Shell L / cmds C', 'Decoded L', 'L shell s', 'Δ agent s', 'L bytes', 'C saved bytes', 'Δ bytes'], rr))
rr = []
for g, pp in groups:
    tt = [p for p in pp if p[0]['tail'] == 'True']
    rr.append([label(g), len(tt), num(sum(ssec(sh(p)) for p in tt)), num(sum(map(delta, tt))),
               integer(sum(map(lbytes, tt)) - sum(map(cbytes, tt))), num(sum(ssec([t for t in sh(p) if t['decoded'] != 'True']) for p in tt))])
P(table(['Tail only', 'n', 'L shell s', 'Δ agent s', 'Δ recorded bytes', 'Unclassified L shell s'], rr))

hard = [p for p in pairs if p[0]['round'] == 'h2h-22']
hsh = [t for p in hard for t in sh(p)]
P(f"h2h-22: {num(ssec(hsh))} shell s, {integer(sum(t['bytes'] for t in hsh))} shell-output bytes, "
  f"{num(ssec([t for t in hsh if t['decoded'] != 'True']))} s unclassified; tail runs {num(sum(ssec(sh(p)) for p in hard if p[0]['tail'] == 'True'))} shell s")
positive = [(p, lower(sh(p)) - p[1]['wall_s']) for p in pairs if lower(sh(p)) > p[1]['wall_s']]
P(f"Positive excess bound summed over h2h-22 runs: {sum(x for p, x in positive if p[0]['round'] == 'h2h-22'):,.3f} s")
rp = [t for p in both for t in dups(L(p))]
P(f"Repeats across both-pass pairs: {sum(t['name'] == 'shell' for t in rp)} shells / {num(ssec([t for t in rp if t['name'] == 'shell']))} s / "
  f"{integer(sum(t['bytes'] for t in rp if t['name'] == 'shell'))} bytes; read_file {sum(t['name'] == 'read_file' for t in rp)} / "
  f"{integer(sum(t['bytes'] for t in rp if t['name'] == 'read_file'))} bytes")
hp = [t for p in hard for t in dups(L(p)) if t['name'] == 'shell']
P(f"Repeats h2h-22: {len(hp)} shells / {num(ssec(hp))} s / {integer(sum(t['bytes'] for t in hp))} bytes")
P()
P(table(['Round / task / rep', 'Both pass', 'L shell interval s', 'C entire agent s', 'Guaranteed excess shell s'],
        [[f"{p[0]['round']} / {p[0]['task']} / {p[0]['rep']}", p[0]['passed'], f"{num(lower(sh(p)))}–{num(upper(sh(p)))}", num(p[1]['wall_s']), f'>{x:.3f}'] for p, x in positive]))
rr = []
for g, pp in groups:
    ls = [t for p in pp for t in known(p)]; cc = [t for p in pp for t in C(p)]
    def counts(k): return f"≥{sum(k in t['kinds'] for t in ls)}/{sum(k in t['kinds'] for t in cc)}"
    rr.append([label(g)] + [counts(k) for k in ['test', 'module-test', 'targeted-test', 'race', 'count', 'build', 'vet', 'format', 'make-check', 'read', 'git']])
P(table(['Round', 'test L/C', 'module', 'targeted', 'race', 'count', 'build', 'vet', 'fmt', 'make check', 'read/discover', 'git'], rr))
rr = []
for g, pp in groups:
    aa = [t for p in pp for t in L(p) if t['name'] != 'shell']
    rr.append([label(g)] + [sum(t['name'] == k for t in aa) for k in ['list_files', 'read_file', 'search_text', 'write_file']] +
              [num(ssec(aa)), integer(sum(t['bytes'] for t in aa if t['name'] in ['list_files', 'read_file', 'search_text']))])
P(table(['Round', 'list', 'read', 'search', 'write', 'Builtin s quantized', 'Builtin read/discovery bytes'], rr))
rr = []
for g, pp in groups:
    lr = [t for p in pp for t in dups(L(p)) if t['name'] == 'shell']
    rr.append([label(g), sum(int(p[0]['multishell_responses']) for p in pp), sum(int(p[1]['overlapping_starts']) for p in pp), len(lr), num(ssec(lr)),
               integer(sum(t['bytes'] for t in lr)), sum(len(dups(C(p))) for p in pp), integer(sum(map(crepeatbytes, pp))),
               f"{sum(t['bytes'] for t in lr) - sum(map(crepeatbytes, pp)):+,}"])
P(table(['Round', 'L multishell responses', 'C starts while active', 'L repeated shells', 'L repeat s', 'L repeat bytes', 'C repeated command text', 'C repeat saved bytes', 'Δ repeated bytes'], rr))
rr = []
for p in pairs:
    d = dups(L(p))
    if d:
        rr.append([label(grp(p)), p[0]['task'] + '/' + p[0]['rep'], ','.join(t['name'] for t in d), num(ssec(d)), integer(sum(t['bytes'] for t in d)),
                   len(dups(L(p), 'result_group')), len(dups(C(p))), integer(crepeatbytes(p)), f"{sum(t['bytes'] for t in d) - crepeatbytes(p):+,}"])
P(table(['Round', 'Task/rep', 'Repeated tools', 'Later-call s', 'Later-call bytes', 'Same result too (n)', 'C repeats', 'C repeat saved bytes', 'Δ repeated bytes'], rr))
def pct(vals, q): return sorted(vals)[max(0, math.ceil(len(vals) * q) - 1)] if vals else 0
rr = []
for g, pp in groups:
    a = [t for p in pp for t in L(p)]; b = [t for p in pp for t in C(p)]
    for side, vals, cuts in [('loop', [t['bytes'] for t in a], sum(t['cut'] for t in a)), ('Codex saved', [t['bytes'] for t in b], sum(t['cut'] for t in b))]:
        rr.append([label(g), side, len(vals), integer(int(statistics.median(vals))), integer(pct(vals, .9)), integer(max(vals)), cuts])
P(table(['Round', 'Side', 'Results', 'Median bytes', 'p90 bytes', 'Max bytes', 'Cuts / C marker hits'], rr))
P(table(['Round', 'Loop result bytes delivered once', 'Loop logical replay bytes', 'Codex replay / excess'],
        [[label(g), integer(sum(map(lbytes, pp))), integer(sum(t['bytes'] * t['later'] for p in pp for t in L(p))), '? / ?'] for g, pp in groups]))
rr = []
for g, pp in groups[:2]:
    for task, v in itertools.groupby(sorted(pp, key=lambda p: p[0]['task']), lambda p: p[0]['task']):
        vv = list(v)
        rr.append([label(g), task, num(sum(ssec(sh(p)) for p in vv)), integer(sum(t['bytes'] for p in vv for t in sh(p))),
                   integer(sum(t['bytes'] for p in vv for t in L(p) if t['name'] in ['read_file', 'list_files', 'search_text'])),
                   integer(sum(map(cbytes, vv))), f"{sum(lbytes(p) - cbytes(p) for p in vv):+,}"])
P(table(['EU effort', 'Task', 'L shell s', 'L shell bytes', 'L builtin read bytes', 'C all saved bytes', 'Δ all bytes'], rr))
for g, pp in groups:
    P('### ' + label(g) + (' — both recorded false' if not pp[0][0]['passed'] else ' — both pass') + '\n')
    rr = []
    for task, v in itertools.groupby(sorted(pp, key=lambda p: p[0]['task']), lambda p: p[0]['task']):
        vv = list(v); ss = [t for p in vv for t in sh(p)]
        rr.append([task, len(vv), ','.join(p[0]['rep'] for p in vv if p[0]['tail'] == 'True') or '—', f"{len(ss)}/{sum(len(C(p)) for p in vv)}",
                   sum(len(known(p)) for p in vv), num(ssec(ss)), f"{num(lower(ss))}–{num(upper(ss))}",
                   num(sum(lower(sh(p)) - p[1]['wall_s'] for p in vv)), f"{sum(map(delta, vv)):+.1f}",
                   f"{sum(map(lbytes, vv)):,}/{sum(map(cbytes, vv)):,}", f"{sum(lbytes(p) - cbytes(p) for p in vv):+,}"])
    P(table(['Task', 'n', 'T', 'Shell L/C cmds', 'Decoded', 'L shell s', 'L interval s', 'Excess lower s', 'Δ wall s', 'Bytes L/C', 'Δ bytes'], rr))
print('\n'.join(out), end='')
