import hashlib,json,math,re,statistics,sys,pathlib
# usage: analyze_edit5.py <run dir> -> writes edit5-analysis.json there, prints a markdown section.
# Registered analysis (protocol.json registration): primary output tokens on edit turns (edit_classifier in the
# protocol), adoption, cost per pass, paired per block (task, rep), exact two-sided sign tests with ties dropped;
# secondary wall, requests, pass.
R=pathlib.Path(sys.argv[1])
protocol=json.loads((R/'protocol.json').read_text())
ARMS=['loop-default','apply-patch','codex'];LABEL={'loop-default':'loop default','apply-patch':'loop + apply_patch','codex':'Codex CLI'}
EC=protocol['edit_classifier'];EDIT_RE=re.compile('|'.join('(?:%s)'%p for p in EC['shell_edit_patterns']))
READS={'finish','read_file','list_files','search_text','view_image'}

def call_text(c):
 try:v=json.loads(c['arguments'])
 except (ValueError,TypeError):return c.get('arguments') or ''
 out=[]
 def walk(x):
  if isinstance(x,str):out.append(x)
  elif isinstance(x,list):[walk(y) for y in x]
  elif isinstance(x,dict):[walk(y) for y in x.values()]
 walk(v);return '\n'.join(out)
def edit_kind(c):
 if c['name'] in EC['file_edit_tools']:return c['name']
 if c['name'] in READS:return None
 return 'shell_edit' if EDIT_RE.search(call_text(c)) else None

def load(d):
 if not (d/'result.json').exists():return None
 r=json.loads((d/'result.json').read_text());s=json.loads((d/'route-summary.json').read_text());t=r['totals']
 rec=[json.loads(x) for x in (d/'route-receipts.jsonl').read_text().splitlines() if json.loads(x).get('forwarded')]
 outs=[json.loads(x) for x in (d/'tool-outputs.jsonl').read_text().splitlines()] if (d/'tool-outputs.jsonl').exists() else []
 head={o.get('call_id'):o.get('head','') for o in outs}
 kinds={'write_file':0,'apply_patch':0,'shell_edit':0};edit_turns=0;edit_out=0;edit_nonreason=0;edit_arg_bytes=0;ap_ids=[]
 for x in rec:
  u=x.get('usage') or {};o=u.get('output_tokens',0);rs=(u.get('output_tokens_details') or {}).get('reasoning_tokens',0)
  ks=[]
  for cl in x.get('output_calls') or []:
   k=edit_kind(cl)
   if k:ks.append(k);kinds[k]+=1;edit_arg_bytes+=cl.get('bytes',0)
   if k=='apply_patch':ap_ids.append(cl.get('call_id'))
  if ks:edit_turns+=1;edit_out+=o;edit_nonreason+=o-rs
 u=[x.get('usage') or {} for x in rec]
 out=sum(x.get('output_tokens',0) for x in u);rs=sum((x.get('output_tokens_details') or {}).get('reasoning_tokens',0) for x in u)
 ap_err=sum(1 for i in ap_ids if head.get(i,'').startswith(('error:','refused:')) or 'Failed to' in head.get(i,'')[:80])
 return {'pass':bool(r.get('all_passed')),'outcome':r.get('outcome'),'wall':t['wall_s'],'requests':s['requests'],'output':out,'reasoning':rs,'nonreasoning':out-rs,
  'edit_turn_output':edit_out,'edit_turn_nonreasoning':edit_nonreason,'edit_turns':edit_turns,'edit_calls':kinds,'edit_arg_bytes':edit_arg_bytes,'apply_patch_calls':kinds['apply_patch'],'apply_patch_errors':ap_err,
  'usd':s['usd_list'] if s.get('all_usage_present') else s['charge_upper_bound_usd']}
cells={};dry={}
for i,c in enumerate(protocol['cells']):
 x=load(R/c['stratum']/'cells'/c['task']/('r'+str(c['rep']))/c['arm'])
 if not x:continue
 x['index']=i
 (cells if c['stratum']=='counted' else dry)[(c['task'],c['rep'],c['arm'])]=x
blocks=[tuple(b) for b in protocol['blocks']]
done=[b for b in blocks if all((*b,a) in cells for a in ARMS)]
def p90(v):v=sorted(v);return v[max(0,math.ceil(.9*len(v))-1)]
def test(w,l,n_all):
 n=w+l;k=min(w,l);p=1. if n==0 else min(1.,2*sum(math.comb(n,i) for i in range(k+1))/2**n)
 return {'first_wins':w,'second_wins':l,'ties':n_all-n,'p':p}
