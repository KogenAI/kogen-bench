#!/usr/bin/env python3
"""L8: test names in the request's section 6 tables with their verdict and whether the row names a replacement.
usage: l8_section6.py <request.md> <out.tsv>"""
import re, sys, csv
req, out = sys.argv[1:3]
lines = open(req).read().splitlines()
start = next(i for i, l in enumerate(lines) if l.startswith('## 6. Delete / rewrite lists'))
end = next(i for i, l in enumerate(lines) if l.startswith('## 7.'))
TEST = re.compile(r'\bTest[A-Za-z0-9_]*[A-Za-z0-9]\b')
VERB = re.compile(r'\b(DEL|REL|REW|MOVE|FAST)\b')
REPL = re.compile(r'(\.go:\d+|\.feature:\d+|\.js:\d+|"[^"]{12,}")|covered|already')
rows = []
for l in lines[start:end]:
    if not l.startswith('|') or set(l.replace('|', '').strip()) <= set('-: '): continue
    cells = [c.strip() for c in l.strip('|').split('|')]
    names = sorted(set(TEST.findall(l)))
    if not names: continue
    verbs = VERB.findall(l)
    verdict = verbs[0] if verbs else ''
    rest = ' '.join(cells[2:]) if len(cells) > 2 else ''
    for n in names:
        rows.append(dict(name=n, verdict=verdict, all_verbs=','.join(sorted(set(verbs))), replacement_named='yes' if REPL.search(rest) or verdict in ('REL', 'FAST') else 'no'))
with open(out, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['name', 'verdict', 'all_verbs', 'replacement_named'], delimiter='\t'); w.writeheader(); w.writerows(rows)
print(len(rows), 'name rows;', len({r['name'] for r in rows}), 'distinct names')
import collections; print(collections.Counter(r['verdict'] for r in rows))
