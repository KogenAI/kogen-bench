#!/usr/bin/env python3
"""Phase 3 stage A, replay (a): arms 2 and 3 over the phase 1-2 cells. Usage: analyze3.py cells/*
Ground truth per cell: forced /compact turns (events.jsonl kind=compact, rc 0) and hooks.jsonl firings.
-p cells: arm 2 evidence = summaries.jsonl (extract.py copied them from the session transcript's
isCompactSummary entries); arm 3 = per-call usage.iterations of the turn results.
live cells: live.stream.jsonl carries compact_boundary and per-message usage (same format as the on-disk jsonl)."""
import json, os, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import detect3

def jl(p):
    return [json.loads(l) for l in open(p)] if os.path.exists(p) else []

tot = {}
def add(k, v): tot[k] = tot.get(k, 0) + v

rows = []
for cell in sorted(sys.argv[1:]):
    ev = jl(f'{cell}/events.jsonl')
    ncomp = sum(1 for e in ev if e.get('kind') == 'compact' and e.get('rc') == 0)
    nhook = sum(1 for h in jl(f'{cell}/hooks.jsonl') if h.get('source') == 'compact')
    nsum = len(jl(f'{cell}/summaries.jsonl'))
    live = os.path.exists(f'{cell}/live.stream.jsonl')
    if live:
        evs = detect3.events_claude(open(f'{cell}/live.stream.jsonl').readlines())
        kind = 'live'
        # live cells are one process: truth = compact_boundary entries
        truth = sum(1 for k, v in evs if k == 'compact' and v == 'compact_boundary')
    else:
        evs = []
        for e in ev:
            f = f'{cell}/turns/{e["file"]}'
            if not os.path.exists(f): continue
            if e['kind'] == 'compact':
                evs.append(('compact', 'summary'))
                continue
            try: d = json.load(open(f))
            except Exception: continue
            for it in (d.get('usage') or {}).get('iterations') or []:
                if it.get('type') == 'message':
                    c = detect3.ctx_claude(it)
                    if c: evs.append(('call', c))
        kind = 'turns'
        truth = ncomp
    s = detect3.score(evs)
    s.update(cell=cell.split('/')[-1], kind=kind, truth_forced=ncomp, hook_firings=nhook, transcript_summaries=nsum, truth_used=truth)
    rows.append(s)
    for k in ('calls', 'compactions', 'arm3_hits', 'arm3_false_alarms', 'arm3_miss_nodrop', 'arm3_unobservable'):
        add(f'{kind}.{k}', s[k])
    add(f'{kind}.truth', truth); add(f'{kind}.hook', nhook); add(f'{kind}.summaries', nsum)
    add(f'{kind}.arm2_hits', s['arm2_hits'])
    add(f'{kind}.cells', 1)
for r in rows:
    print(r['cell'], r['kind'], 'forced', r['truth_forced'], 'hook', r['hook_firings'], 'summ', r['transcript_summaries'], 'calls', r['calls'],
          'comp', r['compactions'], 'a3hit', r['arm3_hits'], 'a3miss', r['arm3_miss_nodrop'], 'a3fa', r['arm3_false_alarms'])
print(json.dumps(tot, indent=1, sort_keys=True))
