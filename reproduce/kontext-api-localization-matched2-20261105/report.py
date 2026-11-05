"""report_prescreen.py results.jsonl: tables for the kontext-matched-2 API packet-only pre-screen (stdlib only).
Arm A = issue + bounded failure; arm B = A + frozen packet. Recall/precision/first-hit are scored model-free against reference.patch files.
'source' columns drop documentation-only reference files (CHANGELOG*, README*, *.md) that neither arm can be expected to name."""
import json, sys, statistics as st, collections, re
rows = [json.loads(l) for l in open(sys.argv[1])]
ok = [r for r in rows if 'error' not in r]
def src(ref): return [f for f in ref if not re.search(r'(^|/)(CHANGELOG|README)[^/]*$|\.md$', f)]
def score(r, only_src):
    ref = src(r['reference']) if only_src else r['reference']
    if not ref: return None
    hit = [f for f in r['files'] if f in ref]
    return dict(recall=len(set(hit)) / len(ref), first=bool(r['files']) and r['files'][0] in ref,
                rank=next((i + 1 for i, f in enumerate(r['files']) if f in ref), None))
cases = list(dict.fromkeys(r['case'] for r in rows))
out = {'calls': len(rows), 'errors': len(rows) - len(ok), 'cost_usd': round(sum(r.get('cost', 0) for r in ok), 4), 'arms': {}, 'cases': {}}
print('| arm | calls | mean recall (all ref files) | mean recall (source ref files) | first file correct (source) | mean input tokens | list cost |\n|---|---|---|---|---|---|---|')
for arm in 'AB':
    rs = [r for r in ok if r['arm'] == arm]
    a = [score(r, False) for r in rs]; s = [x for x in (score(r, True) for r in rs) if x]
    u = [r['usage']['input'] + r['usage']['write'] + r['usage']['read'] for r in rs]
    d = dict(calls=len(rs), recall_all=round(st.mean(x['recall'] for x in a), 3), recall_source=round(st.mean(x['recall'] for x in s), 3),
             first_source=sum(x['first'] for x in s), n_source=len(s), input_tokens=round(st.mean(u)), cost=round(sum(r['cost'] for r in rs), 4))
    out['arms'][arm] = d
    print(f"| {arm} | {d['calls']} | {d['recall_all']} | {d['recall_source']} | {d['first_source']}/{d['n_source']} | {d['input_tokens']} | USD {d['cost']} |")
print('\n| case | arm | source recall per rep | first-hit rank per rep | packet bytes |\n|---|---|---|---|---|')
paired = []
for c in cases:
    m = {}
    for arm in 'AB':
        rs = sorted([r for r in ok if r['case'] == c and r['arm'] == arm], key=lambda r: r['rep'])
        sc = [score(r, True) or score(r, False) for r in rs]
        m[arm] = st.mean(x['recall'] for x in sc) if sc else None
        pb = next((r['packet_bytes'] for r in rs), 0) if arm == 'B' else 0
        print(f"| {c} | {arm} | {', '.join(f'{x['recall']:.2f}' for x in sc)} | {', '.join(str(x['rank']) for x in sc)} | {pb or ''} |")
    out['cases'][c] = dict(A=m['A'], B=m['B'], delta=None if None in m.values() else round(m['B'] - m['A'], 3))
    if out['cases'][c]['delta'] is not None: paired.append(out['cases'][c]['delta'])
print(f"\npaired per-case change in mean source recall (B - A): up {sum(d > 0 for d in paired)}, same {sum(d == 0 for d in paired)}, down {sum(d < 0 for d in paired)} of {len(paired)} cases")
out['paired'] = dict(up=sum(d > 0 for d in paired), same=sum(d == 0 for d in paired), down=sum(d < 0 for d in paired), n=len(paired))
json.dump(out, open('prescreen-summary.json', 'w'), indent=1)
