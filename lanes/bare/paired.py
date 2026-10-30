"""Task-paired descriptive comparison. Default refuses incomplete/unattested rounds."""
import argparse
import collections
import json
import math
import statistics as st
import pubmetrics as pm

def signp(w, l):
    n=w+l
    return sum(math.comb(n,k) for k in range(w,n+1))/2**n if n else 1.0

def comparisons(rows, control):
    arms=collections.defaultdict(dict)
    for row in rows:
        task,rep,arm=row['cell'].split('/')
        arms[arm][task,rep]=row
    if control not in arms:
        raise ValueError('Control arm has no observed cells')
    out=[]
    for arm in sorted(arms):
        if arm==control:
            continue
        common=arms[arm].keys() & arms[control].keys()
        matched=[k for k in sorted(common) if all(isinstance(r.get('pass'),bool) for r in (arms[arm][k],arms[control][k]))]
        by=collections.defaultdict(list)
        for k in matched:
            by[k[0]].append((arms[arm][k],arms[control][k]))
        diffs=[sum(int(a['pass'])-int(b['pass']) for a,b in pairs) for pairs in by.values()]
        row=dict(arm=arm, control=control, pairs=len(matched), excluded_pairs=len(common)-len(matched), tasks=len(by),
                 candidate_pass=sum(arms[arm][k]['pass'] for k in matched), control_pass=sum(arms[control][k]['pass'] for k in matched),
                 task_wins=sum(d>0 for d in diffs),task_losses=sum(d<0 for d in diffs),task_ties=sum(d==0 for d in diffs),
                 repetition_reduction='per-task arithmetic mean over matched repetitions',
                 matched_repetitions={t:len(pairs) for t,pairs in sorted(by.items())})
        row['one_sided_sign_p']=signp(row['task_wins'],row['task_losses'])
        row['descriptive_guard']=len(by)==13 and row['task_losses']-row['task_wins']<=1
        def metric(name, value):
            absolute=[]; relative=[]
            for pairs in by.values():
                av=[value(a) for a,b in pairs];bv=[value(b) for a,b in pairs]
                if any(x is None for x in av+bv):
                    continue
                a,b=st.mean(av),st.mean(bv)
                absolute.append(a-b)
                if b>0:
                    relative.append(a/b-1)
            return {name+'_task_n':len(absolute),name+'_ratio_task_n':len(relative),
                    'median_task_'+name+'_absolute_delta':st.median(absolute) if absolute else None,
                    'median_task_'+name+'_delta':st.median(relative) if relative else None}
        for name,key in [('cell_wall','wall_s'),('agent_wall','agent_wall_s')]:
            row.update(metric(name,lambda r,k=key:r.get(k) if pm.number(r.get(k)) else None))
        def token_value(r, equivalent=False):
            if not all(pm.number(r.get(k)) for k in ('input','cached','output')) or r['cached']>r['input']:
                return None
            return r['input']-r['cached']+(0.1*r['cached']+4*r['output'] if equivalent else 0)
        row.update(metric('uncached_tokens',token_value))
        row.update(metric('equivalent_tokens',lambda r:token_value(r,True)))
        # Compatibility key, now explicitly defined as task means rather than task medians.
        row['median_task_wall_delta']=row['median_task_cell_wall_delta']
        out.append(row)
    return out

def main():
    import lanes_bare as lb
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('run');ap.add_argument('control');ap.add_argument('--exploratory',action='store_true')
    args=ap.parse_args()
    validation=pm.round_validation(args.run)
    if not validation['complete'] and not args.exploratory:
        raise SystemExit('Final scoring refused: incomplete or unattested round; --exploratory emits explicitly provisional measurements')
    rows=lb.summary_rows(args.run)
    controls=[args.control]+sorted({r['cell'].split('/')[-1] for r in rows if r['arm']=='codex'}-{args.control})
    print(json.dumps(dict(exploratory=not validation['complete'],validation=validation,
                          comparisons=[c for control in controls for c in comparisons(rows,control)]),indent=2,allow_nan=False))
if __name__=='__main__':
    main()
