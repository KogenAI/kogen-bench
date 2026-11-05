import re,json,sys,datetime as dt
IN='in/'
def ep(t): return dt.datetime.strptime(t,'%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=dt.timezone.utc).timestamp()
def fleet():
    ticks=[];cur=None
    for l in open(IN+'fleet-check.log',errors='replace'):
        l=l.rstrip('\n')
        m=re.match(r'=== (\S+Z)$',l)
        if m:
            cur={'t':m.group(1),'e':ep(m.group(1)),'lines':[],'exit':None};ticks.append(cur);continue
        if cur is None: continue
        m=re.match(r'exit=(\d+)$',l)
        if m: cur['exit']=int(m.group(1));continue
        if l=='OK' or not l.strip(): continue
        cur['lines'].append(l)
    return ticks
def opstick():
    out=[]
    for l in open(IN+'ops-tick.log',errors='replace'):
        m=re.match(r'(\S+Z) fleet-check exit=(\d+) red=(\d+) relay=(.*?) owner_alerts=(.*?) heartbeat',l)
        if not m: continue
        r=m.group(4);mm=re.match(r'sent (\d+)',r)
        out.append({'t':m.group(1),'e':ep(m.group(1)),'exit':int(m.group(2)),'red':int(m.group(3)),'relay':r,'sent':int(mm.group(1)) if mm else 0,'failed':r.startswith('failed'),'owner':m.group(5)})
    return out
if __name__=='__main__':
    f=fleet();o=opstick()
    print(len(f),f[0]['t'],f[-1]['t']);print(len(o),o[0]['t'],o[-1]['t'])
    import collections
    c=collections.Counter(l.split()[0] for t in f for l in t['lines'])
    for k,v in c.most_common(40):print(v,k)
