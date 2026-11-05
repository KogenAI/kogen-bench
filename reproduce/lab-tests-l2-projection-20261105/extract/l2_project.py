#!/usr/bin/env python3
"""L2 step 0 (model-free): apply the behaviour projection to the recorded diff keys of the red TestBuildRequestBudgetOff windows.
usage: l2_project.py <land log dir> <classified-landred.tsv> <out dir>"""
import csv, json, os, re, sys
land, cls, out = sys.argv[1:4]
PAIR = re.compile(r'"([a-z_0-9]+)":(\[[^\]]*\]|"[^"]*"|[^,}\]]+)')
INSIDE_EXACT = {'exit', 'exit_code', 'outcome', 'stop_code', 'reason', 'phase', 'stopped_phase', 'commits', 'parent', 'tree', 'title'}
def inside(key):
    return key in INSIDE_EXACT or 'budget' in key
def diff_keys(a, b):
    pa, pb = PAIR.findall(a), PAIR.findall(b)
    da, db = dict(pa), dict(pb)
    return [(k, da.get(k), db.get(k)) for k in dict.fromkeys(list(da) + list(db)) if da.get(k) != db.get(k) and k not in ('at', 'timestamp')]
rows = {r['land_log']: r for r in csv.DictReader(open(cls), delimiter='\t')}
logs = sorted(f for f in os.listdir(land) if f.endswith('.log') and
              (re.search(r'BudgetOff|build_request_budget', open(os.path.join(land, f), errors='replace').read()) or
               (f in rows and 'BudgetOff' in rows[f]['failing_test'] + rows[f]['real_cause'])))
CAUSE = [(r'request_offset_ms', 'request_offset_ms'), (r'load_average', 'load_average'), (r"step_sweep 'ms'|'ms':", 'ms'),
         (r'probe status timed_out vs ok|probe timed_out vs ok|toolchain-probe diff|mix-probe flake', 'status')]
res = []
for i, f in enumerate(logs, 1):
    txt = open(os.path.join(land, f), errors='replace').read().splitlines()
    key, src, ev, vals, lineat = None, None, None, None, None
    for j, l in enumerate(txt):
        m = re.search(r'log line (\d+) differs at byte (\d+)', l)
        if m and not lineat: lineat = (int(m.group(1)), int(m.group(2)))
        if l.strip().startswith('omitted:') and j + 1 < len(txt) and txt[j + 1].strip().startswith('zero:'):
            d = diff_keys(l.split('omitted:', 1)[1], txt[j + 1].split('zero:', 1)[1])
            if d:
                key, vals, src = d[0][0], f'{d[0][1]} vs {d[0][2]}', 'log diff lines'
                em = re.search(r'"event":"([a-z_]+)"', l)
                ev = em.group(1) if em else None
                break
    r = rows.get(f)
    if key is None and r:
        t = r['failing_test'] + ' ' + r['real_cause']
        for pat, k in CAUSE:
            if re.search(pat, t):
                key, src = k, 'classified cause text'
                break
    first = re.search(r'^== (\S+) onto (\S+) main (\w+)', txt[0]) if txt else None
    res.append(dict(window=f'W{i:02d}', log=f, producer=first.group(2) if first else (r or {}).get('repo'),
                    producer_main=first.group(3) if first else None, key=key, key_source=src or 'unrecorded',
                    values=vals, event=ev, line_byte=lineat,
                    inside_projection=(inside(key) if key else None)))
ctrl = {'build_request_budget': inside('build_request_budget'), 'outcome': inside('outcome'), 'commits': inside('commits'),
        'request_offset_ms': inside('request_offset_ms'), 'load_average': inside('load_average'), 'ms': inside('ms'), 'status': inside('status')}
rec = [x for x in res if x['key']]
verdict = ('no' if any(x['inside_projection'] for x in rec) else
           'yes' if len(rec) >= 8 and ctrl['build_request_budget'] else 'unresolved')
os.makedirs(out, exist_ok=True)
json.dump(dict(windows_found=len(res), windows_reported=14, windows_with_key=len(rec), rows=res, controls=ctrl, verdict=verdict), open(os.path.join(out, 'l2.json'), 'w'), indent=1)
fo = open(os.path.join(out, 'l2.tsv'), 'w'); w = csv.writer(fo, delimiter='\t')
w.writerow(['window', 'producer', 'producer_main', 'key', 'key_source', 'values', 'line_byte', 'inside_projection'])
for x in res: w.writerow([x[k] for k in ['window', 'producer', 'producer_main', 'key', 'key_source', 'values', 'line_byte', 'inside_projection']])
fo.close()
print(open(os.path.join(out, 'l2.tsv')).read()); print('controls', ctrl); print('found', len(res), 'with key', len(rec), 'verdict', verdict)
