"""Extract the published data files from the raw local logs (not published: operational logs)."""
import sys,json,collections,datetime as dt,re
sys.path.insert(0,'scripts')
from d0 import timeline
from parse import ep
ticks,g=timeline()
START=ep('2026-10-31T13:08:02Z')
out=[]
for t in ticks:
    out.append(dict(t=t['t'],obs_sent=t['sent'],failed=t['failed'],red_logged=t['red'],in_line_window=t['e']>=START,
                    lines=[' '.join(l.split()[:6]) for l in t['lines']] if t['e']>=START else []))
json.dump(out,open('pack/data/ticks.json','w'))
# main stream daily counts (no message text)
o=json.load(open('out/main-msgs.json'))
daily=collections.defaultdict(lambda:collections.Counter())
for m in o:
    d=m['ts'][:10]
    if d<'2026-10-30': continue
    c=daily[d]
    if m['dir']=='in':
        c['in_relay' if m['relay'] else ('in_delivery' if m['peer']=='kogen-delivery' else ('in_research' if m['peer']=='kogen-research-owner' else 'in_other'))]+=1
    else:
        c['out_delivery' if m['peer']=='kogen-delivery' else ('out_research' if m['peer']=='kogen-research-owner' else 'out_other')]+=1
    if not m['relay'] and m['codes']: c['steward_names_alarm_code']+=1
casc=json.load(open('out/main-stream-summary.json'))
for d,v in casc.items():
    daily[d]['forwards_after_relay_same_code']=v['forwards_after_relay_same_code']; daily[d]['restated_in_6h']=v['restated_in_6h']
json.dump({d:dict(c) for d,c in sorted(daily.items())},open('pack/data/main-stream-daily.json','w'),indent=1)
# admit summary
def e2(t): return dt.datetime.strptime(t,'%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=dt.timezone.utc).timestamp()
rows=[l.rstrip('\n').split('\t') for l in open('in/admit-log.tsv')]
adm=[r for r in rows if r[2]!='queue']
callers=collections.Counter(r[4].split(':')[0] for r in adm if len(r)>4)
d=collections.defaultdict(list)
for r in adm:
    p=r[4].split(':')
    if len(p)>=3 and p[0]=='delivery': d[p[2]].append((e2(r[0]),p[1],r[0]))
diff=[];same=0
for k,v in d.items():
    v.sort()
    for a,b in zip(v,v[1:]):
        if b[0]-a[0]<=3600:
            if a[1]!=b[1]: diff.append((k,a[1],b[1],a[2],round((b[0]-a[0])/60)))
            else: same+=1
json.dump(dict(rows=len(rows),admitted_rows=len(adm),hold_rows=len(rows)-len(adm),first=rows[0][0],last=rows[-1][0],
   admitted_by_delivery=sum(len(v) for v in d.values()),items_admitted_by_delivery=len(d),
   admitted_rows_by_other_caller=sum(v for k,v in callers.items() if k!='delivery'),
   items_started_on_two_hosts_within_60min=len(diff),pairs_same_host_within_60min=same,
   pairs_diff_host_within_60min=[dict(item=a,from_host=b,to_host=c,at=t,gap_min=gm) for a,b,c,t,gm in diff]),open('pack/data/admit-summary.json','w'),indent=1)
# fleet-acks (ack rows)
acks=[l.rstrip('\n').split('\t') for l in open('in/fleet-acks.tsv')]
json.dump([dict(code=a[0],subject=a[1],role=a[2],until=a[3]) for a in acks if len(a)>=4],open('pack/data/fleet-acks.json','w'),indent=1)
print(len(out),len(acks))
