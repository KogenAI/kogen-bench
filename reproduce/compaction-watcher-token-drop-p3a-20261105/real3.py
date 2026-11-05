#!/usr/bin/env python3
"""Phase 3 stage A (b): replay arms 2 and 3 over real sessions on this Mac, read in place, read-only.
Prints AGGREGATE counts only (no paths, no session ids, no text). usage: real3.py   (python3 -I)
Claude Code: ~/.claude/projects/*/*.jsonl, main chain only (sidechain entries and subagent files skipped).
Codex: sessions/**/rollout*.jsonl under every ~/.codex* home that exists.
Dedupe: a compaction is counted once by its compact_boundary uuid (Claude; resumed/forked files replay old entries).
A compaction at the very start of a file (no earlier model call in that file) has no baseline for arm 3: 'no_baseline'."""
import glob, json, os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import detect3
H = os.path.expanduser('~')
res = {}
def agg(name):
    return res.setdefault(name, collections.Counter())
# ---- Claude
seen = set()
for f in glob.glob(f'{H}/.claude/projects/*/*.jsonl'):
    a = agg('claude')
    lines = open(f, errors='replace').readlines()
    ev = detect3.events_claude(lines)
    # uuids of boundaries in file order, to dedupe replays
    uu = []
    for l in lines:
        if 'compact_boundary' in l:
            try: d = json.loads(l)
            except Exception: continue
            if d.get('type') == 'system' and d.get('subtype') == 'compact_boundary' and not d.get('isSidechain'):
                uu.append((d.get('uuid'), (d.get('compactMetadata') or {}).get('trigger')))
    s = detect3.score(ev)
    a['files'] += 1; a['calls'] += s['calls']
    # classify per compaction: new vs replay-duplicate
    new = [u for u in uu if u[0] not in seen]
    for u in uu: seen.add(u[0])
    a['compactions_unique'] += len(new); a['compactions_replayed_copy'] += len(uu) - len(new)
    for u in new: a['trigger_' + str(u[1])] += 1
    nb = sum(1 for m in s['missed_detail'] if m[1] == 0)   # compaction before any call in this file
    a['arm3_hits'] += s['arm3_hits']; a['arm3_no_baseline_misses'] += nb
    a['arm3_other_misses'] += s['arm3_miss_nodrop'] - nb
    a['arm3_false_alarm_events'] += s['arm3_false_alarms']
# ---- Codex
for home in sorted(os.path.basename(x) for x in glob.glob(f'{H}/.codex*') if os.path.isdir(x)):
    fs = glob.glob(f'{H}/{home}/sessions/**/rollout*.jsonl', recursive=True)
    if not fs: continue
    a = agg('codex')
    for f in fs:
        s = detect3.score(detect3.events_codex(open(f, errors='replace').readlines()))
        a['files'] += 1; a['calls'] += s['calls']; a['compactions_unique'] += s['compactions']
        a['arm3_hits'] += s['arm3_hits']; a['arm3_other_misses'] += s['arm3_miss_nodrop']
        a['arm3_false_alarm_events'] += s['arm3_false_alarms']
out = {}
for k, a in res.items():
    d = dict(a); d['false_alarms_per_100_calls_arm3'] = round(100 * a['arm3_false_alarm_events'] / max(1, a['calls']), 4)
    d['arm2_false_alarms'] = 0   # arm 2 fires only on a compaction entry; see README for the definition
    out[k] = d
print(json.dumps(out, indent=1, sort_keys=True))
