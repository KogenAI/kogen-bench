#!/usr/bin/env python3
"""wmap analysis (model-free). Usage: analyze_wmap.py <round mirror dir> <out dir> [base_arm wmap_arm]
Per cell: hidden pass (result.json all_passed), outcome, agent wall, requests, input/output tokens, list cost, request-1
input tokens (lever fires), and orientation-only requests before the first edit. Attribution: events.jsonl gives
response n and the tool.call events after it; tool-items.jsonl gives the call arguments by call_id (its {"request": n}
markers come before the calls of response n-1, which turns-classify.py misread). Class per response: edit
(write/apply_patch or a writing shell command) > finish > verify (go test/build/vet, npm, make, ...) > orientation (every
call is read_file/list_files/search_text or a read-only ls/cat/pwd/head/tail/sed -n/rg/grep/find/git status|diff|log|show
shell) > other. Pairs per (task, rep); registered rules (notes-harness/loopclimb/wmap.md)."""
import json, re, sys, csv, pathlib, collections
M = pathlib.Path(sys.argv[1]); OUT = pathlib.Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
BASE, LEV = (sys.argv[3], sys.argv[4]) if len(sys.argv) > 4 else ('base', 'wmap')
EDIT = re.compile(r'(?i)(<<[-~]?\s*[\'"]?\w+|\bapply_patch\b|\bpatch\s|\bsed\s+-i\b|\bgofmt\s+-w\b|(?:^|[;&\n])\s*(?:cp|mv|touch|mkdir|rm)\s|(?<![<>=])>{1,2}\s*[^&/])')
VERIFY = re.compile(r'\b(go\s+(?:test|build|vet)|npm\s|npx\s|make\s|pytest|gofmt\b)')
READSH = re.compile(r'^\s*(?:ls|cat|pwd|head|tail|sed\s+-n|rg|grep|find|git\s+(?:status|diff|log|show))\b')
def classify(calls):
    if not calls: return 'nocall'
    names = [c['name'] for c in calls]; s = '\n'.join(str(c['args'].get('command', '')) for c in calls)
    if any(n in ('write_file', 'apply_patch', 'edit_file') for n in names) or EDIT.search(s): return 'edit'
    if 'finish' in names: return 'finish'
    if VERIFY.search(s): return 'verify'
    if all(c['name'] in ('read_file', 'list_files', 'search_text') or (c['name'] == 'shell' and READSH.match(str(c['args'].get('command', '')))) for c in calls): return 'orient'
    return 'other'
def cell(d):
    args = {}
    for l in (d / 'tool-items.jsonl').open():
        x = json.loads(l)
        if x.get('kind') == 'call':
            try: a = json.loads(x.get('arguments') or '{}')
            except ValueError: a = {'command': x.get('arguments', '')}
            args[x['call_id']] = a if isinstance(a, dict) else {}
    resp = []; cur = None
    for l in (d / 'events.jsonl').open():
        x = json.loads(l)
        if x.get('type') == 'response': cur = {'n': x['n'], 'u': x.get('usage') or {}, 'calls': []}; resp.append(cur)
        elif x.get('type') == 'tool.call' and cur is not None: cur['calls'].append({'name': x['name'], 'args': args.get(x['call_id'], {})})
    pre = []
    for r in resp:
        r['cls'] = classify(r['calls'])
    for r in resp:
        if r['cls'] == 'edit': break
        pre.append(r)
    res = json.loads((d / 'result.json').read_text()); tot = res.get('totals') or {}
    listing_pre = sum(1 for r in pre for c in r['calls'] if c['name'] == 'list_files' and not c['args'].get('path'))
    return {'requests': len(resp), 'orient_pre': sum(r['cls'] == 'orient' for r in pre), 'pre_edit': len(pre),
            'pre_classes': ' '.join(r['cls'] for r in pre), 'root_list_files_pre': listing_pre,
            'req1_input': (resp[0]['u'].get('input') if resp else None),
            'input': tot.get('input_tokens'), 'output': tot.get('output_tokens'), 'usd': tot.get('cost_usd'),
            'wall': tot.get('wall_s'), 'passed': res.get('all_passed'), 'outcome': res.get('outcome'),
            'edited': any(r['cls'] == 'edit' for r in resp)}
