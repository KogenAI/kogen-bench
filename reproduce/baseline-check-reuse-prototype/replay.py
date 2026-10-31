# Replay of the prototype reuse rules over recorded delivery baseline executions. Model-free, read-only.
# Usage: python3 -I replay.py DATADIR   (DATADIR holds runs.json.gz). Key surrogate = (start tree id, check, task); environment fields are unknown.
import json,collections
import gzip,sys
R=json.load(gzip.open(sys.argv[1]+'/runs.json.gz','rt'))
MAXAGE=24*3600
g=collections.defaultdict(list)
tot_base=0; n_base=0
for r in R:
    for c in r['cmds']:
        if c['kind']=='baseline':
            tot_base+=c['secs']; n_base+=1
            g[(r['head'],c['check'],r['host'])].append((c['t0'],c['secs'],c['ok'],r['run']))
def sim(poison,age):
    hits=[];stored=None;res=[]
    for k,v in g.items():
        v.sort(); passes=[];fails=0
        for t0,secs,ok,run in v:
            usable=passes and (not poison or fails==0) and (not age or t0-passes[-1][0]<=MAXAGE)
            # a restart run reuses only results of an EARLIER run (not itself)
            usable=usable and passes[-1][2]!=run
            if usable: hits.append((k,t0,secs,passes[-1][1],run,ok))
            if ok: passes.append((t0,secs,run))
            else: fails+=1
    return hits
# restart baseline = executions at a (head,host) group's later runs
restart_secs=0;restart_n=0
for k,v in g.items():
    runs=[]
    for t0,secs,ok,run in sorted(v):
        if run not in runs: runs.append(run)
        if runs.index(run)>0: restart_secs+=secs;restart_n+=1
print('baseline execs',n_base,'secs',round(tot_base),'| restart-run execs',restart_n,'secs',round(restart_secs))
for name,po,ag in [('naive any prior pass',False,False),('+poison on any prior fail (prototype)',True,False),('+poison +24h max age (prototype)',True,True)]:
    h=sim(po,ag)
    sk=sum(x[2] for x in h)        # seconds actually skipped (this execution's recorded secs)
    ss=sum(x[3] for x in h)        # prototype's saved_secs (stored pass's secs)
    ge300=sum(1 for x in h if x[2]>=300)
    hid=sum(1 for x in h if not x[5])  # hit where the real execution FAILED (would-be hidden red)
    print(f'{name}: hits {len(h)} of {n_base} baseline execs (fire rate {len(h)/n_base:.1%}; of restart execs {len(h)/restart_n:.1%}) skipped {sk:.0f}s = {sk/tot_base:.1%} of baseline, {sk/restart_secs:.1%} of restart baseline; stored-secs {ss:.0f}; hits>=300s {ge300}; hits where the real run FAILED {hid}')
    if po and ag:
        by=collections.Counter();bs=collections.Counter()
        for x in h: by[x[0][1]]+=1;bs[x[0][1]]+=x[2]
        print('  by check',{k:(by[k],round(bs[k])) for k in by})
        print('  hits per group:',collections.Counter((x[0][0][:8],x[0][2]) for x in h).most_common(12))
