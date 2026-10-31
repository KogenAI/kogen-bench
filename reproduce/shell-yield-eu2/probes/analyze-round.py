import hashlib,json,math,pathlib,statistics,sys
# usage: analyze_shellwait.py <run dir> -> writes shellwait-analysis.json there, prints a markdown section.
# Registered analysis (protocol.json registration): primary shell seconds and agent wall per cell, paired per
# task and rep, exact two-sided sign tests with ties dropped; secondary pass, USD / cost per pass, requests.
R=pathlib.Path(sys.argv[1])
protocol=json.loads((R/'protocol.json').read_text())
ARMS=['loop-default','shell-yield','codex'];LABEL={'loop-default':'loop default','shell-yield':'loop shell-yield','codex':'Codex CLI'}

def loop_shell(d,wall):
 """Loop arms: shell tool.call->tool.result from loop's own event times (whole seconds); an unanswered call counts to the agent end."""
 import datetime
 P=lambda x:datetime.datetime.fromisoformat(x.replace('Z','+00:00'))
 ev=[json.loads(x) for x in (d/'events.jsonl').read_text().splitlines() if x.strip()]
 t0=P(ev[0]['time']);st={};sp=[]
 for e in ev:
  if e.get('name')!='shell':continue
  if e.get('type')=='tool.call':st[e['call_id']]=(P(e['time'])-t0).total_seconds()
  elif e.get('type')=='tool.result' and e.get('call_id') in st:sp.append((P(e['time'])-t0).total_seconds()-st.pop(e['call_id']))
 sp+=[max(0.,wall-s) for s in st.values()]
 return round(sum(sp),3),len(sp),round(max(sp,default=0),3),len(st)

def shell(d,arm):
 """(shell seconds, calls or commands, longest single interval s) from receive-time stamps."""
 p=d/'shell-timing.jsonl'
 if not p.exists():return None,0,None
 rows=[json.loads(x) for x in p.read_text().splitlines()]
 start={};spans=[]
 for x in rows:
  if x['event'] in ('tool.call','item.started'):start[x['id']]=x['t']
  elif x['id'] in start:spans.append((start.pop(x['id']),x['t']))
 end=max([x['t'] for x in rows],default=0)
 spans+=[(s,end) for s in start.values()]  # never-finished items count to the last stamp
 if arm=='codex':  # union: Codex overlaps commands
  tot=0.;cur=None
  for s,e in sorted(spans):
   if cur is None or s>cur[1]:
    if cur:tot+=cur[1]-cur[0]
    cur=[s,e]
   else:cur[1]=max(cur[1],e)
  if cur:tot+=cur[1]-cur[0]
 else:tot=sum(e-s for s,e in spans)
 return round(tot,3),len(spans),round(max((e-s for s,e in spans),default=0),3)

def items(d):
 p=d/'tool-items.jsonl'
 if not p.exists():return {}
 xs=[json.loads(x) for x in p.read_text().splitlines()]
 heads=[x.get('head','') for x in xs if x.get('kind')=='output']
 calls=[x for x in xs if x.get('kind')=='call' and x.get('name')=='shell']
 waits=sum('"session"' in (c.get('arguments') or '') and '"command"' not in (c.get('arguments') or '') for c in calls)
 return {'yields':sum(h.startswith('still running after') for h in heads),'stops':sum(h.startswith('stopped session') for h in heads),'session_calls':waits,'shell_calls':len(calls)}

def load(d,arm):
 if not (d/'result.json').exists():return None
 r=json.loads((d/'result.json').read_text());s=json.loads((d/'route-summary.json').read_text());t=r['totals']
 unanswered=0
 if arm=='codex':sh,n,longest=shell(d,arm)
 else:sh,n,longest,unanswered=loop_shell(d,t['wall_s'])
 return {'pass':bool(r.get('all_passed')),'outcome':r.get('outcome'),'wall':t['wall_s'],'shell_s':sh,'shell_n':n,'longest_shell_s':longest,'requests':s['requests'],'reasoning':t['reasoning_tokens'],'output':t['output_tokens'],
  'usd':s['usd_list'] if s.get('all_usage_present') else s['charge_upper_bound_usd'],'timeout':r.get('outcome')=='timeout','unanswered_shell':unanswered,**items(d)}
