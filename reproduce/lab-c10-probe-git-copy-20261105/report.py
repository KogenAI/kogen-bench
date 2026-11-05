#!/usr/bin/env python3
"""Lab C10: recompute the finding's numbers from the published replay records. python3 -I report.py data"""
import json,sys,os
d=sys.argv[1] if len(sys.argv)>1 else 'data'
J=lambda n:json.load(open(os.path.join(d,n)))
A,B=J('replay-A.json'),J('replay-B.json'); rec=J('recorded-controls.json')
def ok(x):
    if x['Group'].startswith('affected'): return (x['Status'],x['Output'])==((0,'observer good\n') if x['Name']=='good' else (1,'observer bad rejected\n'))
    e=rec.get(x['ID']+'/'+x['Name']); return e is not None and x['Status']==e['exit'] and x['Output']==e['output']
for arm,R in (('A (release)',A),('B (git copy)',B)):
    aff=[x for x in R if x['Group'].startswith('affected')]; ctl=[x for x in R if x['Group']=='control-real']
    ids=sorted({x['ID'] for x in aff})
    passing=[i for i in ids if all(ok(x) for x in aff if x['ID']==i)]
    print('arm %s: affected Intents passing %d of %d (%d of %d commands); controls %d (%d commands) matching the recorded result: %d'%(arm,len(passing),len(ids),sum(ok(x) for x in aff),len(aff),len({x['ID'] for x in ctl}),len(ctl),sum(ok(x) for x in ctl)))
same=sum(1 for a,b in zip([x for x in A if x['Group']=='control-real'],[x for x in B if x['Group']=='control-real']) if (a['Status'],a['Output'])==(b['Status'],b['Output']))
print('controls with identical status and output in A and B: %d of %d commands'%(same,len([x for x in A if x['Group']=='control-real'])))
print('isolation test B:',[l for l in open(os.path.join(d,'isolation-test-B.log')) if l.startswith(('--- ','ok','FAIL'))][:3])
for a in 'AB':
    t=open(os.path.join(d,'probe-contract-tests-%s.log'%a)).read()
    print('existing TestProbe* in %s:'%a,'pass' if '\nok' in t or t.startswith('ok') else 'FAIL: '+', '.join(l.strip().split()[2] for l in t.splitlines() if '--- FAIL' in l))
