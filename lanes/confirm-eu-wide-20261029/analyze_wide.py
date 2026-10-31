import collections, csv, datetime, hashlib, json, math, pathlib, statistics
R=pathlib.Path(__file__).resolve().parent
if not (R/'protocol.json').exists(): R=R/'receipts'
protocol=json.loads((R/'protocol.json').read_text())
def read(p):return json.loads(p.read_text())
def sign(values):
    lo=sum(x<0 for x in values);hi=sum(x>0 for x in values);n=lo+hi
    p=min(1.,2*sum(math.comb(n,k) for k in range(min(lo,hi)+1))/2**n) if n else 1.
    return {'loop_lower':lo,'codex_lower':hi,'ties':len(values)-n,'n_nonzero':n,'two_sided_p':p}
cells=[]
for c in protocol['cells']:
    p=R/c['stratum']/'cells'/c['task']/f"r{c['rep']}"/c['arm']
    if not (p/'result.json').exists():continue
    result=read(p/'result.json'); route=read(p/'route-summary.json')
    receipts=[json.loads(s) for s in (p/'route-receipts.jsonl').read_text().splitlines()]
    receipts=[r for r in receipts if r.get('forwarded')]
    usages=[x['usage'] for x in receipts if x.get('usage')]
    i=sum(u['input_tokens'] for u in usages); ca=sum(u.get('input_tokens_details',{}).get('cached_tokens',0) for u in usages)
    wr=sum(u.get('input_tokens_details',{}).get('cache_creation_tokens',u.get('input_tokens_details',{}).get('cache_write_tokens',0)) for u in usages)
    out=sum(u['output_tokens'] for u in usages)
    cells.append({**c,'passed':result.get('all_passed'),'outcome':result['outcome'],'wall_s':result['totals']['wall_s'],'usd':route['usd_list'],'input':i,'uncached':i-ca,'cached':ca,'cache_write':wr,'output':out,'requests':len(receipts),'route_stop_reason':route.get('stop_reason')})
arms={}
for arm in protocol['arms']:
    rows=[c for c in cells if c['arm']==arm];passes=sum(c['passed'] is True for c in rows)
    walls=sorted(c['wall_s'] for c in rows if c['passed'] is not None)
    totals={k:sum(c[k] for c in rows) for k in ['usd','input','uncached','cached','cache_write','output','requests']}
    arms[arm]={'pass':passes,'graded':sum(c['passed'] is not None for c in rows),'launched':len(rows),'unstarted':len(protocol['tasks_randomized'])-len(rows),'clean_completions':sum(c['outcome']=='finished' for c in rows),'median_wall_s':statistics.median(walls) if walls else None,'p90_wall_s':walls[math.ceil(.9*len(walls))-1] if walls else None,'mean_wall_s':statistics.mean(walls) if walls else None,'totals':totals,'per_pass':{k:v/passes if passes else None for k,v in totals.items()}}
pairs={}
for effort in ['medium','high']:
    rows=[]
    for task in protocol['tasks_randomized']:
        loop=next((c for c in cells if c['task']==task and c['arm']=='loop-'+effort),None)
        codex=next((c for c in cells if c['task']==task and c['arm']=='codex-'+effort),None)
        if loop and codex:rows.append({'task':task,'loop':loop,'codex':codex})
    pairs[effort]={'clean_completion_wall_sign_test':sign([r['loop']['wall_s']-r['codex']['wall_s'] for r in rows if r['loop']['outcome']=='finished' and r['codex']['outcome']=='finished']),'n_clean_completion_pairs':sum(r['loop']['outcome']=='finished' and r['codex']['outcome']=='finished' for r in rows),'n_tasks':len(rows),'wall_sign_test':sign([r['loop']['wall_s']-r['codex']['wall_s'] for r in rows]),'cost_sign_test':sign([r['loop']['usd']-r['codex']['usd'] for r in rows]),'grade_sign_test':sign([int(r['codex']['passed'] is True)-int(r['loop']['passed'] is True) for r in rows]),'mean_wall_ratio':sum(r['loop']['wall_s'] for r in rows)/sum(r['codex']['wall_s'] for r in rows) if rows else None,'total_cost_ratio':sum(r['loop']['usd'] for r in rows)/sum(r['codex']['usd'] for r in rows) if rows else None,'rows':rows}
analysis={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seed':protocol['seed'],'arms':arms,'pairs':pairs,'cells':cells,'total_usd':sum(c['usd'] for c in cells),'counted':len(cells),'planned':len(protocol['cells'])}
(R/'analysis.json').write_text(json.dumps(analysis,indent=2,sort_keys=True)+'\n')
with (R/'all-attempts.tsv').open('w') as f:
    writer=csv.DictWriter(f,fieldnames=list(cells[0]),delimiter='\t');writer.writeheader();writer.writerows(cells)
print(json.dumps({k:v for k,v in analysis.items() if k not in ['cells','pairs']},indent=2))
