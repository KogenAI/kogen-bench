# Move the testing-rules section to the head of its text block inside a Kogen test fixture, byte for byte.
# Usage: python3 -I golden_move.py <cli/agent/prompts/testing-rules.md> <original fixture.json> <output fixture.json>
# The section is located in its JSON-escaped form (plain strings, and strings holding a serialized request body),
# moved inside the raw file (nothing else is re-encoded), and the result is checked to equal, after parsing,
# "the original with the section moved to the head of the block that held it".
import json,re,sys
rules_path,src,dst=sys.argv[1:4]
R=open(rules_path,encoding="utf-8").read()
SEG="# Testing rules (docs/testing-rules.md)\n\n"+R+"\n\n"
def escs(s):
    out=set()
    for asc in (False,True):
        e=json.dumps(s,ensure_ascii=asc)[1:-1]
        out.add(e); out.add(e.replace("<","\\u003c").replace(">","\\u003e").replace("&","\\u0026"))
    return out
def moved(v):
    if isinstance(v,dict): return {k:moved(x) for k,x in v.items()}
    if isinstance(v,list): return [moved(x) for x in v]
    if isinstance(v,str):
        if SEG in v: return SEG+v.replace(SEG,"",1)
        if v.startswith("{") and "Testing rules" in v: return ("SERIAL",moved(json.loads(v)))
    return v
def norm(v):
    if isinstance(v,dict): return {k:norm(x) for k,x in v.items()}
    if isinstance(v,list): return [norm(x) for x in v]
    if isinstance(v,str) and v.startswith("{") and "Testing rules" in v: return ("SERIAL",norm(json.loads(v)))
    return v
lvl1=escs(SEG); lvl2=set()
for e in lvl1: lvl2|=escs(e)
lvl2-=lvl1
raw=open(src,encoding="utf-8").read(); edits=[]
for lvl,variants in ((2,lvl2),(1,lvl1)):
    for e in variants:
        for m in re.finditer(re.escape(e),raw):
            p=m.start()
            if any(s0<=p<p0+l0 for s0,p0,l0,_ in edits): continue
            if lvl==2:
                marker='\\"text\\":\\"'; s=raw.rfind(marker,0,p)+len(marker)
            else:
                s=p
                while True:
                    s=raw.rfind('"',0,s); k=s-1; b=0
                    while raw[k]=="\\": b+=1; k-=1
                    if b%2==0: break
                s+=1
            edits.append((s,p,len(e),e))
for s,p,l,e in sorted(edits,reverse=True):
    raw=raw[:s]+e+raw[s:p]+raw[p+l:]
ok=norm(json.loads(raw))==moved(json.loads(open(src,encoding="utf-8").read()))
print(src,"edits",len(edits),"semantic-equal",ok)
if not ok: sys.exit(1)
open(dst,"w",encoding="utf-8").write(raw)
