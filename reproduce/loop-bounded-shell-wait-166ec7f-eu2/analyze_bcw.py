#!/usr/bin/env python3
"""bcw analysis (model-free). Usage: analyze_bcw.py <round mirror dir> <out dir>
Per cell: hidden pass (result.json all_passed), outcome, agent wall (totals.wall_s), requests, output tokens and list
cost (gateway usage via result totals), retrieval-only requests (turns.md / turns-classify.py definition: every tool call
the response made is a shell call with a handle and no command), handles issued (a new command answered with a running
envelope), handle retrievals, handles never completed. Pairs per (task, rep); pooled sums; registered rules (bcw.md)."""
import json, re, sys, csv, pathlib, collections, statistics
M = pathlib.Path(sys.argv[1]); OUT = pathlib.Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
proto = json.loads((M / 'protocol.json').read_text())
def args_of(c):
    try: return json.loads(c.get('arguments') or '{}')
    except ValueError:
        raw = c.get('arguments') or ''
        return {'handle': 'x'} if raw.lstrip().startswith('{"handle"') else {'command': raw}
def cell_stats(d):
    res = json.loads((d / 'result.json').read_text())
    tot = res.get('totals') or {}
    req = collections.OrderedDict(); n = None; outs = {}
    for line in (d / 'tool-items.jsonl').open():
        x = json.loads(line)
        if 'request' in x: n = x['request']; req.setdefault(n, [])
        elif n is not None and x.get('kind') == 'call': req[n].append(x)
        elif x.get('kind') == 'output': outs[x['call_id']] = x.get('head', '')
    retrieval_only = 0; issued = set(); completed = set(); retrievals = 0; sync_cmds = 0; cmds = 0
    for n, calls in req.items():
        a = [(c, args_of(c)) for c in calls]
        if a and all(c['name'] == 'shell' and x.get('handle') and not x.get('command') for c, x in a): retrieval_only += 1
        for c, x in a:
            if c['name'] != 'shell': continue
            head = outs.get(c['call_id'], '')
            if x.get('handle') and not x.get('command'):
                retrievals += 1
                if '"status":"completed"' in head.replace(' ', '') or head.startswith('{"exit_status"'):
                    m = re.search(r'"handle"\s*:\s*"([0-9a-f]+)', c.get('arguments') or '')
                    if m: completed.add(m.group(1))
            elif x.get('command'):
                cmds += 1
                if head.startswith('exit status'): sync_cmds += 1
                m = re.search(r'"handle"\s*:\s*"([0-9a-f]+)', head)
                if m and '"status":"running"' in head.replace(' ', ''): issued.add(m.group(1))
    return {'passed': bool(res.get('all_passed')), 'outcome': res.get('outcome'), 'wall_s': tot.get('wall_s') or res.get('wall_s'),
            'requests': tot.get('requests'), 'output_tokens': tot.get('output_tokens'), 'reasoning_tokens': tot.get('reasoning_tokens'),
            'usd_list': tot.get('cost_usd'), 'retrieval_only_requests': retrieval_only, 'shell_commands': cmds,
            'commands_returned_completed': sync_cmds, 'handles_issued': len(issued), 'handle_retrievals': retrievals,
            'handles_never_completed': len(issued - completed), 'finished_at_mtime': (d / 'result.json').stat().st_mtime}
rows = []
for c in proto['cells']:
    d = M / c['stratum'] / 'cells' / c['task'] / ('r' + str(c['rep'])) / c['arm']
    if not (d / 'result.json').exists(): rows.append(dict(c, missing=True)); continue
    rows.append(dict(c, **cell_stats(d)))
keys = ['task', 'rep', 'arm', 'passed', 'outcome', 'wall_s', 'requests', 'retrieval_only_requests', 'output_tokens', 'reasoning_tokens', 'usd_list',
        'shell_commands', 'commands_returned_completed', 'handles_issued', 'handle_retrievals', 'handles_never_completed']
with (OUT / 'runs.csv').open('w') as f:
    w = csv.DictWriter(f, fieldnames=keys, extrasaction='ignore'); w.writeheader(); [w.writerow(r) for r in rows if not r.get('missing')]
