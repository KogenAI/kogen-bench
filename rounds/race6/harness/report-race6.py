#!/usr/bin/env python3
"""Frozen one-wave pilot: complete Mac samples only, no winner or continuation."""
import argparse,json,statistics
from pathlib import Path
def summarize(runs,invalid_round=False):
    assert len(runs)==2
    scores={a:[r.get(a) for r in runs] for a in 'abcd'}
    complete={a:all(isinstance(v,int) and 0<=v<=106 for v in values) for a,values in scores.items()}
    medians={a:statistics.median(v) if complete[a] else None for a,v in scores.items()}
    spread={a:max(v)-min(v) if complete[a] else None for a,v in scores.items()}
    directions={}
    for a in 'bcd':
        if not complete[a] or not complete['a']:directions[a]='insufficient data'
        elif min(scores[a])>max(scores['a']):directions[a]=a.upper()+' above A'
        elif max(scores[a])<min(scores['a']):directions[a]=a.upper()+' below A'
        else:directions[a]='no clear direction'
    ordered=sorted((m for m in medians.values() if m is not None),reverse=True)
    gap=ordered[0]-ordered[1] if len(ordered)>=2 else None
    ambiguous=(gap is not None and gap<=3) or any(v is not None and v>10 for v in spread.values())
    return dict(status='invalid round' if invalid_round else 'PILOT: observed separation only',N=106,finals=scores,
      medians=medians if not invalid_round else {},median_scores={a:(f'{m:g}/106' if m is not None else 'unavailable') for a,m in medians.items()} if not invalid_round else {},
      differences={a+'-A':medians[a]-medians['a'] if complete[a] and complete['a'] else None for a in 'bcd'} if not invalid_round else {},
      spread=spread, directions=directions if not invalid_round else {},ambiguous_pilot=ambiguous if not invalid_round else None,
      paired_differences={host:{a+'-A':r[a]-r['a'] if isinstance(r.get(a),int) and isinstance(r.get('a'),int) else None for a in 'bcd'} for host,r in zip(('studio','macbook'),runs)},
      planned_sample_size={a:2 for a in 'abcd'},valid_sample_size={a:sum(v is not None for v in scores[a]) for a in 'abcd'},leading_gap=gap,
      continuation='none: one 60-minute wave, no second wave or make-ups')
def load(root,lang="ex"):
    root=Path(root);scores={};slots={};flags=[]
    if (root/'out/audit.txt').exists():flags=[l for l in (root/'out/audit.txt').read_text().splitlines() if l.startswith('FLAG ') and 'CLASSIFY' not in l and ('VOIDING' in l or 'receipt' in l)]
    for a in 'abcd':
        arm=lang+'-'+a;p=root/f'out/results/FINAL-{arm}-score.json';bad=[l for l in flags if l.startswith('FLAG '+arm+' ')]
        if not (root/'DONE').exists():scores[a]=None;slots[a]={'status':'missing','reason':'missing host DONE'};continue
        if not p.exists():scores[a]=None;slots[a]={'status':'invalid','reason':'FINAL unscorable or missing official receipt after DONE (harness failure)','official_final':None};continue
        raw=json.loads(p.read_text())['combined_scored'];scores[a]=None if bad else raw
        slots[a]={'status':'invalid' if bad else 'valid','reason':bad,'official_final':scores[a],'raw_final_nondeciding':raw if bad else None}
    metrics=json.loads((root/'out/metrics.json').read_text()) if (root/'out/metrics.json').exists() else {'observations':'unavailable'}
    return scores,slots,metrics,any(l.startswith('FLAG harness ') for l in flags)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('studio',type=Path);p.add_argument('macbook',type=Path);p.add_argument('--linux',type=Path,action='append',default=[]);a=p.parse_args()
    result={'languages':{},'cross_language_ranking':'none'}
    for lang in ('ex','go'):
        st,sts,stm,stv=load(a.studio,lang);mb,mbs,mbm,mbv=load(a.macbook,lang);entry=summarize([st,mb],stv or mbv)
        entry['slots']={'studio':sts,'macbook':mbs};entry['per_run_metrics']={'studio':stm,'macbook':mbm};result['languages'][lang]=entry
    result['linux_reported_only']={str(r):load(r,'ex')[1:3] for r in a.linux}
    result['methods']={'tokens':'cumulative event/session receipts at each arm FINAL timestamp; missing observations disclosed','wall':'each language epoch to its own 60-minute cap; raw/stall-adjusted observations separate','build_test':'sum command started/completed timestamp intervals matching registered build/test commands'}
    print(json.dumps(result,indent=2))