cells={};dry={}
for i,c in enumerate(protocol['cells']):
 x=load(R/c['stratum']/'cells'/c['task']/('r'+str(c['rep']))/c['arm'],c['arm'])
 if not x:continue
 x['index']=i
 (cells if c['stratum']=='counted' else dry)[(c['task'],c['rep'],c['arm'])]=x
blocks=[(t,r) for r in range(1,protocol['reps']+1) for t in protocol['tasks'] if all((t,r,a) in cells for a in ARMS)]
def p90(v):v=sorted(v);return v[max(0,math.ceil(.9*len(v))-1)]
def test(w,l,n_all):
 n=w+l;k=min(w,l);p=1. if n==0 else min(1.,2*sum(math.comb(n,i) for i in range(k+1))/2**n)
 return {'first_wins':w,'second_wins':l,'ties':n_all-n,'p':p}
def sign(a,b):return test(sum(x<y for x,y in zip(a,b)),sum(x>y for x,y in zip(a,b)),len(a))
def cpp(x):return x['usd'] if x['pass'] else math.inf
per_arm={}
for a in ARMS:
 xs=[cells[(t,r,a)] for (t,r,aa) in cells if aa==a];np_=sum(x['pass'] for x in xs)
 tot={k:sum(x[k] or 0 for x in xs) for k in ('wall','shell_s','requests','reasoning','output','usd')}
 per_arm[a]={'launched':len(xs),'passes':np_,'median_wall':statistics.median(x['wall'] for x in xs) if xs else None,'p90_wall':p90([x['wall'] for x in xs]) if xs else None,
  'median_shell_s':statistics.median(x['shell_s'] or 0 for x in xs) if xs else None,'mean_wall':tot['wall']/len(xs) if xs else None,**{'total_'+k:v for k,v in tot.items()},
  'usd_per_pass':tot['usd']/np_ if np_ else None,'timeouts':sum(x['timeout'] for x in xs),'yields':sum(x.get('yields',0) for x in xs),'stops':sum(x.get('stops',0) for x in xs),'session_calls':sum(x.get('session_calls',0) for x in xs)}
METRICS=['shell_s','wall','usd_per_pass','usd','requests']
def pair(a,b):
 out={}
 for m in METRICS:
  f=cpp if m=='usd_per_pass' else (lambda x,m=m:x[m] if x[m] is not None else math.inf)
  out[m]=sign([f(cells[(t,r,a)]) for t,r in blocks],[f(cells[(t,r,b)]) for t,r in blocks])
 da=[cells[(t,r,a)]['pass'] for t,r in blocks];db=[cells[(t,r,b)]['pass'] for t,r in blocks]
 out['pass']=test(sum(x and not y for x,y in zip(da,db)),sum(y and not x for x,y in zip(da,db)),len(blocks))
 for m in ('wall','shell_s'):
  sa=sum(cells[(t,r,a)][m] or 0 for t,r in blocks);sb=sum(cells[(t,r,b)][m] or 0 for t,r in blocks)
  out[m+'_total_ratio']=sa/sb if sb else None
 return out
pairs={'shell-yield vs loop-default':pair('shell-yield','loop-default'),'shell-yield vs codex':pair('shell-yield','codex'),'loop-default vs codex':pair('loop-default','codex')}
probes=[json.loads(x) for x in (R/'probes.jsonl').read_text().splitlines()] if (R/'probes.jsonl').exists() else []
spend={'counted_usd':sum(x['usd'] for x in cells.values()),'dry_usd':sum(x['usd'] for x in dry.values()),'probes':len(probes),'probe_usd':sum(x.get('usd',0) for x in probes)}
spend['total_usd']=spend['counted_usd']+spend['dry_usd']+spend['probe_usd']
w=R/'patch-witnesses.json';capv=max(protocol['round_cap_usd'],json.loads(w.read_text()).get('cap_usd',0)) if w.exists() else protocol['round_cap_usd']
analysis={'protocol_sha256':hashlib.sha256((R/'protocol.json').read_bytes()).hexdigest(),'registered_tasks':protocol['tasks'],'completed_counted_cells':len(cells),'complete_blocks':blocks,'dry':{f'{t}/r{r}/{a}':x for (t,r,a),x in dry.items()},'per_arm':per_arm,
 'per_cell':{f'{t}/r{r}/{a}':x for (t,r,a),x in cells.items()},'paired_sign_tests':pairs,'spend':spend,'cap_usd':capv}
