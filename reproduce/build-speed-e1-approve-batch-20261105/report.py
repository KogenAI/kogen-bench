#!/usr/bin/env python3
"""Recompute the E1 summary from data/results.json: per-fixture approve wall medians per arm, the cut against
arm A, verdict identity against arm A, and the success rule (B and C identical on 15/15, 3/3 collisions caught,
median cut >= 90% for B and >= 45% for C over the 10 trees)."""
import json, os, statistics as st
d = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'results.json')))
F = d['fixtures']
trees = [f for f in F if f['kind'] not in ('negative', 'worktree')]
negs = [f for f in F if f['kind'] == 'negative']
print('fixture | kind | A s | B med s | C med s | B+C med s | cut B/C/B+C % | identical B/C/B+C')
for f in F:
    m, c, i = f['median_s'], f['cut_pct'], f['identical']
    print(f"{f['fixture']} | {f['kind']} | {m['A']} | {m['B']} | {m['C']} | {m['BC']} | {c['B']}/{c['C']}/{c['BC']} | {i['B']}/{i['C']}/{i['BC']}")
for arm in ('B', 'C', 'BC'):
    fs = [f for f in trees if f['median_s']['A'] is not None and f['median_s'][arm] is not None]
    sa = sum(f['median_s']['A'] for f in fs); sx = sum(f['median_s'][arm] for f in fs)
    cuts = sorted(f['cut_pct'][arm] for f in fs)
    print(f"{arm}: {len(fs)} trees with A and {arm}; pooled cut {100 * (1 - sx / sa):.1f}% (A {sa:.0f} s, {arm} {sx:.0f} s); per-tree cut median {st.median(cuts):.1f}%, min {cuts[0]:.1f}%, max {cuts[-1]:.1f}%; trees >= {90 if arm != 'C' else 45}%: {sum(c >= (90 if arm != 'C' else 45) for c in cuts)}/{len(fs)}")
for arm in ('B', 'C', 'BC'):
    bi = [f['binding_identical'][arm] for f in F if f['binding_identical'][arm] is not None]
    fi = [f['identical'][arm] for f in F if f['identical'][arm] is not None]
    print(f"{arm}: step-binding verdict identical to A on {sum(bi)}/{len(bi)} fixtures; final verdict identical on {sum(fi)}/{len(fi)}")
for arm in ('A', 'B', 'C', 'BC'):
    ran = [f for f in negs if any(r['fixture'] == f['fixture'] and r['arm'] == arm for r in d['runs'])]
    caught = sum(1 for f in ran if all('step_ownership_collision' in (r['verdict'] or '') for r in d['runs'] if r['fixture'] == f['fixture'] and r['arm'] == arm))
    print(f"collisions caught, {arm}: {caught}/{len(ran)} negatives run (of {len(negs)})")
