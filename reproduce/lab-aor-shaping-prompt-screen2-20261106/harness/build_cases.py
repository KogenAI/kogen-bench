import json, glob, re
base = 'work/s1cells' if False else '.'
cases = []
refusals = {}
for f in sorted(glob.glob('s1cells/*/cells/*/*/*/shaping-events.ndjson')):
    cell = f.split('/cells/')[1].rsplit('/', 1)[0]; d = f.rsplit('/', 1)[0]
    evs = [json.loads(l) for l in open(f)]
    ref = [e for e in evs if e.get('event') == 'submission_refused' and e['gate'] == 'decision_check']
    dcs = [e for e in evs if e.get('event') == 'decision_check']
    for i, e in enumerate(dcs):
        items = e['items']
        quotes = [q for it in items for q in it.get('request_quotes', [])]
        cases.append(dict(id=f'{cell}#dc{i+1}', cell=cell, gate='decision_check', items=items, request=' '.join(quotes), intent='\n'.join(it['statement'] for it in items),
                          recorded=(len(ref[i]['problems']) - 1) if i < len(ref) else 0))
    # readiness/evidence rule cases from the final intent
    t = open(d + '/intent/intent.md').read().split('\n')
    acc = []; sec = None
    for l in t:
        if l.startswith('Acceptance:'): sec = 'a'; continue
        if sec == 'a':
            if l.startswith('- '): acc.append(l[2:].strip()); continue
            if l.strip() == '': 
                if acc: sec = None
                continue
            sec = None
    feas = [l for l in t if l.startswith('- evidence: {')]
    if feas: cases.append(dict(id=f'{cell}#evidence', cell=cell, gate='evidence_rule', feasibility=feas, acceptance=acc))
json.dump(cases, open('replay/cases.json', 'w'), indent=1)
print(len(cases), 'cases;', sum(1 for c in cases if c['gate'] == 'decision_check'), 'decision-check events;', sum(1 for c in cases if c['gate'] == 'evidence_rule'), 'evidence-rule cells')
