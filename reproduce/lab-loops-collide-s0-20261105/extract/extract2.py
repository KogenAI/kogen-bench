import json,glob,os,re,collections
base=os.path.expanduser('~/.claude/projects/<project>/')
CODES='REPO_STALL REPO_IDLE SHELF_LOW UNDERUSED LOW_RUNNABLE OVERLOAD EXP_NO_CELLS EXPERIMENTS_LOW UNDERSPEND OVERPACE ADOPTION_RED SCREEN_DEBT GREEN_UNLANDED BUILD_STALL BUILD_HOST_BLOCKED BUILD_FUTILE FINDING_UNROUTED STUDIO_NEW GUARD_HOLD SWAP_HIGH ROADMAP_DRY HOLD_UNSOURCED POLICY_FAILURE WORKER_DEAD LOGIN_MISSING SCHEDULER_DOWN DISK_FLOOR PUBLISH_STALE IDLE_WITH_BACKLOG CPU_HOG MAIN_UNREACHABLE ROLE_RECOVERY LATE_RECENT'.split()
rx=re.compile(r'\b('+'|'.join(CODES)+r')\b[ :]+([A-Za-z0-9_./@-]+)')
f=glob.glob(base+'e5060617*.jsonl')[0]
out=[]
def codes(txt): return sorted({(m.group(1),m.group(2).rstrip(':,.')) for m in rx.finditer(txt)})
for l in open(f,errors='replace'):
    if '"SendMessage"' not in l and 'cross-session' not in l: continue
    try:o=json.loads(l)
    except: continue
    ts=o.get('timestamp','')
    if not ts: continue
    c=(o.get('message') or {}).get('content')
    if isinstance(c,str) and 'cross-session-message' in c[:300]:
        m=re.search(r'from-name="([^"]*)"',c[:400]); peer=m.group(1) if m else '?'
        relay=peer.startswith('control-') and 'ops-tick' in c[:400]
        out.append(dict(dir='in',ts=ts,peer=('ops-tick' if relay else peer),relay=relay,n=len(c),codes=codes(c)))
    elif isinstance(c,list):
        for b in c:
            if isinstance(b,dict) and b.get('type')=='tool_use' and b.get('name')=='SendMessage':
                i=b.get('input',{}); msg=str(i.get('message',''))
                out.append(dict(dir='out',ts=ts,peer=str(i.get('to'))[:40],relay=False,n=len(msg),codes=codes(msg)))
json.dump(out,open('out/main-msgs.json','w'))
print(len(out))