rows = []
for d in sorted(M.glob('counted/cells/*/r*/*')):
    if not (d / 'result.json').exists() or not (d / 'events.jsonl').exists(): continue
    r = cell(d); r.update(task=d.parts[-3], rep=d.parts[-2], arm=d.parts[-1]); rows.append(r)
by = {(r['task'], r['rep'], r['arm']): r for r in rows}
pairs = []
for (t, rep, a), r in sorted(by.items()):
    if a != BASE or (t, rep, LEV) not in by: continue
    pairs.append((t, rep, r, by[(t, rep, LEV)]))
fires = {}
for t, rep, b, w in pairs:
    if b['req1_input'] and w['req1_input']: fires.setdefault(t, []).append(w['req1_input'] - b['req1_input'])
fired = {t for t, v in fires.items() if min(v) > 500}
def S(key, arm_i, sel=lambda t: True): return sum((p[arm_i][key] or 0) for p in pairs if sel(p[0]))
tot = {k: {BASE: S(k, 2), LEV: S(k, 3)} for k in ('orient_pre', 'requests', 'input', 'output', 'usd', 'wall')}
fire_tot = {k: {BASE: S(k, 2, lambda t: t in fired), LEV: S(k, 3, lambda t: t in fired)} for k in ('orient_pre', 'requests', 'input', 'output', 'wall')}
nofire_tot = {k: {BASE: S(k, 2, lambda t: t not in fired), LEV: S(k, 3, lambda t: t not in fired)} for k in ('orient_pre', 'requests', 'input', 'output', 'wall')}
disc = [(t, rep, b['passed'], w['passed']) for t, rep, b, w in pairs if bool(b['passed']) != bool(w['passed'])]
red = 1 - tot['orient_pre'][LEV] / tot['orient_pre'][BASE] if tot['orient_pre'][BASE] else None
rules = {
    'orientation_fall_ge_50pct': red is not None and red >= 0.5,
    'hidden_pass_not_worse_raw': sum(1 for x in disc if x[2] and not x[3]) <= sum(1 for x in disc if x[3] and not x[2]),
    'input_not_up_on_fired_tasks': fire_tot['input'][LEV] <= fire_tot['input'][BASE],
    'output_not_up_on_fired_tasks': fire_tot['output'][LEV] <= fire_tot['output'][BASE],
}
summary = {'arms': [BASE, LEV], 'pairs': len(pairs), 'cells': len(rows), 'fired_tasks': sorted(fired),
           'req1_input_delta_by_task': fires, 'totals': tot, 'fired_totals': fire_tot, 'nofire_totals': nofire_tot,
           'orientation_reduction': red, 'discordant_pass_pairs': disc,
           'hidden_pass': {BASE: sum(bool(p[2]['passed']) for p in pairs), LEV: sum(bool(p[3]['passed']) for p in pairs)},
           'pairs_fewer_requests': sum(p[3]['requests'] < p[2]['requests'] for p in pairs),
           'pairs_more_requests': sum(p[3]['requests'] > p[2]['requests'] for p in pairs),
           'lever_cells_with_root_list_files_pre': [(t, rep) for t, rep, b, w in pairs if t in fired and w['root_list_files_pre']],
           'rules_before_attribution': rules}
(OUT / 'analysis.json').write_text(json.dumps(summary, indent=1, default=str))
with (OUT / 'cells.csv').open('w', newline='') as f:
    k = ['task', 'rep', 'arm', 'passed', 'outcome', 'requests', 'orient_pre', 'pre_edit', 'pre_classes', 'root_list_files_pre', 'req1_input', 'input', 'output', 'usd', 'wall', 'edited']
    w = csv.DictWriter(f, fieldnames=k, extrasaction='ignore'); w.writeheader(); [w.writerow(r) for r in rows]
print(json.dumps({k: summary[k] for k in ('pairs', 'fired_tasks', 'orientation_reduction', 'hidden_pass', 'discordant_pass_pairs', 'pairs_fewer_requests', 'pairs_more_requests', 'rules_before_attribution')}, default=str))
print(json.dumps({'totals': tot, 'fired': fire_tot, 'nofire': nofire_tot}, default=str))
