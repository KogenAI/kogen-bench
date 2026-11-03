#!/usr/bin/env python3
import json,sys
from pathlib import Path
d=json.loads(Path(sys.argv[1]).read_text())
print(d['component']+' '+d['head'][:7]+': '+d['verdict'].upper())
for pin in ['baseline','head']:
    t=d['contract_tests'][pin]
    print(pin+' targeted contracts: '+str(t['passed_cases'])+' passed, '+str(t['failed_cases'])+' failed')
for r in d['tasks']:
    a,b=r['stored'],r['candidate']
    def val(x):return 'unknown' if x is None else str(x).lower()
    print(r['task']+': '+a['outcome']+' -> '+b['outcome']+'; valid Intent '+val(a['valid_intent'])+' -> '+val(b['valid_intent'])+'; hidden pass '+val(a['hidden_pass'])+' -> '+val(b['hidden_pass'])+'; acceptance separation '+b['acceptance_separation']+'; cause '+r['attribution']['class'])
print('Candidate input/output tokens: '+str(d['cost']['input_tokens'])+'/'+str(d['cost']['output_tokens'])+'; dollar total '+('unavailable' if d['cost']['usd'] is None else str(d['cost']['usd'])))
print('Timings include failed attempts. No fresh control cells.')
