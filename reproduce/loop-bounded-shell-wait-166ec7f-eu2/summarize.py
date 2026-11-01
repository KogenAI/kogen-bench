#!/usr/bin/env python3
"""summarize.py runs.csv: the README tables. A pair is censored when a cell has no complete provider usage
(output_tokens empty: the gateway's identity/usage gate stopped it); censored pairs are listed and left out of the pooled
primary readouts, as registered (no replacement)."""
import csv, sys, collections
rows = list(csv.DictReader(open(sys.argv[1])))
cell = {(r['task'], r['rep'], r['arm']): r for r in rows}
pairs = sorted({(r['task'], r['rep']) for r in rows})
cens = [p for p in pairs if any(cell[p + (a,)]['output_tokens'] == '' for a in ('main', 'bcw'))]
f = lambda x: float(x) if x else 0.0
print('pair | retrieval-only main->bcw | requests | wall s | output tokens | hidden pass main/bcw | handles main/bcw')
for p in pairs:
    m, b = cell[p + ('main',)], cell[p + ('bcw',)]
    print(f"{p[0]} r{p[1]}{' (censored: ' + m['outcome'] + ' on main)' if p in cens else ''} | {m['retrieval_only_requests']}->{b['retrieval_only_requests']} | {m['requests']}->{b['requests']} | {f(m['wall_s']):.0f}->{f(b['wall_s']):.0f} | {m['output_tokens'] or '-'}->{b['output_tokens'] or '-'} | {m['passed']}/{b['passed']} | {m['handles_issued']}/{b['handles_issued']}")
keep = [p for p in pairs if p not in cens]
print(f'\npooled over {len(keep)} complete pairs (censored left out: {len(cens)})')
for k in ('retrieval_only_requests', 'requests', 'wall_s', 'output_tokens', 'usd_list', 'shell_commands', 'handles_issued', 'handle_retrievals'):
    m = sum(f(cell[p + ('main',)][k]) for p in keep); b = sum(f(cell[p + ('bcw',)][k]) for p in keep)
    print(f'{k}: main {m:.4g} bcw {b:.4g} ({(b - m) / m * 100:+.1f}%)' if m else f'{k}: main {m:.4g} bcw {b:.4g}')
print('pairs with more retrieval-only requests on bcw:', sum(f(cell[p + ('bcw',)]['retrieval_only_requests']) > f(cell[p + ('main',)]['retrieval_only_requests']) for p in pairs), 'of', len(pairs))
print('pairs with fewer requests on bcw:', sum(f(cell[p + ('bcw',)]['requests']) < f(cell[p + ('main',)]['requests']) for p in keep), 'of', len(keep))
print('pairs passing on main and failing on bcw:', sum(cell[p + ('main',)]['passed'] == 'True' and cell[p + ('bcw',)]['passed'] != 'True' for p in pairs))
for t in sorted({p[0] for p in pairs}):
    print(t, 'hidden pass main', sum(cell[(t, r, 'main')]['passed'] == 'True' for (tt, r) in pairs if tt == t), 'bcw', sum(cell[(t, r, 'bcw')]['passed'] == 'True' for (tt, r) in pairs if tt == t), 'of', sum(tt == t for tt, _ in pairs))
