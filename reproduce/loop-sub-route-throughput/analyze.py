"""Reproduce the numbers in the loop-sub-route-throughput finding from runs.csv, turns.csv and probes/.

usage: python3 analyze.py            (standard library only)

Cohorts: "before" = cell started before 2026-10-30 04:00 UTC, "after" = at or after.
Rates are output tokens/s. Loop cells: output / sum(last_byte - first_byte) over request attempts,
cells with more than 200 output tokens. The snapshot cut-offs (05:14:56 UTC Mac A, 05:15:29 UTC Mac B)
are applied on ended_utc.
"""
import csv, json, statistics as S, pathlib

H = pathlib.Path(__file__).resolve().parent
f = lambda v: float(v) if v not in ('', None) else None
runs = list(csv.DictReader(open(H / 'runs.csv')))
turns = list(csv.DictReader(open(H / 'turns.csv')))
CUT = {'mac-a': '2026-10-30T05:14:56', 'mac-b': '2026-10-30T05:15:29'}
runs = [r for r in runs if r['ended_utc'][:19] <= CUT[r['host']]]
med = lambda v: round(S.median(v), 2)
print('rows within snapshot:', len(runs))


def loop_rate(host, tool, rounds):
    out = {}
    for after in ('False', 'True'):
        xs = [r for r in runs if r['host'] == host and r['tool'] == tool and r['round'] in rounds
              and r['after_0400utc'] == after and f(r['output_tokens']) > 200 and f(r['body_stream_s'])]
        rates = [f(r['output_tokens']) / f(r['body_stream_s']) for r in xs]
        pooled = sum(f(r['output_tokens']) for r in xs) / sum(f(r['body_stream_s']) for r in xs)
        out['after' if after == 'True' else 'before'] = (len(xs), med(rates), round(pooled, 2))
    return out


print('\n== loop body-stream rate (n, median, pooled) ==')
print('Mac A loop medium h2h-24 -> h2h-29', loop_rate('mac-a', 'loop-default-medium', ('h2h-24', 'h2h-29')))
print('Mac B loop high h2h-26           ', loop_rate('mac-b', 'loop-default', ('h2h-26',)))
print('Mac B speed2 high h2h-26         ', loop_rate('mac-b', 'speed2', ('h2h-26',)))

print('\n== Pi large write/edit-only turns (n turns, output tokens, seconds, tok/s lower bound) ==')
for after in ('False', 'True'):
    xs = [t for t in turns if t['tool'] == 'pi-terra-high' and t['after_0400utc'] == after
          and f(t['output_tokens']) > 200 and t['tool_names'] and set(json.loads(t['tool_names'])) <= {'write', 'edit'}]
    o = sum(f(t['output_tokens']) for t in xs); s = sum(f(t['upper_or_step_s']) for t in xs)
    print('after' if after == 'True' else 'before', len(xs), o, round(s, 3), round(o / s, 2))
for after in ('False', 'True'):
    v = [f(r['provider_upper_s']) for r in runs if r['tool'] == 'pi-terra-high' and r['after_0400utc'] == after]
    print('Pi summed per-cell upper bound median', 'after' if after == 'True' else 'before', S.median(v))

print('\n== OpenCode large steps (cells, median proxy, pooled) and DB message-span median ==')
for after in ('False', 'True'):
    xs = [r for r in runs if r['tool'] == 'opencode-terra-high' and r['after_0400utc'] == after]
    big = [r for r in xs if f(r['big_active_s']) and f(r['big_output_tokens'])]
    print('after' if after == 'True' else 'before', len(big),
          med([f(r['big_output_tokens']) / f(r['big_active_s']) for r in big]),
          round(sum(f(r['big_output_tokens']) for r in big) / sum(f(r['big_active_s']) for r in big), 2),
          'db span median', S.median(f(r['db_message_s']) for r in xs if r['db_message_s']))

