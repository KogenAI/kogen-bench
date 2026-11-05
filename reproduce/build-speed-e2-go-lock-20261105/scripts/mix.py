# Arrival mix of Go-lock users over the 48-h window, from the recorded heavy.sh logs (no live host touched).
import re,glob,json,collections,statistics as S,datetime as dt,sys
B=sys.argv[1].rstrip('/')+'/'  # the recorded heavy.sh log extract dir (joined.json); private, not in this pack
T0=dt.datetime(2026,11,3,9,tzinfo=dt.timezone.utc); T1=dt.datetime(2026,11,5,9,tzinfo=dt.timezone.utc)
J=json.load(open(B+'joined.json')); slug2repo={r['slug']:r['repo'] for r in J}
recs=[]
for f in glob.glob(B+'heavy-*.log'):
    h=f.split('heavy-')[-1][:-4]; L=open(f).read().splitlines()
    end=dt.datetime.strptime(L[-1].split()[1],'%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=dt.timezone.utc)
    day=end.date(); prev=None; ev=[]
    for l in reversed(L[:-1]):
        m=re.match(r'(\d\d):(\d\d):(\d\d)Z (\d+) (\S+) (.*)',l)
        if not m: continue
        s=int(m[1])*3600+int(m[2])*60+int(m[3])
        if prev is not None and s>prev+3600: day-=dt.timedelta(days=1)
        prev=s
        t=dt.datetime.combine(day,dt.time(),tzinfo=dt.timezone.utc)+dt.timedelta(seconds=s)
        if t<T0-dt.timedelta(hours=3): break
        ev.append((t,m[4],m[5],m[6]))
    ev.reverse(); w={}
    for t,pid,e,rest in ev:
        path=rest.split()[-1]
        if e.startswith('wait'): w[pid]=(t,path,e)
        elif e=='run' and pid in w: w[pid]=w[pid]+(t,)
        elif e=='end' and pid in w and len(w[pid])==4:
            wt,p,we,rt=w.pop(pid); m2=re.match(r'rc=(\d+) (\d+)s',rest)
            if m2 and T0<=rt<=T1: recs.append(dict(host=h,t=(wt-T0).total_seconds(),wait=(rt-wt).total_seconds(),run=int(m2[2]),rc=int(m2[1]),path=p,mode=we))
def cls(p):
    if 'lanes-grade' in p or 'grade.sh' in p or 'hv' in p.rsplit('/',1)[-1][:2]: return None
    m=re.search(r'heavy-cmds/([^/]+)/go-test\.sh',p)
    if m: return ('build',slug2repo.get(m[1]) or None,m[1])
    m=re.search(r'verify-.*landtree-land-([\w-]+)|verify-.*(kogen-[\w]+|loop)',p)
    if 'landtree' in p or '/logs/verify-' in p:
        m=re.search(r'land-?(kogen-[a-z]+|loop|studio|kogen)\b',p); return ('land',m[1] if m else '?',p.rsplit('/',1)[-1])
    if 'go-shim' in p: return ('shim',None,'')
    return None
out=[]
for r in recs:
    c=cls(r['path'])
    if c and r['mode']!='wait-ex-mix' and 'mix' not in r['mode']: r.update(kind=c[0],repo=c[1],slug=c[2]); out.append(r)
json.dump(out,open('mix-records.json','w'))
g=collections.defaultdict(list)
for r in out: g[(r['kind'],r['repo'] if r['kind']!='shim' else '-')].append(r)
print('kind repo n run_med run_p90 fail% wait_med wait_sum_h')
for k,v in sorted(g.items(),key=lambda x:-len(x[1])):
    run=sorted(x['run'] for x in v); wt=[x['wait'] for x in v]
    print(f"{k[0]:6} {str(k[1]):20} {len(v):5} {S.median(run):6.0f} {run[int(len(run)*.9)]:6} {100*sum(1 for x in v if x['rc'])/len(v):4.0f}% {S.median(wt):6.0f} {sum(wt)/3600:5.1f}")
print(len(out))
