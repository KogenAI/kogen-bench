#!/usr/bin/env python3
import json
from pathlib import Path
p=Path(__file__).resolve().parent
rows=json.loads((p/'data/results.json').read_text())
for r in rows:
 print(r['task'],r['outcome'],'valid_intent='+str(r['valid_intent']),'hidden_all_pass='+str(r['hidden_all_pass']),'provider_errors='+str(r['provider_errors']))
print('n=1 per task; descriptive only. Tool payloads unavailable; no matched efficacy estimate.')
print('Known input:',sum(sum(r[k].get('input',0) for k in ['known_shape_usage','known_build_usage']) for r in rows))
print('Known output:',sum(sum(r[k].get('output',0) for k in ['known_shape_usage','known_build_usage']) for r in rows))
print('Dollars unknown; partial usage is a lower bound; reasoning is included in output.')
