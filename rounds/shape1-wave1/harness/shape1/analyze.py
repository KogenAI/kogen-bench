#!/usr/bin/env python3
"""Exact paired tests and a registered ceiling/floor latch; standard library only."""
import argparse
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path
from shape_common import ROOT, LANGS, write_json
from run_shaper import OLD_LANE, safe_json


def sign_test(a,b):
    wins=sum(x>y for x,y in zip(a,b)); losses=sum(x<y for x,y in zip(a,b)); n=wins+losses
    p=min(1.,2*sum(math.comb(n,k) for k in range(min(wins,losses)+1))/2**n) if n else 1.
    return {'wins':wins,'losses':losses,'ties':len(a)-n,'discordant':n,'p_two_sided':p}


def wilcoxon(a,b):
    pairs=[(Fraction(str(x)),Fraction(str(y))) for x,y in zip(a,b)]
    differences=[x-y for x,y in pairs if x != y]
    ordered=sorted(range(len(differences)),key=lambda i:abs(differences[i]))
    ranks=[Fraction(0)]*len(differences)
    i=0
    while i < len(ordered):
        j=i+1
        while j<len(ordered) and abs(differences[ordered[j]])==abs(differences[ordered[i]]): j+=1
        for k in ordered[i:j]: ranks[k]=Fraction(i+1+j,2)
        i=j
    observed=sum((r for r,d in zip(ranks,differences) if d>0),Fraction(0)); total=sum(ranks,Fraction(0))
    distance=abs(observed-total/2)
    extreme=sum(abs(sum(r*s for r,s in zip(ranks,bits))-total/2)>=distance
                for bits in itertools.product((0,1),repeat=len(ranks)))
    return {'nonzero_pairs':len(ranks),'w_plus':float(observed),'w_plus_exact':str(observed),
            'p_two_sided':extreme/2**len(ranks),'p_exact':str(Fraction(extreme,2**len(ranks)))}


def inferable(row):
    return row.get('status') not in ('blocked','infrastructure_failure') and type(row.get('validity')) is bool


def kill_fraction(row):
    if row.get('mutant_denominator'):
        return Fraction(row['mutants_killed'],row['mutant_denominator'])
    return Fraction(str(row['mutant_kill_rate']))


def interval(k,n):
    if not n:return None
    z=1.959963984540054; p=k/n; d=1+z*z/n
    center=(p+z*z/(2*n))/d; width=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return [max(0,center-width),min(1,center+width)]


def analyze_rows(rows):
    table={}
    plan=json.loads((ROOT/'plan.json').read_text())
    tasks=[t['id'] for t in plan['tasks']]
    for row in rows:
        key=(row['task'],row['language'])
        if key in table:raise ValueError('duplicate measured cell; one rep only')
        if row['task'] not in tasks or row['language'] not in LANGS:raise ValueError('unregistered cell')
        table[key]=row
    result={'measured_cells':len(rows),'validity':{},'paired':{},'coverage_descriptive':{},'complete_tasks':[]}
    for lang in LANGS:
        arm=[table[t,lang] for t in tasks if (t,lang) in table and inferable(table[t,lang])]
        n=len(arm); k=sum(r['validity'] is True for r in arm)
        result['validity'][lang]={'valid':k,'denominator':n,'rate':k/n if n else None,'wilson_95':interval(k,n)}
        coverage=[r['coverage'] for r in arm if r.get('coverage') is not None]
        result['coverage_descriptive'][lang]={'n':len(coverage),'mean':sum(coverage)/len(coverage) if coverage else None}
    complete=[t for t in tasks if all((t,l) in table and inferable(table[t,l]) for l in LANGS)]
    result['complete_tasks']=complete
    for other in ('go','ts-bun'):
        a=[int(table[t,'rust']['validity']) for t in complete]; b=[int(table[t,other]['validity']) for t in complete]
        comparison={'sign':sign_test(a,b),'tasks':complete}
        eligible=[t for t in complete if table[t,'rust'].get('mutant_kill_rate') is not None and table[t,other].get('mutant_kill_rate') is not None]
        comparison['mutant_wilcoxon']=wilcoxon([kill_fraction(table[t,'rust']) for t in eligible],
                                               [kill_fraction(table[t,other]) for t in eligible])
        comparison['mutant_tasks']=eligible
        result['paired']['rust_vs_'+other]=comparison
    ordered=sorted(result['paired'],key=lambda k:result['paired'][k]['sign']['p_two_sided'])
    previous=0.
    for i,key in enumerate(ordered):
        adjusted=min(1.,max(previous,(2-i)*result['paired'][key]['sign']['p_two_sided']))
        result['paired'][key]['sign']['holm_p']=adjusted; previous=adjusted
    first=tasks[:4]
    ready=all(t in complete for t in first)
    values=[table[t,l]['validity'] for t in first for l in LANGS] if ready else []
    result['stop']= 'ceiling' if ready and all(values) else 'floor' if ready and not any(values) else None
    return result


def analyze(paths):
    keys=('task','language','pilot','validity','coverage','status','mutants_killed',
          'mutant_denominator','mutant_kill_rate','lane','strict_eligible')
    rows=[safe_json(p,keys) for p in paths]
    rows=[r for r in rows if not r.get('pilot')]
    strict=[];descriptive=[]
    for row in rows:
        if row.get('lane')==OLD_LANE or row.get('strict_eligible') is False:
            descriptive.append(row)
        elif row.get('lane') in (None,'strict'):
            strict.append(row)
        else:raise ValueError('unknown lane; refusing to pool results')
    result=analyze_rows(strict)
    result.update(lane='strict',strict_eligible=True)
    separate=analyze_rows(descriptive)
    separate.update(lane=OLD_LANE,strict_eligible=False,reporting='descriptive only',stop=None)
    result['old_descriptive']=separate
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('scores',type=Path,nargs='*');p.add_argument('--output',type=Path,required=True);p.add_argument('--apply-stop',action='store_true')
    a=p.parse_args();result=analyze(a.scores);write_json(a.output,result)
    if a.apply_stop and result['stop']:
        (ROOT/'STOP').write_text(result['stop']+'\n')
    print(json.dumps(result))
