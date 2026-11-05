import json,collections,datetime as dt
def ep(t): return dt.datetime.strptime(t[:19],'%Y-%m-%dT%H:%M:%S').replace(tzinfo=dt.timezone.utc).timestamp()
o=json.load(open('out/main-msgs.json'))
for m in o: m['e']=ep(m['ts']); m['cs']={tuple(c) for c in m['codes']}
o.sort(key=lambda m:m['e'])
relays=[m for m in o if m['relay']]
allst=[m for m in o if not m['relay'] and m['cs']]
res={}
for d in ('2026-10-31','2026-11-01','2026-11-02','2026-11-03','2026-11-04'):
    x=[m for m in o if m['ts'].startswith(d)]
    steward=[m for m in x if not m['relay']]
    withcode=[m for m in steward if m['cs']]
    casc=0
    for m in [y for y in x if y['dir']=='out' and y['cs']]:
        recent=set()
        for r in relays:
            if 0<m['e']-r['e']<=1800: recent|=r['cs']
        if m['cs']&recent: casc+=1
    rest=0
    for m in withcode:
        prev=set()
        for r in allst:
            if r is m: continue
            if 0<m['e']-r['e']<=6*3600: prev|=r['cs']
        if m['cs']&prev: rest+=1
    res[d]=dict(main_involved=len(x),relays=sum(1 for y in x if y['relay']),steward=len(steward),steward_with_alarm_code=len(withcode),forwards_after_relay_same_code=casc,restated_in_6h=rest,main_out=sum(1 for y in x if y['dir']=='out'))
    print(d,res[d])
json.dump(res,open('out/main-stream-summary.json','w'),indent=1)
