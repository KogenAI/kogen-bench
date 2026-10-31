"""usage: build_pack.py <pack dir> <round1 mirror> <round2 mirror>: runs.csv + pooled expected-output.txt for loopnight levers."""
import json,sys,pathlib,csv,math,statistics as st
pk=pathlib.Path(sys.argv[1]);rounds=[('r1',pathlib.Path(sys.argv[2])),('r2',pathlib.Path(sys.argv[3]))]
def metrics(R,c):
    p=R/'counted'/'cells'/c['task']/('r'+str(c['rep']))/c['arm']
    if not (p/'result.json').exists() or not (p/'route-summary.json').exists():return None
    r=json.loads((p/'result.json').read_text());s=json.loads((p/'route-summary.json').read_text())
    rc=[x for x in map(json.loads,(p/'route-receipts.jsonl').read_text().splitlines()) if x.get('forwarded')]
    names=[[c['name'] for c in x.get('output_calls') or []] for x in rc];u=[x.get('usage') or {} for x in rc]
    w=[i for i,n in enumerate(names) if 'write_file' in n]
    return dict(outcome=r.get('outcome'),passed=int(bool(r.get('all_passed'))),wall=r['totals']['wall_s'],usd=s['usd_list'] if s.get('all_usage_present') else s['charge_upper_bound_usd'],req=len(rc),tool_calls=sum(len(n) for n in names),
      out=sum(x.get('output_tokens',0) for x in u),inp=sum(x.get('input_tokens',0) for x in u),cached=sum((x.get('input_tokens_details') or {}).get('cached_tokens',0) for x in u),
      shell_only=sum(1 for n in names if n and set(n)=={'shell'}),writes=sum(n.count('write_file') for n in names),after_write=(len(names)-1-w[-1]) if w else '')
rows=[];pairs={}
for rn,R in rounds:
    if not (R/'protocol.json').exists():continue
    prot=json.loads((R/'protocol.json').read_text())
    for b in prot['blocks']:
        cs=[prot['cells'][i] for i in b['cells']];m={}
        for c in cs:
            x=metrics(R,c)
            if x:rows.append(dict(round=rn,lever=b['lever'],task=c['task'],rep=c['rep'],arm=c['arm'],**x));m[c['arm']]=x
        if len(m)==2:pairs.setdefault(b['lever'],[]).append((rn,b['task'],m['base'],m[b['lever']]))
with (pk/'runs.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def sign(k,n):
    m=min(k,n-k);return min(1.0,2*sum(math.comb(n,i) for i in range(m+1))/2**n) if n else 1.0
def gm(xs):return math.exp(st.mean(math.log(x) for x in xs))
out=[]
for lv in ('l1','l2','l3'):
    for scope in ('r1','r2','pooled'):
        P=[(t,a,b) for rn,t,a,b in pairs.get(lv,[]) if scope in ('pooled',rn)]
        if not P:continue
        n=len(P);line=[f'{lv} {scope}: {n} blocks; pass base {sum(a["passed"] for _,a,_ in P)}/{n} lever {sum(b["passed"] for _,_,b in P)}/{n}']
        for k,lab in (('wall','wall'),('usd','cost'),('req','requests'),('out','output tokens'),('shell_only','shell-only requests'),('writes','write_file calls')):
            win=sum(b[k]<a[k] for _,a,b in P);tie=sum(b[k]==a[k] for _,a,b in P)
            r=gm([b[k]/a[k] for _,a,b in P if a[k] and b[k]]) if all(a[k] and b[k] for _,a,b in P) else float('nan')
            line.append(f'  {lab}: lever lower {win}/{n} (ties {tie}), sign p={sign(win,n-tie):.4f}, geomean ratio {r:.3f}, base mean {st.mean(a[k] for _,a,_ in P):.3f}, lever mean {st.mean(b[k] for _,_,b in P):.3f}')
        out+=line+['']
(pk/'expected-output.txt').write_text('\n'.join(out))
print('\n'.join(out))
