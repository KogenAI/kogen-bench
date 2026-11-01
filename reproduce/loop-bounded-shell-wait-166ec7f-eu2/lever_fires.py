#!/usr/bin/env python3
"""Lever-fires check from the screen's own cell logs: per bcw-arm shell command, duration upper bound =
next request.started after its tool.call (events.jsonl, 1 s resolution); counts commands > 1 s that returned
'exit status' in the same response (on main these would have yielded a handle). Usage: lever_fires.py <round dir>"""
import json,sys,glob,datetime,collections
def ts(s):return datetime.datetime.strptime(s,"%Y-%m-%dT%H:%M:%SZ").timestamp()
out=collections.defaultdict(list)
for cell in sorted(glob.glob(sys.argv[1]+'/counted/cells/*/*/*')):
    arm=cell.rsplit('/',1)[1]
    ev=[json.loads(l) for l in open(cell+'/events.jsonl')]
    reqs=sorted(ts(e['time']) for e in ev if e.get('type')=='request.started')
    ct={e['call_id']:ts(e['time']) for e in ev if e.get('type')=='tool.call'}
    calls={};heads={}
    for l in open(cell+'/tool-items.jsonl'):
        x=json.loads(l)
        if x.get('kind')=='call':calls[x['call_id']]=x
        if x.get('kind')=='output':heads[x['call_id']]=x['head']
    for cid,c in calls.items():
        if c['name']!='shell' or '"command"' not in c['arguments'][:20] or cid not in ct:continue
        h=heads.get(cid,'')
        nxt=next((r for r in reqs if r>ct[cid]),None)
        out[arm].append((round(nxt-ct[cid]) if nxt else None,'sync' if h.startswith('exit status') else 'handle'))
for arm,v in out.items():
    d=[x for x,k in v if k=='sync' and x is not None]
    print(arm,'commands',len(v),'returned completed',sum(k=='sync' for _,k in v),'handles',sum(k=='handle' for _,k in v),
          'completed with duration bound >1 s:',sum(x>1 for x in d),'>10 s:',sum(x>10 for x in d),'>30 s:',sum(x>30 for x in d),'max',max(d) if d else None)
