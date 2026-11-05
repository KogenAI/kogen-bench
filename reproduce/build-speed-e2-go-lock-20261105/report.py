#!/usr/bin/env python3
"""Regenerates the E2 numbers in README.md from data/: host availability from the EU monitor, calibration lines, and the trace-driven
lock-policy simulation (scripts/sim.py on data/mix-records.json). Run: python3 -I report.py   (from this directory)"""
import json,os,statistics as S,subprocess,sys
D=os.path.join(os.path.dirname(os.path.abspath(__file__)),'data'); X=os.path.join(os.path.dirname(os.path.abspath(__file__)),'scripts')
rows=[l.split() for l in open(D+'/overlap-eu.log') if len(l.split())==3]
c=[int(r[1]) for r in rows]; l=[float(r[2]) for r in rows]; t=[int(r[0]) for r in rows]
def longest(pred):
    best=cur=0;s=0
    for ti,ci,li in zip(t,c,l):
        if pred(ci,li):
            if cur==0:s=ti
            cur=ti-s+5;best=max(best,cur)
        else: cur=0
    return best
print('EU monitor samples (5 s):',len(rows),'window',t[0],'-',t[-1])
print('samples with 0 foreign busy processes:',sum(1 for x in c if x==0))
print('samples that pass the registered guard (0 foreign and load1 < 1.2):',sum(1 for a,b in zip(c,l) if a==0 and b<1.2))
print('longest guard-passing stretch s:',longest(lambda a,b:a==0 and b<1.2),'; longest stretch with 0 foreign:',longest(lambda a,b:a==0))
print('load1 median %.1f max %.1f; foreign median %d max %d'%(S.median(l),max(l),S.median(c),max(c)))
out=subprocess.run([sys.executable,'-I',X+'/sim.py',D+'/mix-records.json','/tmp/e2-sim-summary.json'],capture_output=True,text=True)
sim=json.load(open('/tmp/e2-sim-summary.json'))
print('\nhost policy alpha_small lock_wait_h wait_plus_run_h small_median_s')
for h,v in sim.items():
    for k,x in v.items():
        if isinstance(x,dict): print(h,k.split()[0],k.split('a_small=')[1].split()[0],x['wait_h'],x['wait_plus_run_h'],x['small_wait_run_median_s'])
