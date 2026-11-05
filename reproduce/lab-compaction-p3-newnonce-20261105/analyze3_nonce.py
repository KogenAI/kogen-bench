#!/usr/bin/env python3
"""Stage B scoring for arm 1 (mode newnonce). usage: analyze3_nonce.py <cell dirs>
Per forced /compact (events.jsonl kind=compact): hit = the first studio_note after it carries a changed nonce
(calls.jsonl signal changed-fresh; changed-reused is reported apart and counts as a hit only for 'changed').
Later calls in the same compaction window that change again, and any change in a window with no compaction,
are false alarms. Hook firings (hooks.jsonl) are the paired reference. Missing nonce = non-compliance."""
import json, os, sys
tot = dict(compactions=0, hook=0, hit=0, hit_fresh=0, missing_first=0, notes=0, steady_notes=0, false_alarms=0, missing=0)
for d in sys.argv[1:]:
    jl = lambda n: [json.loads(l) for l in open(os.path.join(d, n))] if os.path.exists(os.path.join(d, n)) else []
    ev = [e for e in jl('events.jsonl') if e.get('rc') == 0]
    notes = [c for c in jl('calls.jsonl') if c.get('tool') == 'studio_note']
    comp_t = sorted(e['t1'] for e in ev if e['kind'] == 'compact')
    tot['hook'] += len([h for h in jl('hooks.jsonl') if h.get('source') == 'compact'])
    tot['notes'] += len(notes); tot['missing'] += sum(1 for n in notes if n.get('signal') == 'missing')
    seen_first = set()
    for n in notes:
        k = sum(1 for t in comp_t if t < n['t'])   # compactions before this note
        first = k > 0 and k not in seen_first
        if first:
            seen_first.add(k)
            tot['compactions'] += 0
            if n.get('detected') and n.get('signal') != 'missing': tot['hit'] += 1; tot['hit_fresh'] += n.get('signal') == 'changed-fresh'
            if n.get('signal') == 'missing': tot['missing_first'] += 1
        else:
            if k == 0: tot['steady_notes'] += 1
            if n.get('detected') and n.get('signal') != 'missing': tot['false_alarms'] += 1
    tot['compactions'] += len(comp_t)
print(json.dumps(tot))
