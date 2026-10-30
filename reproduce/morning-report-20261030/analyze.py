"""Recompute the morning-report numbers that can be derived from the shipped rows.
usage: python3 analyze.py   (standard library only)

Inputs: runs.csv (API confirmation high/medium, API patch screen; counted + dry rows) and stream-rates.csv.
Definitions as in the report: wall = agent-process time; p90 = nearest rank on all counted runs with a wall;
USD per pass = all counted USD / counted passes; mean-wall and cost ratios are loop / Codex;
paired "faster / cheaper on N of 4 tasks" compares per-task means; the noise floor is
|wall1 - wall2| / mean over same-tool, same-task repetitions (loop and Codex only), median and range."""
import csv, math, statistics as S, pathlib, collections

H = pathlib.Path(__file__).resolve().parent
f = float
runs = list(csv.DictReader(open(H / 'runs.csv')))
streams = list(csv.DictReader(open(H / 'stream-rates.csv')))


def summ(x):
    w = sorted(f(r['wall_s']) for r in x)
    passes = [r for r in x if r['passed'] == 'true']
    usd = sum(f(r['cost_usd']) for r in x)
    return dict(n=len(x), passes=len(passes), med=S.median(w), p90=w[math.ceil(.9 * len(w)) - 1], mean=S.mean(w), usd_pass=usd / len(passes))


def sel(exp, effort, stratum, tool):
    return [r for r in runs if r['experiment'] == exp and r['effort'] == effort and r['stratum'] == stratum and r['tool'] == tool]


for effort in ('high', 'medium'):
    print('== common API route, gpt-6.1-terra, %s effort (4 tasks x 2 reps, counted) ==' % effort)
    res = {}
    for tool in ('loop', 'codex') + (('speed2',) if effort == 'medium' else ()):
        s = res[tool] = summ(sel('api-confirm', effort, 'counted', tool))
        print('%-7s pass %d/%d  median %.2f  p90 %.2f  mean %.3f  USD/pass $%.6f' % (tool, s['passes'], s['n'], s['med'], s['p90'], s['mean'], s['usd_pass']))
    print('loop/Codex mean-wall ratio %.3f, cost ratio %.3f' % (res['loop']['mean'] / res['codex']['mean'], res['loop']['usd_pass'] / res['codex']['usd_pass']))
    tasks = sorted({r['task'] for r in runs if r['experiment'] == 'api-confirm' and r['effort'] == effort and r['stratum'] == 'counted'})
    fw = ch = 0
    for t in tasks:
        a = [r for r in sel('api-confirm', effort, 'counted', 'loop') if r['task'] == t]
        b = [r for r in sel('api-confirm', effort, 'counted', 'codex') if r['task'] == t]
        fw += S.mean(f(r['wall_s']) for r in a) < S.mean(f(r['wall_s']) for r in b)
        ch += S.mean(f(r['cost_usd']) for r in a) < S.mean(f(r['cost_usd']) for r in b)
    print('loop faster on %d/%d task means, cheaper on %d/%d' % (fw, len(tasks), ch, len(tasks)))
    d = []
    for tool in ('loop', 'codex'):
        for t in tasks:
            w = [f(r['wall_s']) for r in sel('api-confirm', effort, 'counted', tool) if r['task'] == t]
            d.append(abs(w[0] - w[1]) / S.mean(w))
    print('repeat scatter (%d task-tool pairs): median %.2f%%, range %.2f-%.2f%%' % (len(d), 100 * S.median(d), 100 * min(d), 100 * max(d)))
    if effort == 'high':
        for tool in ('loop', 'codex'):
            allr = [r for r in runs if r['experiment'] == 'api-confirm' and r['effort'] == 'high' and r['tool'] == tool]
            n = len([r for r in allr if r['stratum'] == 'counted' and r['passed'] == 'true'])
            print('  incl. dry attempts: %s USD per counted pass $%.6f' % (tool, sum(f(r['cost_usd']) for r in allr) / n))
    print()

print('== API patch screen, high effort, 4 tasks x 1 rep (counted) ==')
base = summ(sel('api-patch-screen', 'high', 'counted', 'loop-b8a4046'))
for tool in ('loop-b8a4046', 'speed2', 'api-replay', 'api-batch', 'api-answer-end', 'wall-http2', 'wall-h1reuse'):
    x = sel('api-patch-screen', 'high', 'counted', tool)
    s = summ(x)
    print('%-15s pass %d/%d  median %.2f  p90 %.2f  USD/pass $%.6f  mean-wall change vs loop %+.1f%%' % (tool, s['passes'], s['n'], s['med'], s['p90'], s['usd_pass'], 100 * (s['mean'] / base['mean'] - 1)))
allb = [r for r in runs if r['experiment'] == 'api-patch-screen' and r['tool'] == 'api-batch']
print('api-batch incl. its dry attempt: $%.6f per counted pass' % (sum(f(r['cost_usd']) for r in allb) / 4))

print('\n== loop output rate (output tokens / body-stream seconds, runs with > 200 output tokens), by start window ==')
WIN = (('29 Oct 18-21Z', '2026-10-29T18', '2026-10-29T22'), ('30 Oct 04-05Z', '2026-10-30T04', '2026-10-30T06'))
for label, a, b in WIN:
    by = collections.defaultdict(list)
    for r in streams:
        if a <= r['started_utc'][:13] < b and f(r['output_tokens']) > 200 and f(r['body_stream_s']):
            by[(r['round'], r['host'])].append(f(r['output_tokens']) / f(r['body_stream_s']))
    print(label)
    for k in sorted(by):
        print('  %-7s %-6s n=%-3d median %.1f' % (k[0], k[1], len(by[k]), S.median(by[k])))
