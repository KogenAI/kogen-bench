#!/usr/bin/env python3
"""profile.py <dir with <repo>.json files from `go test -json`>: per-repo summary as JSON on stdout."""
import json,sys,glob,os
BUDGET={'kogen':60,'kogen-build':60,'kogen-shaping':45,'kogen-loop':10}
out={}
for f in sorted(glob.glob(os.path.join(sys.argv[1],'*.json'))):
    r=os.path.basename(f)[:-5]; T={}; pk={}; failed=set()
    for l in open(f,errors='replace'):
        try: e=json.loads(l)
        except ValueError: continue
        a=e.get('Action'); t=e.get('Test'); p=e.get('Package')
        if a in ('pass','fail','skip') and e.get('Elapsed') is not None:
            if t: T[(p,t)]=e['Elapsed']
            else: pk[p]=e['Elapsed']
        if a=='fail' and t: failed.add((p,t.split('/')[0]))
    top=sorted(T.items(),key=lambda x:-x[1])[:20]
    mx=max(pk.values() or [0]); sm=sum(pk.values())
    out[r]=dict(packages=len(pk),tests=len(T),failed_tests=len(failed),over_1s=sum(v>1 for v in T.values()),over_5s=sum(v>5 for v in T.values()),
        package_wall_max_s=round(mx,1),package_wall_sum_s=round(sm,1),parallelism_ratio=round(sm/mx,2) if mx else 0,
        budget_s=BUDGET.get(r,20),slowest=[[k[1],round(v,1)] for k,v in top])
json.dump(out,sys.stdin if False else sys.stdout,indent=1,sort_keys=True)
