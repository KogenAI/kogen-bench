import json,sys,collections,statistics as S
D=sys.argv[1]
runs=[json.loads(l) for l in open(D+'/runs.jsonl')]
items=json.load(open(D+'/items-resolved.json'))
by=collections.defaultdict(lambda:{'A':[],'B':[]})
for r in runs: by[(r['tree'],r['check'])][r['arm']].append(r)
res=[]
for it in items:
    k=(it['tree'].rsplit('/',1)[-1],it['check']); g=by.get(k)
    if not g or not g['A']: res.append(dict(id=it['id'],bucket=it['bucket'],cls='not-run')); continue
    A=[x['rc']==0 for x in g['A']]; B=[x['rc']==0 for x in g['B']]
    if not any(A): c='real'
    elif not all(A): c='flaky'
    elif not all(B): c='load-induced'
    else: c='not-reproduced'
    sa=S.median([x['secs'] for x in g['A']]); sb=S.median([x['secs'] for x in g['B']]) if g['B'] else None
    res.append(dict(id=it['id'],bucket=it['bucket'],repo=it['repo'],sha=it['sha'],cls=c,A_pass=f"{sum(A)}/{len(A)}",B_pass=f"{sum(B)}/{len(B)}",A_med_s=sa,B_med_s=sb,ratio=round(sb/sa,2) if sb and sa else None,
        B_timeouts=sum(1 for x in g['B'] if x['timeout']),A_timeouts=sum(1 for x in g['A'] if x['timeout']),B_load1=round(S.mean([float(x['load1']) for x in g['B']]),1) if g['B'] else None))
json.dump(res,open(D+'/e3-summary.json','w'),indent=1)
cnt=collections.defaultdict(collections.Counter)
for r in res: cnt[r['bucket']][r['cls']]+=1
print(json.dumps({b:dict(c) for b,c in cnt.items()}))
for r in res: print(r)
