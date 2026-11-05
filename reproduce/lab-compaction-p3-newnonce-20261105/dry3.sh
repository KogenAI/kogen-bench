#!/bin/bash
# Stage B dry check, NO model call: drives stub3.py (mode newnonce) with scripted JSON-RPC calls and checks the
# hit / no-change / reuse classifications. usage: dry3.sh <empty scratch dir>
set -eu
D=$1; mkdir -p "$D"; HERE=$(cd "$(dirname "$0")" && pwd)
cat > "$D/cell.json" <<J
{"name":"dry3","mode":"newnonce","reserve":0,"K":0,"P":0,"Q":0,"ticket":"QX-0001","prefix":"lane-test","brief_rev":"r1","nonce":"a1b2c3d4","model":"none","effort":"none"}
J
/usr/bin/python3 -I - "$D" "$HERE/stub3.py" <<'PY'
import json,subprocess,sys,os
d,stub=sys.argv[1:3]
p=subprocess.Popen(["/usr/bin/python3","-I",stub],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True,env=dict(os.environ,STUB_CELL=d))
def rpc(i,m,pr=None):
    p.stdin.write(json.dumps({"jsonrpc":"2.0","id":i,"method":m,"params":pr or {}})+"\n");p.stdin.flush();return json.loads(p.stdout.readline())
rpc(1,"initialize")
r=rpc(2,"tools/call",{"name":"studio_start","arguments":{}})
assert 'nonce' in r["result"]["content"][0]["text"] and "a1b2c3d4" in r["result"]["content"][0]["text"]
seq=[("a1b2c3d4",False),("a1b2c3d4",False),("0f0f0f0f",True),("0f0f0f0f",False),("a1b2c3d4",True),("",True)]
for i,(n,exp) in enumerate(seq):
    a={"step":i,"text":"[lane-test] x","ticket":"QX-0001"}
    if n: a["nonce"]=n
    rpc(10+i,"tools/call",{"name":"studio_note","arguments":a})
p.stdin.close();p.wait()
rows=[json.loads(l) for l in open(os.path.join(d,"calls.jsonl"))] if os.path.exists(os.path.join(d,"calls.jsonl")) else []
print(len(rows),"logged")
got=[r.get("detected") for r in rows if r.get("tool")=="studio_note"]
print(got,[r.get("signal") for r in rows if r.get("tool")=="studio_note"])
assert got==[e for _,e in seq],"classification mismatch"
print("DRY3 PASS")
PY
