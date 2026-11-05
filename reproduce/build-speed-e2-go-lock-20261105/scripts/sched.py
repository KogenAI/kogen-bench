import json,random
R=random.Random(20261105)
comp=[('kogen-setup',10,'small'),('kogen-executor',8,'small'),('kogen-review',7,'small'),('kogen-loop',6,'small'),('kogen-coordinator',7,'small'),('kogen-verification',2,'large')]
shim=[('kogen-review','./contract'),('kogen-review','./review'),('kogen-setup','./contract'),('kogen-executor','./contract'),('kogen-executor','./core'),('kogen-review','./cmd/kogen-review')]
suites=[(r,c) for r,n,c in comp for _ in range(n)]
small=[s for s in suites if s[1]=='small']; R.shuffle(small)
S=[[] for _ in range(4)]
big=[s for s in suites if s[1]=='large']
slots={(0,3):big[0],(1,5):big[1]}   # verification on stream 0 item 4 and stream 1 item 6
it=iter(small)
for si in range(4):
    for k in range(10):
        S[si].append(slots.get((si,k)) or next(it))
assert not list(it)
streams=[]
for si in range(4):
    items=[]
    for r,c in S[si]:
        sr,sp=R.choice(shim)
        items.append(dict(kind='shim',suite='shim:'+sr+sp,tree=sr,**{'class':'small'},cmd=f'# kogen-go-shim (lab replay of a builder go test)\nexec go test -count=1 {sp}'))
        items.append(dict(kind='suite',suite=r,tree=r,**{'class':c},cmd='GOFLAGS="-trimpath -count=1" go test ./...'))
    streams.append(items)
json.dump(dict(stagger=[0,15,30,45],think=5,streams=streams),open('sched.json','w'),indent=1)
from collections import Counter
print(Counter(i['suite'] for s in streams for i in s if i['kind']=='suite'),sum(1 for s in streams for i in s))