print('\n== Mac A matched tasks h2h-24 -> h2h-29, medium ==')
def cohort(tool, rnd):
    return {r['task']: r for r in runs if r['host'] == 'mac-a' and r['tool'] == tool and r['round'] == rnd}
cx0, cx1 = cohort('codex-terra-medium', 'h2h-24'), cohort('codex-terra-medium', 'h2h-29')
lp0, lp1 = cohort('loop-default-medium', 'h2h-24'), cohort('loop-default-medium', 'h2h-29')
mc = sorted(set(cx0) & set(cx1))   # each tool is matched on its own task set
ml = sorted(set(lp0) & set(lp1))
print('matched tasks: Codex', len(mc), 'loop', len(ml))
print('Codex median agent wall', S.median(f(cx0[t]['agent_wall_s']) for t in mc), '->', S.median(f(cx1[t]['agent_wall_s']) for t in mc))
print('Codex paired wall ratio', round(S.median(f(cx1[t]['agent_wall_s']) / f(cx0[t]['agent_wall_s']) for t in mc), 3),
      'paired output ratio', round(S.median(f(cx1[t]['output_tokens']) / f(cx0[t]['output_tokens']) for t in mc), 3))
print('Codex output/agent-wall lower bound median', med([f(cx0[t]['output_tokens']) / f(cx0[t]['agent_wall_s']) for t in mc]), '->',
      med([f(cx1[t]['output_tokens']) / f(cx1[t]['agent_wall_s']) for t in mc]))
print('loop paired wall ratio', round(S.median(f(lp1[t]['agent_wall_s']) / f(lp0[t]['agent_wall_s']) for t in ml), 3),
      'paired output ratio', round(S.median(f(lp1[t]['output_tokens']) / f(lp0[t]['output_tokens']) for t in ml), 3))
print('loop body-stream rate median', med([f(lp0[t]['output_tokens']) / f(lp0[t]['body_stream_s']) for t in ml]), '->',
      med([f(lp1[t]['output_tokens']) / f(lp1[t]['body_stream_s']) for t in ml]))
print('example r70-1-go loop medium (output, attempts, provider s, body s, agent s, tok/s):')
for rnd, c in (('h2h-24', lp0), ('h2h-29', lp1)):
    r = c['r70-1-go']
    print(' ', rnd, r['output_tokens'], r['attempts'], r['provider_attempt_wall_s'], r['body_stream_s'], r['agent_wall_s'],
          round(f(r['output_tokens']) / f(r['body_stream_s']), 2))

print('\n== direct SSE probes (3 pairs) ==')
P = [json.loads(l) for l in open(H / 'probes' / 'direct-sse-probes.jsonl') if l.strip()]
for c in ('loop', 'codex'):
    x = [p for p in P if p['client'] == c]
    print(c, 'pooled stream s', round(sum(p['stream_s'] for p in x), 3), 'tok/s', round(sum(p['output'] for p in x) / sum(p['stream_s'] for p in x), 2),
          'median rate', med([p['rate'] for p in x]),
          'median delta->last', med([p['output'] / (p['last_s'] - p['first_delta_s']) for p in x]))

print('\n== sub-route probes (probes/subroute-probes.jsonl), Linux host, loop credential only ==')
R = [json.loads(l) for l in open(H / 'probes' / 'subroute-probes.jsonl') if l.strip()]
ok = [r for r in R if r.get('rate') and not r.get('err')]
for c in 'ABE':
    x = [r for r in ok if r['cand'] == c and r['rep'] >= 1]
    fl = [r['output'] / (r['last_s'] - r['first_s']) for r in x]
    dl = [r['output'] / (r['last_s'] - r['first_delta_s']) for r in x]
    print(c, 'n', len(x), 'first->last median', med(fl), 'first delta->last median', med(dl),
          'time-to-first-delta median', round(S.median(r['first_delta_s'] for r in x), 2))