def sign(a,b):return test(sum(x<y for x,y in zip(a,b)),sum(x>y for x,y in zip(a,b)),len(a))
def cpp(x):return x['usd'] if x['pass'] else math.inf  # cost per pass of one cell; two failures tie
TOT=('wall','requests','reasoning','output','nonreasoning','edit_turn_output','edit_turn_nonreasoning','edit_turns','edit_arg_bytes','apply_patch_calls','apply_patch_errors','usd')
per_arm={}
for a in ARMS:
 xs=[cells[(*b,a)] for b in blocks if (*b,a) in cells];np_=sum(x['pass'] for x in xs)
 tot={k:sum(x[k] for x in xs) for k in TOT}
 kinds={k:sum(x['edit_calls'][k] for x in xs) for k in ('write_file','apply_patch','shell_edit')};ne=sum(kinds.values())
 per_arm[a]={'launched':len(xs),'passes':np_,'median_wall':statistics.median(x['wall'] for x in xs) if xs else None,'p90_wall':p90([x['wall'] for x in xs]) if xs else None,'edit_calls':kinds,
  'cells_using_apply_patch':sum(x['apply_patch_calls']>0 for x in xs),'apply_patch_call_share':(kinds['apply_patch']/ne if ne else None),
  **{'total_'+k:v for k,v in tot.items()},'usd_per_pass':(tot['usd']/np_ if np_ else None),**{k+'_per_run':(v/len(xs) if xs else None) for k,v in tot.items()}}
METRICS=['edit_turn_output','usd_per_pass','wall','requests','output','nonreasoning','reasoning','edit_turns','usd']
def pair(a,b,bs):
 out={}
 for m in METRICS:
  fn=cpp if m=='usd_per_pass' else (lambda x,m=m:x[m])
  out[m]=sign([fn(cells[(*k,a)]) for k in bs],[fn(cells[(*k,b)]) for k in bs])
 da=[cells[(*k,a)]['pass'] for k in bs];db=[cells[(*k,b)]['pass'] for k in bs]
 out['pass']=test(sum(x and not y for x,y in zip(da,db)),sum(y and not x for x,y in zip(da,db)),len(bs))
 for m in ('edit_turn_output','output','usd','wall'):
  ra=[math.log(cells[(*k,a)][m]/cells[(*k,b)][m]) for k in bs if cells[(*k,a)][m]>0 and cells[(*k,b)][m]>0]
  out[m+'_geomean_ratio']=math.exp(sum(ra)/len(ra)) if ra else None
  out[m+'_geomean_n']=len(ra)
 out['usd_per_pass_ratio']=(per_arm[a]['usd_per_pass']/per_arm[b]['usd_per_pass']) if per_arm[a]['usd_per_pass'] and per_arm[b]['usd_per_pass'] else None
 out['edit_turn_output_total_ratio']=per_arm[a]['total_edit_turn_output']/per_arm[b]['total_edit_turn_output'] if per_arm[b]['total_edit_turn_output'] else None
 return out
COMP=[('apply-patch','loop-default'),('apply-patch','codex'),('loop-default','codex')]
pairs={f'{a} vs {b}':pair(a,b,done) for a,b in COMP}
by_task={t:{f'{a} vs {b}':pair(a,b,[k for k in done if k[0]==t]) for a,b in COMP} for t in protocol['tasks']}
probes=[json.loads(x) for x in (R/'probes.jsonl').read_text().splitlines()] if (R/'probes.jsonl').exists() else []
spend={'counted_usd':sum(x['usd'] for x in cells.values()),'dry_usd':sum(x['usd'] for x in dry.values()),'probes':len(probes),'probe_usd':sum(x.get('usd',0) for x in probes)}
spend['total_usd']=spend['counted_usd']+spend['dry_usd']+spend['probe_usd']
analysis={'protocol_sha256':hashlib.sha256((R/'protocol.json').read_bytes()).hexdigest(),'registered_tasks':protocol['tasks'],'reps':protocol['reps'],'completed_counted_cells':len(cells),'complete_blocks':[list(b) for b in done],'dry':{f'{t}/r{r}/{a}':x for (t,r,a),x in dry.items()},'per_arm':per_arm,
 'per_cell':{f'{t}/r{r}/{a}':cells[(t,r,a)] for (t,r) in blocks for a in ARMS if (t,r,a) in cells},'paired_sign_tests':pairs,'paired_by_task':by_task,'spend':spend,'cap_usd':protocol['round_cap_usd']}
