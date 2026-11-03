#!/usr/bin/env python3
import csv
from pathlib import Path
rows=list(csv.DictReader((Path(__file__).parent/'data/paired-results.tsv').open(),delimiter='\t'))
assert len(rows)==11
counts={a:{'intent':sum(r[a+'_intent']=='yes' for r in rows),'landed':sum(r[a+'_outcome']=='landed' for r in rows),'all_pass':sum(r[a+'_all_pass']=='yes' for r in rows)} for a in ['control','candidate']}
for a,v in counts.items():print(a,v)
a,b=counts['control'],counts['candidate']
print('Decision:', 'REVERT' if b['intent']<a['intent'] and b['landed']<=a['landed'] else 'KEEP')
print('Acceptance separation unknown; dollars unknown; no significance claim.')
