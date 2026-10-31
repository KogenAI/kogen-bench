# Per-run replay: baseline reuse across restarts, command concurrency, impact-selected repeats, fixer cadence and staged scope.
# Usage: python3 -I analyze_runs.py DATADIR   (DATADIR holds runs.json.gz). Standard library only.
import json,collections,gzip,sys
R=json.load(gzip.open(sys.argv[1]+'/runs.json.gz','rt'))
LONG={'test','go-test','spec','cucumber','acceptance','no-home-paths'}
tot=collections.Counter()
def p(*a): print(*a)
# overall by kind
for r in R:
    for c in r['cmds']: tot[c['kind']]+=c['secs']
p('secs by kind',{k:round(v) for k,v in tot.items()})
# --- M2 baseline reuse same head, same host, cmd
b=collections.defaultdict(list)
for r in R:
    for c in r['cmds']:
        if c['kind']=='baseline': b[(r['head'],c['check'],r['host'])].append((c['t0'],c['secs'],c['ok'],r['run'],r['tree']))
n=s=mixed=0; sk=collections.Counter();skn=collections.Counter()
for k,v in b.items():
    v.sort(); 
    first_ok=None
    for t0,secs,ok,run,tree in v:
        if first_ok is not None:
            n+=1;s+=secs;sk[k[1]]+=secs; skn[k[1]]+=1
        if ok and first_ok is None: first_ok=t0
    oks={x[2] for x in v}
    if len(oks)>1: mixed+=1
p('M2 same head+check+host: reusable-after-pass execs',n,'secs',round(s),'; groups w/ mixed outcome',mixed,'of',len(b))
p(' by check',{k:(skn[k],round(sk[k])) for k in sk})
# identity completeness: how many baseline execs have head? env? 
# --- per-pass structure
npass=0; wall=0; sumsecs=0; conc_saved=0; passes_n=0
repeat_fail=0;repeat_fail_secs=0;nobuilder=0;nobuilder_secs=0
reexec_pass_secs=0;reexec_n=0; inter_full=0; inter_full_n=0
fixer=[]
for r in R:
    P=r['passes']
    if not P: continue
    for i,pp in enumerate(P):
        cs=[c for c in r['cmds'] if c['kind']=='verify' and c['pass_']==pp['n']]
        if not cs: continue
        passes_n+=1
        w=max(c['t1'] for c in cs)-min(c['t0'] for c in cs)
        sm=sum(c['secs'] for c in cs)
        wall+=w;sumsecs+=sm
        # independent concurrency ideal: all non-setup checks concurrent => max secs ; setup excluded
        chk=[c for c in cs if not c['check'].startswith('setup')]
        setup=sum(c['secs'] for c in cs if c['check'].startswith('setup'))
        if chk:
            ideal=setup+max(c['secs'] for c in chk)
            conc_saved+=max(0,w-ideal)
    # re-exec: passes>=2: commands that passed in previous pass
    for i in range(1,len(P)):
        prev=[c for c in r['cmds'] if c['kind']=='verify' and c['pass_']==P[i-1]['n'] and c['check'] in LONG|{'format','compile'}]
        okprev={c['check'] for c in prev if c['ok']}
        cur=[c for c in r['cmds'] if c['kind']=='verify' and c['pass_']==P[i]['n'] and c['check'] in okprev]
        last = i==len(P)-1
        s_=sum(c['secs'] for c in cur)
        if not last or not P[i]['green']:
            reexec_pass_secs+=s_;reexec_n+=len(cur)
        else:
            inter_full+=s_
        # same failing set as previous
        if P[i]['failing']==P[i-1]['failing'] and P[i]['failing']:
            repeat_fail+=1
            repeat_fail_secs+=sum(c['secs'] for c in r['cmds'] if c['kind']=='verify' and c['pass_']==P[i]['n'])
            if r['rb'].get(str(P[i-1]['n']),0)==0:
                nobuilder+=1;nobuilder_secs+=sum(c['secs'] for c in r['cmds'] if c['kind']=='verify' and c['pass_']==P[i]['n'])
p('verify passes with commands',passes_n,'wall',round(wall),'sum',round(sumsecs),'conc ideal saving (upper, independence UNKNOWN)',round(conc_saved))
p('M4 re-executed prev-green checks in non-final-or-red passes: n',reexec_n,'secs',round(reexec_pass_secs),'; in final green pass (must stay)',round(inter_full))
p('M5 passes whose failing set == previous failing set: n',repeat_fail,'secs',round(repeat_fail_secs),'| with 0 executor rounds started between (no builder edit seen)',nobuilder,round(nobuilder_secs))
# passes/run, outcomes
c=collections.Counter(len(r['passes']) for r in R);p('passes/run',sorted(c.items()))
c=collections.Counter((r['outcome']) for r in R);p('outcomes',c)
c=collections.Counter(r['executor'] for r in R);p('executors',c)
# fail-stop: how many verify passes have not_run
nr=[(pp['n'],pp['not_run']) for r in R for pp in r['passes'] if pp['not_run']]
p('passes with not_run (fail-stop gating present):',len(nr),'of',sum(len(r['passes']) for r in R))
# M6: seconds of verify-pass checks that ran in a red pass but were not the failing check (info not needed to repair)
red=0;redn=0
for r in R:
    for pp in r['passes']:
        if pp['green']:continue
        for c in r['cmds']:
            if c['kind']=='verify' and c['pass_']==pp['n'] and c['check'] in LONG|{'compile','format'} and c['check'] not in pp['failing']:
                red+=c['secs'];redn+=1
p('M6 passing checks executed inside red passes: n',redn,'secs',round(red))
# time in red passes total vs green passes
rs=gs=0
for r in R:
    for pp in r['passes']:
        s_=sum(c['secs'] for c in r['cmds'] if c['kind']=='verify' and c['pass_']==pp['n'])
        if pp['green']: gs+=s_
        else: rs+=s_
p('verify secs in red passes',round(rs),'in green passes',round(gs))
# per-check totals verify vs baseline
t=collections.defaultdict(lambda:[0,0.0,0,0.0])
for r in R:
    for c in r['cmds']:
        if c['kind']=='verify': t[c['check']][0]+=1;t[c['check']][1]+=c['secs']
        elif c['kind']=='baseline': t[c['check']][2]+=1;t[c['check']][3]+=c['secs']
for k,v in sorted(t.items(),key=lambda x:-x[1][1]-x[1][3])[:14]: p(' ',k,'verify n',v[0],round(v[1]),'baseline n',v[2],round(v[3]))

p('--- mixed-outcome same head/check/host groups')
for k,v in b.items():
    if len({x[2] for x in v})>1: p(k[0][:8],k[1],k[2],[(round(x[1]),x[2],x[3],x[4]) for x in sorted(v)])
p('--- repeated failing sets')
for r in R:
    P=r['passes']
    for i in range(1,len(P)):
        if P[i]['failing'] and P[i]['failing']==P[i-1]['failing']:
            p(r['run'],r['tree'],r['host'],'pass',P[i]['n'],P[i]['failing'],'rounds between',r['rb'].get(str(P[i-1]['n']),0),'pass secs',round(sum(c['secs'] for c in r['cmds'] if c['kind']=='verify' and c['pass_']==P[i]['n'])))
fc=collections.Counter()
for r in R:
    for pp in r['passes']:
        for f in pp['failing']: fc[f]+=1
p('failing checks in passes',fc)
bf=collections.Counter()
for r in R:
    for c in r['cmds']:
        if c['kind']=='baseline' and not c['ok']: bf[c['check']]+=1
p('baseline failing',bf)
