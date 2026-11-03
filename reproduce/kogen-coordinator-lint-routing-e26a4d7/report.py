#!/usr/bin/env python3
"""Print the saved, descriptive task table; does not invoke models or grading."""
import json,sys
from pathlib import Path
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('results.json')
x=json.loads(p.read_text())
assert x['verdict'] in ('unresolved','same','better','worse')
assert len(x['tasks'])==3
print('Verdict:',x['verdict'])
print('task\tstored outcome\tcandidate outcome\tvalid Intent old/new\thidden whole-task pass old/new\tattribution')
for r in x['tasks']:
 a,b=r['stored'],r['candidate'];at=r['attribution'];yn=lambda z:'unknown' if z is None else 'yes' if z else 'no'
 print('\t'.join([r['task'],a['outcome'],b['outcome'],yn(a['valid_intent'])+'/'+yn(b['valid_intent']),yn(a['hidden_pass'])+'/'+yn(b['hidden_pass']),at['stage']+' / '+at['class']+' / '+at['cause']]))
print('Measured input/cached/output tokens:',*(x['cost'][k] for k in ('input_tokens','cached_input_tokens','output_tokens')))
print('Candidate wall seconds including failed attempts:',x['candidate_cell_wall_s'])
print('Acceptance separation:',x['acceptance_separation'])
print('USD:',x['cost']['usd'])
print('Disposition:',x['disposition'])
