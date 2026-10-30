"""Recompute the numbers of the api-patch-screen-2nd-host finding from runs.csv and excluded.csv.
usage: python3 analyze.py   (standard library only)
Per arm: passes, median wall, median USD per passing cell. Per task: candidate minus speed2 (wall, USD).
Spend: counted cells + charged-but-excluded attempts. Lower wall / USD is better."""
import csv, statistics as S, pathlib

H = pathlib.Path(__file__).resolve().parent
rows = list(csv.DictReader(open(H / 'runs.csv')))
ex = list(csv.DictReader(open(H / 'excluded.csv')))
ARMS = ['speed2', 'api-replay', 'api-batch', 'api-answer-end']
f = float
assert all(r['all_models_match'] == 'true' and r['usage_complete'] == 'true' for r in rows), 'identity/usage gate'

print('arm              passes  median wall s  median USD/pass')
for a in ARMS:
    x = [r for r in rows if r['tool'] == a]
    p = [r for r in x if r['passed'] == 'true']
    print('%-16s %d/%d    %-13.3f  $%.6f' % (a, len(p), len(x), S.median(f(r['wall_s']) for r in p), S.median(f(r['cost_usd']) for r in p)))

by = {(r['task'], r['tool']): r for r in rows}
print('\ncandidate minus speed2 (wall s / USD):')
for t in ['cron-go', 'vm-go', 'artifact-go', 'readtime-go']:
    out = []
    for a in ARMS[1:]:
        c, b = by[(t, a)], by[(t, 'speed2')]
        out.append('%s %+.3f s / %+.6f' % (a, f(c['wall_s']) - f(b['wall_s']), f(c['cost_usd']) - f(b['cost_usd'])))
    print('%-12s' % t, ' | '.join(out))

counted = sum(f(r['cost_usd']) for r in rows)
excluded = sum(f(r['cost_usd']) for r in ex)
print('\ncounted cells cost  $%.8f' % counted)
print('charged, excluded   $%.8f' % excluded)
print('total experiment    $%.8f of $3.00 cap' % (counted + excluded))
