"""usage: stage_ends.py <round dir>: per arm, how every stage (round) ended and the outcome/end_reason/error of every provider request attempt (network outages would show as non-complete attempts or non-terminal endings)."""
import sys,json,collections,glob
root=sys.argv[1]
for arm in ('pin','main'):
    e=collections.Counter();o=collections.Counter();n=0
    for f in sorted(glob.glob(root+'/counted/cells/*/r1/'+arm+'/events.jsonl')):
        for l in open(f):
            j=json.loads(l);r=j.get('record',j)
            if j['type']=='round.ended':e[r.get('ending')]+=1
            if j['type']=='request.attempt':
                n+=1;o[(r.get('outcome'),r.get('end_reason'),str(r.get('error'))[:80])]+=1
    print(arm,'attempts',n,dict(e));[print('  ',v,k) for k,v in o.most_common()]
