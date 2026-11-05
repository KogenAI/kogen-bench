#!/usr/bin/env python3
"""L4 step 0: projected critical path per repo and host class, by the rule registered in the Lab record. usage: l4_model.py <data dir>"""
import json, os, sys
D = sys.argv[1]
L = lambda n: json.load(open(os.path.join(D, n)))
walls, steps, counts, pkgs = L('suite_walls.json'), L('adoption_steps.json'), L('static_counts.json'), L('package_times.json')
BUDGET = {'kogen': 60, 'kogen-loop': 10, 'kogen-build': 60, 'kogen-shaping': 45}
budget = lambda r: BUDGET.get(r, 20)
step = lambda lab, name: next(s['median_s'] for s in steps if s['label'] == lab and s['step'] == name)
# Priced savings (rule (a)): packaging charged once: (8-1) x setup step; builds charged once: (12-1) x build step. N from the request. kogen only.
priced = {'kogen': {'packaging_once': (8 - 1) * step('final', 'setup'), 'builds_once': (12 - 1) * step('final', 'build')}}
# Rule (b): REL tests with a stated wall that are not t.Parallel. The three named waits are t.Parallel (source), so they are floors, not savings.
floors = [dict(repo='kogen', item='approve deadline split/hung CLI tests (REL)', stated_wall_s=130, parallel=True, saves_s=0),
          dict(repo='kogen', item='silent-shell scenario sleep 47 (REL), cucumber --parallel 4', stated_wall_s=47, parallel=True, saves_s=0)]
cnt = {c['repo']: c for c in counts}
rows = []
for w in walls:
    if w['n'] < 3 or w['host_class'] not in ('macbook', 'linux-a', 'linux-2core', 'mac-studio'): continue
    r = w['repo']
    if r not in cnt: continue
    sav = sum(priced.get(r, {}).values())
    proj = max(0, w['median_s'] - sav)
    c = cnt[r]; nonpar = 1 - min(1, c['parallel_calls'] / c['tests'])
    ideal = round(w['median_s'] / 4, 1) if nonpar >= 0.9 else None
    rows.append(dict(repo=r, host_class=w['host_class'], runs=w['n'], median_s=w['median_s'], p90_s=w['p90_s'], budget_s=budget(r), priced_savings_s=sav,
                     projected_s=proj, within_budget=proj <= budget(r), gap_s=max(0, proj - budget(r)), required_factor=round(w['median_s'] / budget(r), 1),
                     tests=c['tests'], parallel_calls=c['parallel_calls'], serial_only_ideal_4core_s=ideal))
verdict = 'yes' if all(x['within_budget'] for x in rows if x['host_class'] in ('macbook', 'linux-a')) else 'unresolved'
json.dump(dict(rows=rows, floors=floors, priced=priced, verdict=verdict), open(os.path.join(D, 'l4.json'), 'w'), indent=1)
print('repo | host | n | median | p90 | budget | savings | projected | gap | need x | ideal 4-core (non-parallel repos)')
for x in sorted(rows, key=lambda x: (x['repo'], x['host_class'])):
    print(f"{x['repo']:19}|{x['host_class']:12}|{x['runs']:4}|{x['median_s']:6.0f}|{x['p90_s']:6.0f}|{x['budget_s']:4}|{x['priced_savings_s']:4.0f}|{x['projected_s']:6.0f}|{x['gap_s']:6.0f}|{x['required_factor']:5}|{x['serial_only_ideal_4core_s']}")
print(verdict)
