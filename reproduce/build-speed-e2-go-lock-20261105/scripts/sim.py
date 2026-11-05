"""Trace-driven check of E2: replay the 48 h Go-lock arrivals (heavy.sh logs, mix-records.json) through FIFO lock policies A/B/C.
A = exclusive for all; B = small shared, large exclusive; C = B with large shared capped at 2. FIFO head-of-line like heavy.sh.
Concurrency slowdown model (assumption, not data): a run that starts with k other runs active takes d*(1+alpha*k) (alpha_small for small, alpha_large for large)."""
import json,heapq,collections,statistics as S,sys
R=json.load(open(sys.argv[1] if len(sys.argv)>1 else 'mix-records.json'))
LARGE_REPOS={'kogen','kogen-build','kogen-shaping','kogen-verification'}
def klass(r):
    if r['kind']=='shim': return 'small'
    if r['kind']=='build': return 'large' if r['repo'] in LARGE_REPOS else 'small'
    return 'large'          # land / adoption verify: monolith-sized suites
def sim(recs,arm,a_small,a_large,cap=2):
    recs=sorted(recs,key=lambda r:r['t']); q=collections.deque(); act=[]; t=0.0; i=0; waits=[]; end_last=0
    # act: heap of (end_time, id, cls); state
    ex=False; nsh=0; nlarge=0
    def start(r,now,cl):
        nonlocal ex,nsh,nlarge
        k=len(act); d=r['run']*(1+(a_large if cl=='large' else a_small)*k)
        waits.append((now-r['t'],cl,d,r['run'])); heapq.heappush(act,(now+d,id(r),cl,mode_of(cl)))
        m=mode_of(cl)
        if m=='ex': ex=True
        else: nsh+=1
        if cl=='large' and arm=='C': nlarge+=1
    def mode_of(cl): 
        if arm=='A': return 'ex'
        if cl=='small': return 'sh'
        return 'ex' if arm=='B' else 'sh'
    def admit(now):
        while q:
            r,cl=q[0]; m=mode_of(cl)
            ok=(not ex and nsh==0) if m=='ex' else (not ex)
            if ok and arm=='C' and cl=='large' and nlarge>=cap: ok=False
            if not ok: break
            q.popleft(); start(r,now,cl)
    while i<len(recs) or q or act:
        na=recs[i]['t'] if i<len(recs) else 1e18; ne=act[0][0] if act else 1e18
        if na<=ne:
            now=na; r=recs[i]; i+=1; q.append((r,klass(r))); admit(now)
        else:
            now=ne; e,_,cl,m=heapq.heappop(act)
            if m=='ex': ex=False
            else: nsh-=1
            if cl=='large' and arm=='C': nlarge-=1
            admit(now)
    return waits
out={}
for host in sorted({r['host'] for r in R}):
    H=[r for r in R if r['host']==host]
    if len(H)<200: continue
    out[host]={}
    obs=sum(r['wait'] for r in H)/3600
    out[host]['n']=len(H); out[host]['recorded_wait_h']=round(obs,1)
    for arm,a_s,a_l in [('A',0,0),('B',0,0),('B',0.15,1.0),('B',0.3,1.0),('C',0.15,1.0),('C',0.3,1.0),('B',0.5,1.0),('C',0.5,1.0)]:
        w=sim(H,arm,a_s,a_l)
        key=f'{arm} a_small={a_s} a_large={a_l}'
        tot=sum(x[0] for x in w)/3600; wr=sum(x[0]+x[2] for x in w)/3600
        sm=[x[0]+x[2] for x in w if x[1]=='small']; 
        out[host][key]=dict(wait_h=round(tot,1),wait_plus_run_h=round(wr,1),small_wait_run_median_s=round(S.median(sm),1))
print(json.dumps(out,indent=1)); json.dump(out,open(sys.argv[2] if len(sys.argv)>2 else 'sim-summary.json','w'),indent=1)
