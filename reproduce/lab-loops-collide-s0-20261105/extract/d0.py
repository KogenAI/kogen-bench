import re,json,collections,sys
sys.path.insert(0,'scripts')
from parse import fleet,opstick,ep
STATUS_ONLY=('OVERLOAD','EXPERIMENTS_LOW','UNDERSPEND')
def key(line):
    p=line.split()
    return ' '.join(p[:3] if p[:2]==['PUBLISH_STALE','finding'] else p[:2]) if len(p)>1 else line.strip()
def timeline():
    """per ops-tick tick: epoch, list of red lines (from fleet-check, STATUS_ONLY removed), logged red/sent"""
    # format 2 lines grouped by ts
    g=collections.defaultdict(list)
    for l in open('in/fleet-check.log',errors='replace'):
        m=re.match(r'(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ) (.*)',l.rstrip('\n'))
        if m: g[m.group(1)].append(m.group(2))
    fts=sorted(g)
    fe=[ep(t) for t in fts]
    import bisect
    ticks=[]
    for o in opstick():
        i=bisect.bisect_right(fe,o['e'])-1
        lines=[]
        if i>=0 and o['e']-fe[i]<=300: lines=g[fts[i]]
        # drop ones consumed by an earlier ops-tick? (each fleet ts once)
        ticks.append(dict(o,lines=lines,fts=fts[i] if lines else None))
    return ticks,g
if __name__=='__main__':
    ticks,g=timeline()
    # use only ticks in format-2 coverage
    cov=[t for t in ticks if t['e']>=ep('2026-10-31T13:08:02Z')]
    ok=0;bad=[]
    for t in cov:
        L=[l for l in t['lines'] if l.split(' ',1)[0] not in STATUS_ONLY]
        # ACKED/POLICY_OK are not red lines?
        t['red_calc']=len(L)
        if len(L)==t['red']: ok+=1
        else: bad.append((t['t'],len(L),t['red'],t['sent']))
    print(len(cov),ok); print(bad[:15])