(R/'edit5-analysis.json').write_text(json.dumps(analysis,indent=2,sort_keys=True,default=str)+'\n')

f=lambda v,d=3:'n/a' if v is None else f'{v:,.{d}f}'
L=[f"Counted cells {len(cells)}/{3*len(blocks)}, complete blocks {len(done)}/{len(blocks)} ({len(protocol['tasks'])} tasks x {protocol['reps']} reps); spend ${f(spend['total_usd'],6)} (counted ${f(spend['counted_usd'],6)}, dry ${f(spend['dry_usd'],6)}, {spend['probes']} probes ${f(spend['probe_usd'],6)}) / cap ${f(protocol['round_cap_usd'],2)}.",'']
L.append('| Arm | Pass / launched | Edit-turn output (total / per run) | Edit turns per run | Edit calls write_file / apply_patch / shell | apply_patch: cells using / call share / errors | Output total | Median / p90 wall s | Requests per run | USD total / per pass |')
L.append('| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |')
for a in ARMS:
 x=per_arm[a];k=x['edit_calls']
 L.append(f"| {LABEL[a]} (high) | {x['passes']} / {x['launched']} | {x['total_edit_turn_output']:,} / {f(x['edit_turn_output_per_run'],0)} | {f(x['edit_turns_per_run'],1)} | {k['write_file']} / {k['apply_patch']} / {k['shell_edit']} | {x['cells_using_apply_patch']}/{x['launched']} / {f(x['apply_patch_call_share'],2)} / {x['total_apply_patch_errors']} | {x['total_output']:,} | {f(x['median_wall'])} / {f(x['p90_wall'])} | {f(x['requests_per_run'],1)} | ${f(x['total_usd'],6)} / ${f(x['usd_per_pass'],6)} |")
L.append('');L.append('**Paired by block (lower is better; first-arm wins / second-arm wins, ties, exact two-sided sign test p). Primary: edit-turn output tokens, cost per pass. Secondary: wall, requests, pass.**');L.append('')
L.append('| Comparison | Edit-turn output | Cost per pass | Wall | Requests | Pass | Total output | Edit-turn output geomean ratio (n) | Total output ratio | USD/pass ratio | Wall ratio |');L.append('| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |')
g=lambda v:f"{v['first_wins']}/{v['second_wins']}, {v['ties']} ties, p={v['p']:.4f}"
for k,v in pairs.items():
 L.append(f"| {k} ({len(done)} blocks) | {g(v['edit_turn_output'])} | {g(v['usd_per_pass'])} | {g(v['wall'])} | {g(v['requests'])} | {g(v['pass'])} | {g(v['output'])} | {f(v['edit_turn_output_geomean_ratio'])} ({v['edit_turn_output_geomean_n']}) | {f(v['output_geomean_ratio'])} | {f(v['usd_per_pass_ratio'])} | {f(v['wall_geomean_ratio'])} |")
L.append('');L.append('**By task, apply-patch vs loop-default (edit-turn output wins / losses; geomean ratios).**');L.append('')
for t in protocol['tasks']:
 v=by_task[t]['apply-patch vs loop-default'];L.append(f"- {t}: edit-turn output {g(v['edit_turn_output'])}, ratio {f(v['edit_turn_output_geomean_ratio'])}; total output ratio {f(v['output_geomean_ratio'])}; USD ratio {f(v['usd_geomean_ratio'])}")
L.append('');L.append('**Per cell (edit-turn output / total output / edit calls w,a,s / USD / wall s / requests; pass).**');L.append('')
L.append('| Block | loop default | loop + apply_patch | Codex CLI |');L.append('| --- | --- | --- | --- |')
def cellrow(x):
 k=x['edit_calls'];return f"{x['edit_turn_output']:,} / {x['output']:,} / {k['write_file']},{k['apply_patch']},{k['shell_edit']} / ${f(x['usd'],4)} / {f(x['wall'],1)} / {x['requests']}; {'pass' if x['pass'] else 'fail ('+str(x['outcome'])+')'}"
for (t,r) in blocks:
 L.append(f'| {t} r{r} | '+' | '.join('not run' if (t,r,a) not in cells else cellrow(cells[(t,r,a)]) for a in ARMS)+' |')
for (t,r,a),x in sorted(dry.items(),key=lambda z:z[1]['index']):
 L.append(f'| dry {t} ({a}) | '+cellrow(x)+' | | |')
print('\n'.join(L))
