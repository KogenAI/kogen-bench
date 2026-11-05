import json,sys,statistics as S,re
D=sys.argv[1]  # dir holding A/ B/ C/ result.json and calib.log
solo={}
for l in open(D+'/calib.log'):
    m=re.match(r'(\S+) timed rc=(\d+) secs=([\d.]+)',l)
    if m: solo[m[1]]=(int(m[2]),float(m[3]))
def q(v,p): v=sorted(v); return v[min(len(v)-1,int(len(v)*p))]
out={}
for arm in 'ABC':
    try: r=json.load(open(f'{D}/{arm}/result.json'))
    except FileNotFoundError: continue
    recs=r['recs']; su=[x for x in recs if x['kind']=='suite']; sh=[x for x in recs if x['kind']=='shim']
    def agg(v,key):
        a=[x[key] for x in v if x.get(key) is not None]; return dict(n=len(a),median=round(S.median(a),1),mean=round(S.mean(a),1),p90=round(q(a,.9),1),sum=round(sum(a))) if a else None
    for x in recs: x['wr']=(x['wait'] or 0)+(x['run'] or 0)
    red=[x for x in su if x['rc'] and solo.get(x['suite'],(0,))[0]==0]
    out[arm]=dict(makespan=round(r['makespan']),suites=len(su),shim=len(sh),
      small_wait_run=agg([x for x in su if x['cls']=='small'],'wr'),large_wait_run=agg([x for x in su if x['cls']=='large'],'wr'),
      small_wait=agg([x for x in su if x['cls']=='small'],'wait'),all_wait=agg(recs,'wait'),shim_wait_run=agg(sh,'wr'),
      large_run=agg([x for x in su if x['cls']=='large'],'run'),
      small_run_vs_solo=round(S.median([x['run']/solo[x['suite']][1] for x in su if x['cls']=='small' and x['run'] and x['suite'] in solo]),2),
      false_red=len(red),false_red_suites=[(x['suite'],x['rc']) for x in red],all_rc_nonzero=[(x['kind'],x['suite'],x['rc']) for x in recs if x['rc']])
json.dump(out,open(D+'/e2-summary.json','w'),indent=1)
print(json.dumps(out,indent=1))
