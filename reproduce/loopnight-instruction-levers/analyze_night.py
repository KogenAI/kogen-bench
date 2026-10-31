"""usage: analyze_night.py <round dir (mirror)> [lever...]; paired per task, lever vs the fresh base cell of the same block."""
import json,sys,pathlib,statistics as st,math
R=pathlib.Path(sys.argv[1]);levers=sys.argv[2:] or ['l1','l2','l3']
prot=json.loads((R/'protocol.json').read_text())
def d(c):return R/'counted'/'cells'/c['task']/('r'+str(c['rep']))/c['arm']
def metrics(c):
    p=d(c)
    if not (p/'result.json').exists() or not (p/'route-summary.json').exists():return None
    r=json.loads((p/'result.json').read_text());s=json.loads((p/'route-summary.json').read_text())
    rc=[x for x in map(json.loads,(p/'route-receipts.jsonl').read_text().splitlines()) if x.get('forwarded')]
    names=[[c['name'] for c in x.get('output_calls') or []] for x in rc]
    u=[x.get('usage') or {} for x in rc]
    w=[i for i,n in enumerate(names) if 'write_file' in n]
    return dict(wall=r['totals']['wall_s'],usd=s['usd_list'] if s.get('all_usage_present') else s['charge_upper_bound_usd'],req=len(rc),passed=bool(r.get('all_passed')),
      out=sum(x.get('output_tokens',0) for x in u),inp=sum(x.get('input_tokens',0) for x in u),cached=sum((x.get('input_tokens_details') or {}).get('cached_tokens',0) for x in u),
      shell_only=sum(1 for n in names if n and set(n)=={'shell'}),writes=sum(n.count('write_file') for n in names),after_write=(len(names)-1-w[-1]) if w else None)
def sign(wins,n):
    k=wins;m=min(k,n-k);p=sum(math.comb(n,i) for i in range(0,m+1))/2**n*2;return min(1.0,p)
def gm(xs):return math.exp(st.mean(math.log(x) for x in xs))
for lv in levers:
    pairs=[]
    for b in prot['blocks']:
        if b['lever']!=lv:continue
        cs=[prot['cells'][i] for i in b['cells']];base=[c for c in cs if c['arm']=='base'][0];lev=[c for c in cs if c['arm']==lv][0]
        mb,ml=metrics(base),metrics(lev)
        if mb and ml:pairs.append((b['task'],mb,ml))
    n=len(pairs)
    print(f'\n## {lv}: {n}/12 blocks complete')
    if not n:continue
    print('| task | base wall/usd/req/pass | lever wall/usd/req/pass | base out/shell-only/writes/after-write | lever |\n|---|---|---|---|---|')
    for t,a,b in pairs:print(f"| {t} | {a['wall']:.0f}/${a['usd']:.3f}/{a['req']}/{'P' if a['passed'] else 'F'} | {b['wall']:.0f}/${b['usd']:.3f}/{b['req']}/{'P' if b['passed'] else 'F'} | {a['out']}/{a['shell_only']}/{a['writes']}/{a['after_write']} | {b['out']}/{b['shell_only']}/{b['writes']}/{b['after_write']} |")
    for key,lab in (('wall','wall s'),('usd','cost'),('req','requests'),('out','output tokens'),('shell_only','shell-only reqs'),('writes','writes')):
        wins=sum(1 for _,a,b in pairs if b[key]<a[key]);ties=sum(1 for _,a,b in pairs if b[key]==a[key]);nn=n-ties
        rat=gm([max(b[key],1e-9)/max(a[key],1e-9) for _,a,b in pairs if a[key] and b[key]]) if all(a[key] and b[key] for _,a,b in pairs) else float('nan')
        print(f"- {lab}: lever lower in {wins}/{n} (ties {ties}), sign p={sign(wins,nn) if nn else 1:.3f}, geomean ratio {rat:.3f}, base mean {st.mean(a[key] for _,a,_ in pairs):.3f} lever mean {st.mean(b[key] for *_,b in pairs):.3f}")
    pa=sum(a['passed'] for _,a,_ in pairs);pb=sum(b['passed'] for *_,b in pairs)
    print(f"- pass: base {pa}/{n}, lever {pb}/{n}; cost per pass base ${sum(a['usd'] for _,a,_ in pairs)/max(pa,1):.4f} lever ${sum(b['usd'] for *_,b in pairs)/max(pb,1):.4f}")
