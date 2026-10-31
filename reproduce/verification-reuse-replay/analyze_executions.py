# Counts command seconds by kind and replays the "same start tree and command, an earlier run passed" rule on single executions.
# Usage: python3 -I analyze_executions.py DATADIR   (DATADIR holds exec.json.gz). Standard library only.
import json,collections,gzip,sys
d=json.load(gzip.open(sys.argv[1]+'/exec.json.gz','rt')); rows=d['rows']; passes=d['passes']
def isTest(r): return r['check'] not in('format','compile') and not r['check'].startswith(('setup','fix'))
print('executions',len(rows))
c=collections.Counter((r['src'],r['kind']) for r in rows); print(c)
s=collections.defaultdict(float)
for r in rows: s[(r['src'],r['kind'])]+=r['secs']
print({k:round(v) for k,v in s.items()})
runs=collections.defaultdict(list)
for r in rows: runs[(r['src'],r['run'])].append(r)
# identity: vdir uniqueness
vd=collections.Counter((r['src'],r['run'],r['vdir']) for r in rows if r['vdir'])
print('verify dirs',len(vd),'reused-in-run (same vdir in >1 pass):', sum(1 for (k,v) in {(a,b,c):1 for (a,b,c) in vd}.items()))
# same vdir across passes?
vp=collections.defaultdict(set)
for r in rows:
    if r['vdir']: vp[(r['src'],r['run'],r['vdir'])].add(r['pass_'])
print('vdir spanning >1 pass',sum(1 for v in vp.values() if len(v)>1), 'of',len(vp))
# --- baseline reuse: same start_head + check cmd across runs, prior passed
for src in('delivery','lanes'):
    seen={}; save=0;n=0;unk=0;tot=0
    allb=[r for r in rows if r['src']==src and r['kind']=='baseline']
    for r in sorted(allb,key=lambda r:r['start']):
        tot+=r['secs']
        k=(r['start_head'],r['cmd'])
        if k in seen and seen[k]['status']==0:
            save+=r['secs'];n+=1
        seen.setdefault(k,r) if k not in seen or seen[k]['status']!=0 else None
    print(src,'baseline execs',len(allb),'secs',round(tot),'| same head+cmd earlier passed: n',n,'secs',round(save))