by = {(r['task'], r['rep'], r['arm']): r for r in rows if not r.get('missing')}
pairs = []
for t in proto['tasks']:
    for rep in sorted({c['rep'] for c in proto['cells']}):
        a, b = by.get((t, rep, 'main')), by.get((t, rep, 'bcw'))
        if a and b:
            pairs.append({'task': t, 'rep': rep, **{k + '_' + s: r[k] for s, r in (('main', a), ('bcw', b)) for k in ('retrieval_only_requests', 'requests', 'wall_s', 'output_tokens', 'passed', 'handles_issued', 'usd_list')}})
def tot(arm, k): return sum((r[k] or 0) for r in rows if not r.get('missing') and r['arm'] == arm and any(p['task'] == r['task'] and p['rep'] == r['rep'] for p in pairs))
pool = {k: {'main': tot('main', k), 'bcw': tot('bcw', k)} for k in ('retrieval_only_requests', 'requests', 'wall_s', 'output_tokens', 'usd_list', 'handles_issued', 'handle_retrievals', 'handles_never_completed', 'shell_commands')}
def frac(k): m = pool[k]['main']; return None if not m else round((pool[k]['bcw'] - m) / m, 4)
higher_ro = sum(p['retrieval_only_requests_bcw'] > p['retrieval_only_requests_main'] for p in pairs)
lower_req = sum(p['requests_bcw'] < p['requests_main'] for p in pairs)
disc = [p for p in pairs if p['passed_main'] != p['passed_bcw']]
false_stop = [p for p in pairs if p['passed_main'] and not p['passed_bcw']]
rules = {
    'primary1_retrieval_only': {'pooled_change': frac('retrieval_only_requests'), 'pairs_higher_on_bcw': higher_ro, 'n_pairs': len(pairs),
                                'met': frac('retrieval_only_requests') is not None and frac('retrieval_only_requests') <= -0.5 and higher_ro <= 1},
    'primary2_requests': {'pooled_change': frac('requests'), 'pairs_lower_on_bcw': lower_req, 'n_pairs': len(pairs),
                          'met': frac('requests') is not None and frac('requests') < 0 and lower_req >= 4},
    'guard_hidden': {'discordant_pairs': [(p['task'], p['rep'], p['passed_main'], p['passed_bcw']) for p in disc], 'main_pass_bcw_fail': len(false_stop), 'held_before_attribution': not false_stop},
    'guard_wall': {'pooled_change': frac('wall_s'), 'held': frac('wall_s') is not None and frac('wall_s') <= 0.15},
}
last = max((r['finished_at_mtime'] for r in rows if not r.get('missing')), default=None)
import datetime
an = {'protocol_id': proto['id'], 'cells_done': sum(not r.get('missing') for r in rows), 'cells_planned': len(proto['cells']), 'pairs': pairs, 'pooled': pool,
      'rules': rules, 'last_cell_result_mtime_utc': datetime.datetime.fromtimestamp(last, datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ') if last else None,
      'pass_by_arm_task': {f'{t}/{a}': f"{sum(by[(t, r, a)]['passed'] for r in (1, 2, 3) if (t, r, a) in by)}/{sum((t, r, a) in by for r in (1, 2, 3))}" for t in proto['tasks'] for a in ('main', 'bcw')}}
(OUT / 'analysis.json').write_text(json.dumps(an, indent=1, sort_keys=True) + '\n')
print(json.dumps({k: an[k] for k in ('cells_done', 'cells_planned', 'pooled', 'rules', 'pass_by_arm_task', 'last_cell_result_mtime_utc')}, indent=1))
for p in pairs: print(p['task'], p['rep'], 'RO', p['retrieval_only_requests_main'], '->', p['retrieval_only_requests_bcw'], 'req', p['requests_main'], '->', p['requests_bcw'], 'wall', p['wall_s_main'], '->', p['wall_s_bcw'], 'pass', p['passed_main'], p['passed_bcw'])
