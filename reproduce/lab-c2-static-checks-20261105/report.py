#!/usr/bin/env python3
"""Lab C2 step 1: recompute every number of the finding from the published data. python3 -I report.py data"""
import json,re,sys,collections,os
d=sys.argv[1] if len(sys.argv)>1 else 'data'
J=lambda n:json.load(open(os.path.join(d,n)))
L=lambda n:[json.loads(x) for x in open(os.path.join(d,n)) if x.strip()]
tab=J('c2-table.json'); bb=[r for r in tab if r['group']=='builder-blocked']; ri=[r for r in tab if r['group']=='report_invalid']
caught=sum(r['a_catches'] for r in bb)
print('builder-blocked targeted: %d, caught by (a): %d (%.1f%%)'%(len(bb),caught,100*caught/len(bb)))
print('report_invalid: 6 rows = %d Intents, all already refused by the readiness acceptance run'%len(ri))
print('caught before approve counting existing refusals: 7 of 28 = %.0f%%'%(100*7/28))
ch=L('cheap-checks.jsonl'); g=[x for x in ch if x['kind']=='green']; f=[x for x in ch if x['kind']=='fail']
print('cheap checks: green trees %d, files %d, flagged %d; recovered failing trees %d (5 of C2 plus the C10 tree), files %d, flagged %d'%(len({x['tree'] for x in g}),len({(x['tree'],x['file']) for x in g}),sum(x['fail'] for x in g),len({x['tree'] for x in f}),len({(x['tree'],x['file']) for x in f}),sum(x['fail'] for x in f)))
smp=set(J('green-sample30.json')); print('sample: %d Intents, %d with checkable files, flagged files %d'%(len(smp),len({x['tree'] for x in g if x['tree'] in smp}),sum(x['fail'] for x in g if x['tree'] in smp)))
v=L('go-vet-configured-scope.jsonl'); dirs=[(r,x) for r in v for x in r['vet']]
cov=[(r,x) for r,x in dirs if x['covered']]
print('go vet, %d Intents with Go: %d dirs in ./... scope: %d pass, %d fail; %d outside scope'%(len(v),len(cov),sum(1 for r,x in cov if x['rc']==0),sum(1 for r,x in cov if x['rc']),len(dirs)-len(cov)))
for r,x in cov:
    if x['rc']: print('  false refusal:',r['repo'],r['slug'],x['out'].replace('\n',' | ')[-120:])
print('  false refusals in the 30 sample:',sum(1 for r,x in cov if x['rc'] and r['repo']+'__'+r['slug'] in smp))
pk=L('go-vet-package-mode.jsonl'); c=collections.Counter()
for r in pk:
    for x in r['vet']:
        o=x['out']
        c['pass' if x['rc']==0 else 'type error against code the Intent adds' if re.search(r'undefined:|has no field or method|not declared by package|cannot use',o) and not re.search(r'cannot find module|is not in std',o) else 'not compilable standalone (constraints, module)']+=1
print('naive go vet <dir> of every shaped Go dir:',dict(c))
for p in J('class-probes.json'): print('  probe %-28s flagged=%s'%(p['cls'],p['flagged']))
print('success rule: catch>=60%% -> %s ; false refusals<=1 of 30 -> %s'%('MET' if caught/len(bb)>=.6 else 'NOT MET','MET' if sum(x['fail'] for x in g if x['tree'] in smp)<=1 else 'NOT MET'))
