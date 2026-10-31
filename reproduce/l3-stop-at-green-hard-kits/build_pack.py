"""usage: build_pack.py <pack dir> <round mirror dir>: runs.csv + expected-output.txt for the l3hard round (L3 stop-at-green on two hard kits)."""
import json,sys,pathlib,csv,statistics as st
pk=pathlib.Path(sys.argv[1]);R=pathlib.Path(sys.argv[2])
prot=json.loads((R/'protocol.json').read_text())
def metrics(c):
    p=R/'counted'/'cells'/c['task']/('r'+str(c['rep']))/c['arm']
    r=json.loads((p/'result.json').read_text());s=json.loads((p/'route-summary.json').read_text());ev=json.loads((p/'evaluation.json').read_text())
    rc=[x for x in map(json.loads,(p/'route-receipts.jsonl').read_text().splitlines()) if x.get('forwarded')]
    u=[x.get('usage') or {} for x in rc];ids=ev.get('ids') or {}
    return dict(outcome=r.get('outcome'),passed=int(bool(r.get('all_passed'))),failed_checks=sum(v!='passed' for v in ids.values()),checks=len(ids),
      wall=r['totals']['wall_s'],usd=s['usd_list'] if s.get('all_usage_present') else s['charge_upper_bound_usd'],req=len(rc),
      out=sum(x.get('output_tokens',0) for x in u),inp=sum(x.get('input_tokens',0) for x in u),cached=sum((x.get('input_tokens_details') or {}).get('cached_tokens',0) for x in u),
      failed_scenarios=' '.join(sorted(k.split(':')[1] for k,v in ids.items() if v!='passed' and k.startswith('acceptance'))))
rows=[];D={}
for c in prot['cells']:
    m=metrics(c);D[(c['task'],c['rep'],c['arm'])]=m
    rows.append(dict(task=c['task'],rep=c['rep'],arm=c['arm'],**m))
with (pk/'runs.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
out=['l3hard: base vs l3 (stop-at-green sentence), gpt-6.1-terra high, 4 reps x 2 kits, paired blocks run at the same time','']
tf={'base':0,'l3':0};fs=0;low={'wall':0,'usd':0,'req':0}
for t in prot['tasks']:
    out.append(t)
    for rep in (1,2,3,4):
        b=D[(t,rep,'base')];l=D[(t,rep,'l3')]
        out.append(f'  rep {rep}: base pass={b["passed"]} ({b["outcome"]}, failed checks {b["failed_checks"]}/{b["checks"]}, wall {b["wall"]:.0f}s, ${b["usd"]:.3f}, {b["req"]} req) | l3 pass={l["passed"]} ({l["outcome"]}, failed checks {l["failed_checks"]}/{l["checks"]}, wall {l["wall"]:.0f}s, ${l["usd"]:.3f}, {l["req"]} req)')
        tf['base']+=1-b['passed'];tf['l3']+=1-l['passed'];fs+=(b['passed'] and not l['passed'])
        for k in low:low[k]+=l[k]<b[k]
    for a in ('base','l3'):
        out.append(f'  {a}: pass {sum(D[(t,r,a)]["passed"] for r in (1,2,3,4))}/4, median wall {st.median(D[(t,r,a)]["wall"] for r in (1,2,3,4)):.0f}s, median cost ${st.median(D[(t,r,a)]["usd"] for r in (1,2,3,4)):.3f}, median requests {st.median(D[(t,r,a)]["req"] for r in (1,2,3,4))}')
    out.append('')
out+=[f'all 8 blocks: failures base {tf["base"]}, l3 {tf["l3"]}; false stops (l3 fails where its paired base passes) {fs}',
 f'l3 lower in: wall {low["wall"]}/8, cost {low["usd"]}/8, requests {low["req"]}/8 (descriptive, 8 blocks of 2 kits)',
 'total wall base %.0f s, l3 %.0f s; total cost base $%.3f, l3 $%.3f; requests base %d, l3 %d'%tuple(sum(v[m] for k,v in D.items() if k[2]==a) for m in ("wall","usd","req") for a in ("base","l3"))]
(pk/'expected-output.txt').write_text('\n'.join(out)+'\n');print('\n'.join(out))
