"""All-attempt accounting, separate evaluation and infrastructure outcomes."""
import argparse
import collections
import json
import math
import statistics as st
import sys
import pubmetrics as pm

def summarize(rows):
    arms=collections.defaultdict(list)
    for r in rows:
        arms[r['cell'].split('/')[-1]].append(r)
    summaries=[]
    for arm,rs in sorted(arms.items()):
        scored=[r for r in rs if isinstance(r.get('pass'),bool)]
        land=[r for r in scored if r['pass']]
        complete=[r for r in rs if all(pm.number(r.get(k)) for k in ('input','cached','output')) and r['input']>=r['cached']]
        full=len(complete)==len(rs)
        i,c,o=(sum(r[k] for r in complete) for k in ('input','cached','output'))
        usd=[r['usd'] for r in rs if pm.number(r.get('usd'))]
        lower={k:sum((r.get('usage_lower_bounds') or {}).get(k) or 0 for r in rs) for k in pm.TOKENS}
        result=dict(arm=arm,observed_attempts=len(rs),boolean_evaluator_reports=sum(isinstance(r.get('reported_pass'),bool) for r in rs),
                    reported_passes=sum(r.get('reported_pass') is True for r in rs),scored=len(scored),final_tree_test_passes=len(land),
                    infrastructure=sum(bool(r.get('infra')) for r in rs),tests_not_run=sum(r.get('tests_ran') is False for r in rs),
                    tests_ran_unknown=sum(r.get('tests_ran') is None for r in rs),clean_agent_completions=sum(r.get('clean_agent_completion') is True for r in rs),
                    outcomes=dict(collections.Counter(r.get('outcome') or 'unknown' for r in rs)),usage_n=len(complete),usage_denominator=len(rs),
                    usage_lower_bounds=lower,known_complete_usage_totals=dict(input=i,cached=c,output=o),usd_n=len(usd),
                    uncached_per_test_pass=(i-c)/len(land) if full and land else None,
                    equivalent_tokens_per_test_pass=(i-c+.1*c+4*o)/len(land) if full and land else None,
                    usd_per_test_pass=sum(usd)/len(land) if len(usd)==len(rs) and land else None,
                    leak_flags=sum(bool(r.get('leak')) for r in rs))
        for label,key,subset in [('all_attempt_cell_wall','wall_s',rs),('all_attempt_agent_wall','agent_wall_s',rs),
                                 ('passing_tree_cell_wall','wall_s',land),('clean_completion_cell_wall','wall_s',[r for r in rs if r.get('clean_agent_completion') and not r.get('infra')])]:
            values=sorted(r[key] for r in subset if pm.number(r.get(key)))
            result[label]=dict(n=len(values),median=st.median(values) if values else None,
                               p90=values[math.ceil(.9*len(values))-1] if values else None)
        summaries.append(result)
    return summaries

def main():
    import lanes_bare as lb
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('run',nargs='?');ap.add_argument('--exploratory',action='store_true');args=ap.parse_args()
    run=args.run or sys.stdin.readline().strip()
    validation=pm.round_validation(run)
    if not validation['complete'] and not args.exploratory:
        raise SystemExit('Final scoring refused: incomplete or unattested round; use --exploratory for provisional measurements')
    print(json.dumps(dict(exploratory=not validation['complete'],validation=validation,summary=summarize(lb.summary_rows(run))),indent=2,allow_nan=False))
if __name__=='__main__':
    main()