(R/'shellwait-analysis.json').write_text(json.dumps(analysis,indent=2,sort_keys=True,default=str)+'\n')

f=lambda v,d=1:'n/a' if v is None else f'{v:,.{d}f}'
L=[f"Counted cells {len(cells)}/{3*len(protocol['tasks'])*protocol['reps']}, complete task-rep blocks {len(blocks)}/{len(protocol['tasks'])*protocol['reps']}; spend ${f(spend['total_usd'],6)} (counted ${f(spend['counted_usd'],6)}, dry ${f(spend['dry_usd'],6)}, {spend['probes']} probes ${f(spend['probe_usd'],6)}) / cap ${f(capv,6)}.",'']
L.append('| Arm | Pass / launched (deadline timeouts) | Shell s (total / median) | Agent wall s (mean / median / p90) | Requests | USD total / per pass | Yields / waits / stops |')
L.append('| --- | ---: | ---: | ---: | ---: | ---: | ---: |')
for a in ARMS:
 x=per_arm[a]
 L.append(f"| {LABEL[a]} (high) | {x['passes']} / {x['launched']} ({x['timeouts']}) | {f(x['total_shell_s'])} / {f(x['median_shell_s'])} | {f(x['mean_wall'])} / {f(x['median_wall'])} / {f(x['p90_wall'])} | {x['total_requests']:,} | ${f(x['total_usd'],4)} / {'$'+f(x['usd_per_pass'],4) if x['usd_per_pass'] else 'n/a'} | {x['yields']} / {x['session_calls']} / {x['stops']} |")
L.append('');L.append('**Paired by task and rep (lower is better; first-arm wins / comparison wins, ties, exact two-sided sign test p). Primary: shell seconds, agent wall.**');L.append('')
L.append('| Comparison | Shell s | Wall | Shell total ratio | Wall total ratio | Pass | Cost per pass | USD | Requests |');L.append('| --- | --- | --- | --- | --- | --- | --- | --- | --- |')
g=lambda v:f"{v['first_wins']}/{v['second_wins']}, {v['ties']} ties, p={v['p']:.3f}"
for k,v in pairs.items():
 L.append(f"| {k} ({len(blocks)} pairs) | {g(v['shell_s'])} | {g(v['wall'])} | {f(v['shell_s_total_ratio'],2)} | {f(v['wall_total_ratio'],2)} | {g(v['pass'])} | {g(v['usd_per_pass'])} | {g(v['usd'])} | {g(v['requests'])} |")
L.append('');L.append('**Per cell (agent wall s / shell s, longest shell s / requests / USD; pass).**');L.append('')
L.append('| Task / rep | loop default | loop shell-yield | Codex CLI |');L.append('| --- | --- | --- | --- |')
def cellrow(x):
 if not x:return 'not run'
 y=f"; yields {x.get('yields',0)}, waits {x.get('session_calls',0)}, stops {x.get('stops',0)}" if x.get('yields') or x.get('stops') else ''
 return f"{f(x['wall'])} / {f(x['shell_s'])}, {f(x['longest_shell_s'])} / {x['requests']} / ${f(x['usd'],4)}; {'pass' if x['pass'] else 'fail'}{'; deadline timeout' if x['timeout'] else ''}{y}"
for (t,r) in [('dry',0)]+[(t,r) for r in range(1,protocol['reps']+1) for t in protocol['tasks']]:
 if t=='dry':
  L.append(f"| dry: {protocol['dry_task']} | "+' | '.join(cellrow(dry.get((protocol['dry_task'],0,a))) for a in ARMS)+' |');continue
 L.append(f'| {t} r{r} | '+' | '.join(cellrow(cells.get((t,r,a))) for a in ARMS)+' |')
print('\n'.join(L))
