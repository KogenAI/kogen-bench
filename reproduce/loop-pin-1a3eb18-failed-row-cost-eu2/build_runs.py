"""usage: build_runs.py <out dir> <label>=<round dir>[:arm] ...
Per-cell rows (runs.csv) and the full per-cell analysis (cells.json) from round directories (events.jsonl, route-receipts.jsonl, tool-items.jsonl,
result.json, evaluation.json per cell). Uses analyze_loopnp.py in this directory plus a count of shell polls (calls carrying a handle)."""
import csv,json,sys,pathlib,collections
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
import analyze_loopnp as A
def polls(d):
 d=pathlib.Path(d);f=d/'tool-items.jsonl'
 out=dict(commands=0,polls=0,yielded=0,refused=0,poll_only_requests=0,poll_only_usd=0.,poll_only_model_s=0.,poll_same_size=0,max_polls_one_handle=0)
 if not f.exists():return out
 items=[json.loads(x) for x in f.read_text().splitlines()]
 calls={i['call_id']:i for i in items if i.get('kind')=='call'};outs={i['call_id']:i for i in items if i.get('kind')=='output'}
 last={};per=collections.Counter()
 for cid,c in calls.items():
  if c['name']!='shell':continue
  a=c['arguments'];o=outs.get(cid,{});h=o.get('head','')
  if h.startswith('error: supply exactly one'):out['refused']+=1
  if a.startswith('{"handle"'):
   out['polls']+=1;hd=json.loads(a)['handle'];per[hd]+=1
   if hd in last and last[hd]==o.get('bytes'):out['poll_same_size']+=1
   last[hd]=o.get('bytes')
  else:
   out['commands']+=1
   if h.startswith('{"handle"'):
    out['yielded']+=1;m=__import__('re').match(r'\{"handle":"([0-9a-f]+)"',h)
    if m:last[m.group(1)]=o.get('bytes')
 ev=A.jl(d/'events.jsonl');ev_att=[j['record'] for j in ev if j['type']=='request.attempt'];rc=[x for x in A.jl(d/'route-receipts.jsonl') if x.get('forwarded')]
 by=collections.defaultdict(list);n=0
 for j in ev:
  if j['type']=='request.started':n=j['n']
  elif j['type']=='tool.call':by[n].append((j['call_id'],j['name']))
 for k,x in enumerate(rc,1):
  ks=by.get(k,[])
  if ks and all(nm=='shell' and calls.get(cid,{}).get('arguments','').startswith('{"handle"') for cid,nm in ks):
   u=x['usage'];dd=u.get('input_tokens_details') or {};i=u['input_tokens'];c=dd.get('cached_tokens',0)
   out['poll_only_requests']+=1;out['poll_only_model_s']+=ev_att[k-1]['wall_ms']/1000;out['poll_only_usd']+=((i-c)+c*.05+dd.get('cache_write_tokens',0)*.25+u['output_tokens']*5)/1e6

 out['max_polls_one_handle']=max(per.values(),default=0)
 return out
if __name__=='__main__':
 out=pathlib.Path(sys.argv[1]);rows=[];cells={}
 for a in sys.argv[2:]:
  label,rest=a.split('=',1);arm=None
  if ':' in rest:rest,arm=rest.rsplit(':',1)
  root=pathlib.Path(rest)
  for r in sorted(root.glob('counted/cells/*/r*/*/result.json')):
   d=r.parent
   if arm and d.name!=arm:continue
   c=A.cellstats(d);p=polls(d);cells[label+'/'+c['cell']]=dict(c,shell=p)
   rows.append(dict(set=label,cell=c['cell'],outcome=c['outcome'],passed=int(bool(c['passed'])),wall_s=c['wall_s'],requests=c['requests'],usd=c['usd'],input_tokens=c['input'],cached_tokens=c['cached'],
    output_tokens=c['output'],reasoning_tokens=c['reasoning'],model_s=c['model_s'],gap_s=c['gap_total_s'],max_gap_s=c['gap_max_s'],gaps_over_30s=len(c['gaps_gt30']),max_request_bytes=c['max_request_bytes'],
    condensed=c['condensed'],shell_commands=p['commands'],shell_yielded=p['yielded'],shell_polls=p['polls'],poll_only_requests=p['poll_only_requests'],poll_only_usd=round(p['poll_only_usd'],5),poll_only_model_s=round(p['poll_only_model_s'],1),poll_same_size=p['poll_same_size'],max_polls_one_handle=p['max_polls_one_handle'],refused_command_and_handle=p['refused'],failed_ids=len(c['failed_ids']),errors=';'.join(e['reason'] or '' for e in c['error_events'])))
 with (out/'runs.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 (out/'cells.json').write_text(json.dumps(cells,indent=1,sort_keys=True))
 print(len(rows),'rows')
