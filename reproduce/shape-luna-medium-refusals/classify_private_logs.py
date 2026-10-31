#!/usr/bin/env python3
import json,csv,re,sys,collections,os
raw=json.load(open(sys.argv[1])); am=json.load(open(sys.argv[2]))
res={x['label']:x for x in csv.DictReader(open(sys.argv[3]),delimiter='\t')}
blind=sys.argv[4]
TEST=re.compile(r'^- (none: \S.*|.+: .+ \((unit|integration|scenario|regression|existing)\))$')
SRC=re.compile(r'\(source: (request|answer \d+)\)\s*$')
def decision_kind(lab):
    f=f'{blind}/{lab}/intent.md'
    if not os.path.exists(f): return 'other'
    t=open(f).read(); m=re.search(r'^## Decisions\n(.*?)(?=^## |\Z)',t,re.S|re.M)
    if not m: return 'other'
    kinds=set()
    for l in m.group(1).splitlines():
        if l.startswith('- ') and not SRC.search(l):
            kinds.add('S' if re.search(r'\(source: (request|answer \d+)\)\W+$',l) else 'F')
    return 'S' if kinds=={'S'} else 'F'
def one(lab,p,gate):
    if gate=='coverage_ledger': return ('STRICTNESS','coverage-ledger gate (S2 patch only)')
    m=re.match(r'tests: (.*) must be `',p,re.S)
    if m:
        l=m.group(1).strip()
        if TEST.match(re.sub(r'[.;,]+$','',l)): return ('STRICTNESS','tests line ends with a period after the layer tag (anchored regex)')
        return ('FORMAT','tests line not in "- rule: test (layer)" form')
    if p.startswith('decisions:'):
        return ('STRICTNESS','decision line has trailing punctuation after (source: ...)') if decision_kind(lab)=='S' else ('FORMAT','decision source tag missing or non-standard source')
    if p.startswith('title:'): return ('FORMAT','title over 50 characters')
    if p.startswith('stages:'): return ('FORMAT','stages JSON fence')
    if p.startswith('acceptance.feature'): return ('FORMAT','Gherkin: unexpected text (unquoted data/continuation lines)')
    if p.startswith('acceptance:') or p.startswith('model:'): return ('FORMAT','file named in Intent missing from submission')
    if 'undefined step' in p: return ('FORMAT','step self-check: undefined step')
    if gate=='validation': return ('FORMAT','submit schema (questions/files/blocked)')
    return ('FORMAT','Quint run/typecheck failure (readiness)')
rows=[]; recs=[]
for lab,r in raw.items():
    a=am[lab]['arm']; cl=res[lab]['class']
    if cl=='ready': rows.append((a,'ACCEPTED','accepted Intent',0)); continue
    if cl=='questions': rows.append((a,'REASONING','asked questions, no Intent submitted'+(' (after refused submissions)' if r['refused'] else ''),0)); continue
    if cl=='other_exit_4': rows.append((a,'PROVIDER','provider refused the request',0)); continue
    if 'protected_conflict' in r['stdout']: rows.append((a,'REASONING','required edits touch protected files',0)); continue
    if not r['refused']: rows.append((a,'FORMAT','Quint run/typecheck failure (readiness)',0)); continue
    last=r['refused'][-1]; ps=last['p'] or ['']
    subs=[one(lab,p,last['gate']) for p in ps]
    # cell cause: STRICTNESS only if every problem in the final attempt is an anchor problem (fixing it alone would clear the gate)
    allstrict=all(s[0]=='STRICTNESS' for s in subs)
    pick=subs[0] if allstrict else next((s for s in subs if s[0]=='FORMAT'),subs[0])
    # any attempt hit an anchor problem?
    anyanchor=any(one(lab,p,x['gate'])[0]=='STRICTNESS' for x in r['refused'] for p in x['p'])
    rows.append((a,pick[0],pick[1],int(anyanchor)))
    recs.append(dict(arm=a,cause=pick[0],sub=pick[1],anchor_any=int(anyanchor),refused=len(r['refused']),cls=cl,attempt_kinds=[sorted({one(lab,p,x['gate'])[1] for p in (x['p'] or [''])}) for x in r['refused']]))
t=collections.defaultdict(collections.Counter); sub=collections.defaultdict(collections.Counter); anch=collections.Counter(); n=collections.Counter()
for a,c,s,an in rows:
    t[a][c]+=1; sub[a][(c,s)]+=1; n[a]+=1
    if c!='ACCEPTED': anch[a]+=an
print('cause per arm (26 shapes each):')
for a in ('b0','p2','p4'): print(a,dict(t[a]),'any-attempt-hit-anchor-strictness:',anch[a])
print()
for a in ('b0','p2','p4'):
    print(a)
    for (c,s),v in sorted(sub[a].items(),key=lambda x:(x[0][0],-x[1])): print(f'  {v:2d} {c:10s} {s}')

# non-failure rows carry no attempts
import hashlib
simple=[dict(arm=a,cause=c,sub=sx,anchor_any=an,refused=0,cls='-',attempt_kinds=[]) for a,c,sx,an in rows if c in ('ACCEPTED','REASONING','PROVIDER') ]
full=[x for x in recs]+[x for x in simple if not any(False for _ in [0])]
json.dump(full,open('cells_full.json','w'))
