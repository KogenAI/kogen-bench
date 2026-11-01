"""Model-free per-cell analysis of loop cells (events.jsonl, tool-trace.jsonl, route-receipts.jsonl, result.json, evaluation.json).
usage: python3 -I analyze_loopnp.py <out.json> <label>=<mirror dir>[:arm] ...   (arm default: every arm; loopnight base cells = 'base')
Prices (confirmation_ext.cost): input 1.0, cached 0.05, cache write 1.25, output 5.0 $/M (x2 / x1.5 above 272k input)."""
import json,sys,pathlib,statistics,collections,datetime
def T(x):return datetime.datetime.fromisoformat(x.replace('Z','+00:00')).timestamp()
def jl(p):
 out=[]
 try:
  for l in open(p):
   try:out.append(json.loads(l))
   except ValueError:pass
 except OSError:pass
 return out
def cellstats(d):
 d=pathlib.Path(d)
 res=json.loads((d/'result.json').read_text())
 ev=jl(d/'events.jsonl');tt=jl(d/'tool-trace.jsonl');rc=[x for x in jl(d/'route-receipts.jsonl') if x.get('forwarded')]
 evl=json.loads((d/'evaluation.json').read_text()) if (d/'evaluation.json').exists() else {}
 st=json.loads((d/'status.json').read_text()) if (d/'status.json').exists() else {}
 s=res['stages'][0] if res.get('stages') else {}
 c={'cell':res['cell'],'outcome':res['outcome'],'passed':res['all_passed'],'wall_s':s.get('wall_s') or res.get('wall_s'),'requests':len(rc),'errors':res.get('errors'),'exit':res.get('exit_code'),
  'agent_outcome':st.get('agent_outcome'),'clean_agent_completion':st.get('clean_agent_completion')}
 ins=[];tot=dict(new=0.,write=0.,cached=0.,out=0.);I=C=W=O=Rz=0
 for x in rc:
  u=x['usage'];i=u['input_tokens'];dd=u.get('input_tokens_details') or {};ca=dd.get('cached_tokens',0);w=dd.get('cache_write_tokens',dd.get('cache_creation_tokens',0));o=u['output_tokens']
  rz=(u.get('output_tokens_details') or {}).get('reasoning_tokens',0)
  f=2 if i>272000 else 1;g=1.5 if i>272000 else 1
  tot['new']+=(i-ca)*f/1e6;tot['write']+=w*.25*f/1e6;tot['cached']+=ca*.05*f/1e6;tot['out']+=o*5*g/1e6
  ins.append(i);I+=i;C+=ca;W+=w;O+=o;Rz+=rz
 usd=sum(tot.values())
 c.update(usd=round(usd,5),input=I,cached=C,write=W,output=O,reasoning=Rz,max_input=max(ins) if ins else 0,
  share={k:round(v/usd,3) for k,v in tot.items()} if usd else None,cached_frac=round(C/I,3) if I else None,
  first_input=ins[0] if ins else None,last_input=ins[-1] if ins else None,
  growth_per_req=round((ins[-1]-ins[0])/(len(ins)-1)) if len(ins)>1 else None,
  new_input_per_req=round((I-C)/len(ins)) if ins else None,
  max_request_bytes=max((x.get('client_request_bytes') or 0) for x in rc) if rc else 0,
  statuses=dict(collections.Counter(str(x.get('status')) for x in rc)),http=dict(collections.Counter(str(x.get('http_status')) for x in rc)))
 att=[j['record'] for j in ev if j['type']=='request.attempt']
 c['attempts']=len(att);c['attempt_outcomes']=dict(collections.Counter(a.get('outcome') for a in att));c['end_reasons']=dict(collections.Counter(a.get('end_reason') for a in att))
 c['attempt_errors']=[a['error'] for a in att if a.get('error')][:5]
 c['model_s']=round(sum(a.get('wall_ms',0) for a in att)/1000,1)
 tt1=[a['ttft_ms'] for a in att if a.get('ttft_ms') is not None]
 c['ttft_mean_s']=round(statistics.mean(tt1)/1000,2) if tt1 else None
 c['max_attempt_s']=round(max((a.get('wall_ms',0) for a in att),default=0)/1000,1)
 c['max_gap_s']=round(max((a.get('max_gap_ms',0) for a in att),default=0)/1000,1)
 names=collections.Counter(j['name'] for j in ev if j['type']=='tool.call');c['tools']=dict(names)
 # client-side gap after each response: attempt timestamp = request start, wall_ms = attempt duration (validated against tool-trace to 3 ms)
 gaps=[];turn_tools=collections.defaultdict(list);n=0
 for j in ev:
  if j['type']=='request.started':n=j['n']
  elif j['type']=='tool.call':turn_tools[n].append(j['name'])
 for k in range(len(att)-1):
  g=T(att[k+1]['timestamp'])-T(att[k]['timestamp'])-att[k]['wall_ms']/1000
  gaps.append({'turn':k+1,'gap_s':round(g,2),'tools':turn_tools.get(k+1,[])})
 c['gap_total_s']=round(sum(x['gap_s'] for x in gaps),1)
 by=collections.defaultdict(float)
 for x in gaps:by['+'.join(sorted(set(x['tools']))) or 'none']+=x['gap_s']
 c['gap_by_tools']={k:round(v,1) for k,v in sorted(by.items(),key=lambda kv:-kv[1])[:6]}
 c['gaps_gt30']=[x for x in gaps if x['gap_s']>30];c['gap_max_s']=max((x['gap_s'] for x in gaps),default=0)
 shg=[x['gap_s'] for x in gaps if 'shell' in x['tools']];c['shell_turns']=len(shg);c['shell_turn_max_s']=max(shg,default=0)
 c['shell_turn_gt30']=sum(1 for v in shg if v>30);c['shell_turn_gt60']=sum(1 for v in shg if v>60)
 c['tool_total_s']=c['gap_total_s']
 if c['wall_s']:
  c['model_frac']=round(c['model_s']/c['wall_s'],3);c['tool_frac']=round(c['tool_total_s']/c['wall_s'],3);c['other_s']=round(c['wall_s']-c['model_s']-c['tool_total_s'],1)
 err=[j for j in ev if j['type']=='error'];c['error_events']=[{'reason':j.get('reason'),'class':j.get('class'),'detail':(j.get('detail') or '')[:200]} for j in err]
 re_=[j for j in ev if j['type']=='round.ended'];c['round_ended']=[{k:(v if k!='claim' else str(v)[:80]) for k,v in j.items() if k in('reason','status','claim','steps','finish')} for j in re_]
 c['condensed']=sum(1 for j in ev if j['type']=='context.condensed');c['event_types']=dict(collections.Counter(j['type'] for j in ev))
 order=[j['name'] for j in ev if j['type']=='tool.call']
 c['write_calls']=sum(1 for n in order if n in('write_file','edit_file','apply_patch','replace_in_file'))
 c['failed_ids']=evl.get('failed') or [];c['missing']=len(evl.get('missing') or []);c['timed_out_ids']=evl.get('timed_out') or []
 c['eval_totals']=evl.get('totals');c['infrastructure']=evl.get('infrastructure')
 c['commands']=[(x['name'],x['ok'],x['status'],x['timed_out']) for x in (evl.get('commands') or [])]
 return c
def load(root,arm=None):
 root=pathlib.Path(root);rows=[]
 for r in sorted(root.glob('counted/cells/*/r*/*/result.json')):
  d=r.parent
  if arm and d.name!=arm:continue
  rows.append(cellstats(d))
 return rows
if __name__=='__main__':
 out={}
 for a in sys.argv[2:]:
  label,rest=a.split('=',1);arm=None
  if ':' in rest:rest,arm=rest.rsplit(':',1)
  out[label]=load(rest,arm)
 pathlib.Path(sys.argv[1]).write_text(json.dumps(out,indent=1,sort_keys=True))
 for k,v in out.items():print(k,len(v),'cells')
