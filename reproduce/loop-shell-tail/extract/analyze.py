import os,pathlib,json,collections,datetime,hashlib,re,shlex,itertools,math,csv
R=pathlib.Path(os.environ.get('SHELLTAIL_SNAPSHOT') or pathlib.Path(__file__).resolve().parent)
O=pathlib.Path(os.environ.get('SHELLTAIL_OUT') or '.')
def js(v):return json.dumps(v,ensure_ascii=False,separators=(',',':'))
def sha(v):return hashlib.sha256(v.encode()).hexdigest()
def ts(v):return datetime.datetime.fromisoformat(v.replace('Z','+00:00')).timestamp()
def unwrap(s):
 try:
  a=shlex.split(s)
  if len(a)==3 and a[1] in ['-lc','-c']:return a[2]
 except ValueError:pass
 return s

def executable(s):
 s=unwrap(s);out=[];end=None
 for line in s.splitlines():
  if end:
   if line.strip()==end:end=None
   continue
  h=re.search(r"<<-?\s*['\"]?([A-Za-z_][A-Za-z0-9_]*)['\"]?",line)
  if h:
   end=h.group(1)
   continue
  out.append(line)
 return '\n'.join(out)

def kinds(s):
 # Command-bearing categories, intentionally overlapping for compounds.
 s=executable(s)
 return [k for k,p in {
 'test':r'\bgo\s+(?:-C\s+\S+\s+)?test\b|\bmix\s+test\b|\bnpm\s+(?:test|run\s+(?:test|acceptance))\b',
 'build':r'\bgo\s+(?:-C\s+\S+\s+)?build\b|\bmix\s+compile\b|\bmake\s+build\b|\bnpm\s+run\s+build\b',
 'vet':r'\bgo\s+(?:-C\s+\S+\s+)?vet\b','format':r'\bgofmt\b|\bgo\s+fmt\b','make-check':r'\bmake\s+check\b',
 'acceptance':r'(?:scripts/)?acceptance(?:\.sh)?|\bmake\s+acceptance\b',
 'read':r'\b(?:ls|cat|sed|head|tail|rg|grep|pwd|find)\b', 'git':r'\bgit\s+',
 'module-test':r'\bgo\s+(?:-C\s+\S+\s+)?test\b[^\n;&|]*\./\.\.\.',
 'targeted-test':r'\bgo\s+(?:-C\s+\S+\s+)?test\b[^\n;&|]*(?:\s-run(?:=|\s)|\s\./[A-Za-z_][^\s;&|]*)',
 'race':r'\bgo\s+(?:-C\s+\S+\s+)?test\b[^\n;&|]*-race\b','count':r'\bgo\s+(?:-C\s+\S+\s+)?test\b[^\n;&|]*-count(?:=|\s)',
 }.items() if re.search(p,s)]
cells=[]; calls=[]; commands=[]; sources=[]
for f in sorted(R.glob('**/result.json')):
 if 'cells' not in f.parts:continue
 d=json.loads(f.read_text());client=d.get('arm')
 if client not in ['loop','codex']:continue
 c=f.parent
 if not (c/'events.jsonl').exists() or d.get('totals',{}).get('wall_s') is None:continue
 b=c.relative_to(R).parts[0];key=f'{b}/{c.parent.parent.name}/{c.parent.name}/{c.name}'
 es=[];bad=0
 for s in (c/'events.jsonl').read_text().splitlines():
  try:es.append(json.loads(s))
  except ValueError:bad+=1
 z=dict(key=key,batch=b,task=c.parent.parent.name,rep=c.parent.name,arm=c.name,client=client,effort=d['effort'],passed=d.get('all_passed'),outcome=d.get('outcome'),wall=d['totals']['wall_s'],cellwall=d['wall_s'],prompt=d['prompt_sha256'],start=d.get('start_commit'),model=d['model'],bad=bad)
 pending={};active=set();overlap=0;n=0;cc=[];cmds=[];batches=collections.defaultdict(list);provider=0;callidx=0
 for e in es:
  typ=e.get('type');it=e.get('item') or {}
  if typ=='request.started':n=e['n']
  if typ=='request.attempt':provider+=e['record']['wall_ms']/1000
  if typ=='tool.call':pending[e['call_id']]=e;batches[n].append(e['name'])
  if typ=='tool.result':
   a=pending.pop(e['call_id'],None)
   if not a:continue
   t=dict(key=key,n=n,seq=a['seq'],name=a['name'],arg=a['arguments_sha256'],result=e['result_sha256'],bytes=e['bytes'],cut=e['cut'],seconds=ts(e['time'])-ts(a['time']),call_id=e['call_id'],command=None)
   calls.append(t);cc.append(t)
  if typ=='item.started' and it.get('type')=='command_execution':
   overlap+=bool(active);active.add(it['id'])
  if typ=='item.completed' and it.get('type')=='command_execution':
   active.discard(it['id']);s=it.get('command','');output=it.get('aggregated_output','')
   t=dict(key=key,id=it['id'],command=s,output_bytes=len(output.encode()),exit=it.get('exit_code'),cut=bool(re.search(r'truncated|omitted|Output truncated',output,re.I)),kinds=kinds(s));commands.append(t);cmds.append(t)
 for t in cc:t['later_provider_attempts']=sum(e.get('type')=='request.attempt' and e['n']>t['n'] for e in es);t['logical_replay_bytes']=t['bytes']*t['later_provider_attempts']
 z.update(logical_replay_bytes=sum(t['logical_replay_bytes'] for t in cc),provider=provider if client=='loop' else None,shell_s=sum(t['seconds'] for t in cc if t['name']=='shell'),shell_n=sum(t['name']=='shell' for t in cc),tool_bytes=sum(t['bytes'] for t in cc),shell_bytes=sum(t['bytes'] for t in cc if t['name']=='shell'),read_bytes=sum(t['bytes'] for t in cc if t['name'] in ['read_file','list_files','search_text']),cuts=sum(t['cut'] for t in cc),cmd_n=len(cmds),cmd_bytes=sum(t['output_bytes'] for t in cmds),overlap=overlap,multishell=sum(v.count('shell')>1 for v in batches.values()),terminal_reminders=sum(e.get('type')=='terminal.reminder' for e in es))
 cells.append(z)
 for p in [f,c/'events.jsonl',c/'evaluation.json',c/'prompt.md',c/'usage-events.jsonl']:
  if p.exists():sources.append(dict(path=str(p.relative_to(R)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
# Exact command preimages only; no inference from timings or output sizes.
pool=set()
for t in commands:
 s=unwrap(t['command']);pool.update([s,t['command'],s.strip()])
 for v in re.split(r'\s*(?:&&|;|\n)\s*',s):
  if v and len(v)<2000:pool.add(v)
base=['go test ./...','go vet ./...','go build ./...','go build .','go test','go test .','go vet .','make check','make build','make test','sh scripts/acceptance.sh','./scripts/acceptance.sh','bash scripts/acceptance.sh','git diff','git diff --stat','git status --short','ls','ls -la','pwd']
for scope in ['./...','.','./tools','./build','./provider','./loop','./cmd/kogen']:
 for flags in ['', '-count=1','-count 1','-race','-v','-race -count=1','-count=1 -race']:
  base.extend([f'go test {flags} {scope}'.replace('  ',' '),f'go test {scope} {flags}'.rstrip()])
base=list(set(base));pool.update(base)
for a in base:
 for b in ['go test ./...','go vet ./...','make check','git diff --stat','go build ./...','sh scripts/acceptance.sh']:
  for sep in [' && ','; ','\n']:pool.add(a+sep+b)
# Simple formatting/check combinations from names in visible commands and final diffs.
files=set()
for s in list(pool):files.update(re.findall(r'[\w./-]+\.go\b',s))
for f in R.glob('**/final.diff'):
 if 'cells' not in f.parts:continue
 for s in re.findall(r'^\+\+\+ b/(.*\.go)$',f.read_text(errors='replace'),re.M):files.add(s)
fmts=['gofmt -w *.go','gofmt -w .']
fmts+=['gofmt -w '+s for s in sorted(files)]
for a in fmts:
 pool.add(a)
 for b in ['go test ./...','go test ./... -count=1','go test -count=1 ./...','go vet ./...','go test ./... && go vet ./...','go vet ./... && go test ./...']:
  for sep in [' && ','; ','\n']:pool.add(a+sep+b)
# Additional finite verification chains, including package-root prefixes.
checks=['go test ./...','go vet ./...','make check','make build','sh scripts/acceptance.sh','./scripts/acceptance.sh','go test -race ./...','go test ./... -count=1','go test -count=1 ./...']
chains=set(checks)
for n in [2,3]:
 for seq in itertools.permutations(checks,n):
  for sep in [' && ','; ','\n']:chains.add(sep.join(seq))
for f in R.glob('**/final.diff'):
 fs=sorted(set(re.findall(r'^\+\+\+ b/(.*\.go)$',f.read_text(errors='replace'),re.M)))
 if 1<len(fs)<=6:
  for n in range(2,len(fs)+1):
   for combo in itertools.combinations(fs,n):fmts.append('gofmt -w '+' '.join(combo))
for fmt in set(fmts):
 for check in ['go test ./...','go test ./... && go vet ./...','go vet ./... && go test ./...','go test ./... && go vet ./... && make check','go test ./... && make check','go test ./... -count=1','go test -race ./...']:
  for sep in [' && ','; ','\n']:pool.add(fmt+sep+check)
pool.update(chains)
for prefix in ['cd cli && ','cd cli; ','cd cli\n']:
 for v in list(chains):pool.add(prefix+v)
# Supplied prompt check literals, with common finite batching/order variants.
for f in R.glob('**/prompt.md'):
 text=f.read_text(errors='replace')
 checks0=re.findall(r'^- [^\n:]+: `([^`]+)`',text,re.M)
 checks0=[v for v in checks0 if len(v)<600]
 if not checks0:continue
 fm='test -z "$(cd cli && gofmt -l .)"' if '(cd cli' in text else 'test -z "$(gofmt -l .)"'
 checkset=list(dict.fromkeys(checks0+[fm]))
 for n in range(1,min(len(checkset),5)+1):
  for seq in itertools.permutations(checkset,n):
   for sep in [' && ','; ','\n',';\n']:
    pool.add(sep.join(seq))
for scope in ['./...','./build','./build/','./project','./project/','./project/ ./verify/','./verify/']:
 for flag in ['', '-count=1','-v','-count=1 -v','-race']:
  for cmd in [f'go test {flag} {scope}'.replace('  ',' '),f'go test {scope} {flag}'.rstrip()]:
   for prefix in ['cd cli && ','cd cli; ','cd cli\n']:
    pool.add(prefix+cmd);pool.add('('+prefix+cmd+')')
want={t['arg'] for t in calls if t['name']=='shell'};matches={}
for s in pool:
 for val in [s,s+'\n']:
  for sep in [(',',':'),(',',': '),(', ',': '),(', ',':')]:
   a=json.dumps({'command':val},ensure_ascii=False,separators=sep)
   for a2 in [a,a.replace('&','\\u0026').replace('<','\\u003c').replace('>','\\u003e')]:
    h=sha(a2)
    if h in want:matches[h]=val
for t in calls:
 if t['name']=='shell':t['command']=matches.get(t['arg']);t['kinds']=kinds(t['command']) if t['command'] else []
# Pair only baseline same task/rep, effort/model/prompt and both passing.
idx={(z['batch'],z['task'],z['rep'],z['effort'],z['client']):z for z in cells if z['client']=='codex'}
pairs=[]
for z in cells:
 if z['client']!='loop' or z['arm'] not in ['loop-default','loop-default-medium','loop']:continue
 c=idx.get((z['batch'],z['task'],z['rep'],z['effort'],'codex'))
 if not c or any(z[k]!=c[k] for k in ['prompt','model','start']):continue
 if z['passed']!=c['passed']:continue
 pairs.append(dict(loop=z,codex=c))
for g,ps in itertools.groupby(sorted(pairs,key=lambda p:(p['loop']['batch'],p['loop']['effort'])),key=lambda p:(p['loop']['batch'],p['loop']['effort'])):
 ps=list(ps);eligible=[z for z in cells if (z['batch'],z['effort'])==g and z['arm'] in ['loop-default','loop-default-medium','loop']]
 top={z['key'] for z in sorted(eligible,key=lambda z:(-z['wall'],z['key']))[:math.ceil(len(eligible)/4)]}
 for p in ps:p['tail']=p['loop']['key'] in top
bycall=collections.defaultdict(list);bycmd=collections.defaultdict(list)
for t in calls:bycall[t['key']].append(t)
for t in commands:bycmd[t['key']].append(t)
for z in cells:
 ts0=bycall[z['key']];cs=bycmd[z['key']];seen=set();seenr=set();rep=[];reprs=[]
 for t in ts0:
  k=(t['name'],t['arg']);kr=(*k,t['result'])
  if k in seen:rep.append(t)
  if kr in seenr:reprs.append(t)
  seen.add(k);seenr.add(kr)
 z.update(repeat_calls=len(rep),repeat_s=sum(t['seconds'] for t in rep),repeat_bytes=sum(t['bytes'] for t in rep),same_result_repeats=len(reprs),same_result_s=sum(t['seconds'] for t in reprs),same_result_bytes=sum(t['bytes'] for t in reprs),repeat_shells=sum(t['name']=='shell' for t in rep),repeat_shell_s=sum(t['seconds'] for t in rep if t['name']=='shell'),repeat_shell_bytes=sum(t['bytes'] for t in rep if t['name']=='shell'),read_repeats=sum(t['name']=='read_file' for t in rep),codex_repeats=len(cs)-len(set(t['command'] for t in cs)),known_shells=sum(t['command'] is not None for t in ts0 if t['name']=='shell'))
for name,v in [('cells',cells),('calls',calls),('commands',commands),('pairs',pairs),('sources',sources)]:
 (R/(name+'.json')).write_text(json.dumps(v,indent=2)+'\n')
print('cells',len(cells),'pairs',len(pairs),'commands',len(commands),'pool',len(pool),'recovered unique hashes',len(matches),'of',len(want))
for g,ps in itertools.groupby(sorted(pairs,key=lambda p:(p['loop']['batch'],p['loop']['effort'])),key=lambda p:(p['loop']['batch'],p['loop']['effort'])):
 ps=list(ps);ls=[p['loop'] for p in ps];cs=[p['codex'] for p in ps];keys={z['key'] for z in ls};sh=[t for t in calls if t['key'] in keys and t['name']=='shell']
 print(g,len(ps),'delta',round(sum(z['wall'] for z in ls)-sum(z['wall'] for z in cs),3),'shell',sum(t['seconds'] for t in sh),'known',sum(t['command'] is not None for t in sh),'/',len(sh),'bytes L/C',sum(z['tool_bytes'] for z in ls),sum(z['cmd_bytes'] for z in cs),'repeats',sum(z['repeat_shells'] for z in ls),'tail',[(p['loop']['task'],p['loop']['rep'],round(p['loop']['wall'],1),p['loop']['shell_s']) for p in ps if p['tail']])
