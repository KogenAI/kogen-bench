"""shellwait setup on eu2 (run as lanes, under the research-shellwait host lock): run dir with the
replayconf clean route (harness, grader, loop source, GOCACHE snapshot, read boundary, attested loop-b8a4046,
Codex 0.165.0 fixed release dir), the yielding-shell experiment binary built from b8a4046 + shell-yield.diff,
the gateway extension with the run-dir path, a cli/go.mod-aware boundary probe and two measurement-only
receipts (receive-time shell timing, shell tool parameter names and tool items), and the three h2h-22
hard tasks qualified under the unchanged confirm5 rule."""
import datetime,hashlib,json,os,pathlib,shutil,sys,time
R=pathlib.Path(os.environ['SHELLWAIT_ROOT']).resolve()  # run root to create
RC=pathlib.Path(os.environ['REPLAYCONF_ROOT']).resolve()  # attested replayconf run root
EU_R=os.environ['EU_REPLAY_ROOT']  # run-root path string embedded in confirmation_ext.eu.py
TASKS=['kogen-review-on-demand','kogen-review-retry','kogen-shell-bound']  # LOOP-GAPS lever 4: the 3 h2h-22 tasks with shell tails
SRC=pathlib.Path(os.environ['TASKS_SRC']).resolve()  # task kits (private)
CODEX_DIR=pathlib.Path(os.environ['CODEX_BIN']).resolve().parent
ENV=dict(LANES_DIR=str(R/'grader'),PATH=os.environ['PATH'],GOMAXPROCS='2',GOPROXY='off',GOTOOLCHAIN='local')
LOOP_DEFAULT_SHA='611cbb9d47b3fb2e8e7cd9f3575ee7bd32f31e138b046bac73812b308865a817'
def save(p,d):p.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()

# Measurement-only additions to the frozen extension (plus the probe's module-file check).
TIMING='''
def timed_filtered(h,cmd,cwd,env,deadline_s,events_path,stderr,stdin,arm,out):
 """The harness's filtered_agent_run (lanes_bare.py 428-470, attested 9744637d) unchanged except that each
 line read from the agent's stdout is stamped on receipt: loop shell calls/results and Codex command_execution
 items go to shell-timing.jsonl (seconds since agent start). Measurement only; no filtering change."""
 import signal as _signal
 sidecar=os.path.join(out,'usage-events.jsonl');state={'size':0,'capped':False}
 usage_types={'message_end','agent_end','turn.completed','step_finish','message.updated','result','response','request.started','turn.started','turn.failed','session.started','tool.call','item.completed','error'}
 t0=time.monotonic();timing=open(os.path.join(out,'shell-timing.jsonl'),'w')
 def reader(pipe):
  with open(events_path,'wb') as saved,open(sidecar,'wb') as usage_saved:
   for line in iter(pipe.readline,b''):
    t=round(time.monotonic()-t0,3);keep=True
    try:
     event=json.loads(line);kind=event.get('type') or event.get('event')
     if arm=='pi' and (kind=='message_update' or kind=='tool_execution_update'):keep=False
     if kind in usage_types:usage_saved.write(line)
     it=event.get('item') or {}
     if kind in ('tool.call','tool.result') and event.get('name')=='shell':timing.write(json.dumps({'t':t,'event':kind,'id':event.get('call_id'),'kind':'loop-shell','time':event.get('time')})+'\\n');timing.flush()
     elif kind in ('item.started','item.completed') and it.get('type')=='command_execution':timing.write(json.dumps({'t':t,'event':kind,'id':it.get('id'),'kind':'codex-command','exit_code':it.get('exit_code')})+'\\n');timing.flush()
    except (ValueError,TypeError,AttributeError):pass
    if keep and not state['capped']:
     if state['size']+len(line)>h.EVENTS_CAP:state['capped']=True
     else:saved.write(line);state['size']+=len(line)
   pipe.close()
 proc=subprocess.Popen(cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=stderr,stdin=stdin,start_new_session=True)
 thread=threading.Thread(target=reader,args=(proc.stdout,),daemon=True);thread.start()
 timed_out=False
 try:proc.wait(timeout=deadline_s)
 except subprocess.TimeoutExpired:
  h.common._kill_group(proc);timed_out=True
 finally:thread.join()
 h.common._killpg(proc.pid,_signal.SIGKILL);timing.close()
 return proc.returncode,timed_out,state['capped'],sidecar

def record_items(g,body):
 """Tool items the client sends (new ones only) and the shell tool's parameter names: the activation witness."""
 try:
  seen=g.__dict__.setdefault('seen_items',set());rows=[]
  shell=[t.get('function',t) for t in body.get('tools',[]) if t.get('function',t).get('name')=='shell']
  rows.append({'request':len(g.rows)+1,'shell_params':sorted((shell[0].get('parameters') or {}).get('properties',{})) if shell else None})
  items=[]
  for x in body.get('input') or []:
   if isinstance(x,dict) and x.get('type') in ('function_call','custom_tool_call'):items.append(('call',x.get('call_id'),x.get('name'),x.get('arguments') or x.get('input')))
   if isinstance(x,dict) and x.get('type') in ('function_call_output','custom_tool_call_output'):
    o=x.get('output');items.append(('output',x.get('call_id'),None,o if isinstance(o,str) else json.dumps(o)))
  for m in body.get('messages') or []:
   for c in m.get('tool_calls') or []:items.append(('call',c.get('id'),c['function'].get('name'),c['function'].get('arguments')))
   if m.get('role')=='tool':
    o=m.get('content');items.append(('output',m.get('tool_call_id'),None,o if isinstance(o,str) else json.dumps(o)))
  for kind,cid,name,text in items:
   if (kind,cid) in seen:continue
   seen.add((kind,cid));text=text or ''
   rows.append({'kind':kind,'call_id':cid,'name':name,'arguments':text[:2000]} if kind=='call' else {'kind':kind,'call_id':cid,'head':text[:160],'bytes':len(text.encode())})
  with (g.out/'tool-items.jsonl').open('a') as f:f.write(''.join(json.dumps(r)+'\\n' for r in rows))
 except Exception as e:
  with (g.out/'tool-items.jsonl').open('a') as f:f.write(json.dumps({'record_error':type(e).__name__})+'\\n')

def install(h):'''
EDITS=[  # (old, new): each old must occur exactly once
 ("'workspace_readable':pathlib.Path('go.mod').is_file()","'workspace_readable':pathlib.Path('go.mod').is_file() or pathlib.Path('cli/go.mod').is_file()"),
 ("raw=self.rfile.read(n);row['client_request_bytes']=len(raw);body=json.loads(raw)","raw=self.rfile.read(n);row['client_request_bytes']=len(raw);body=json.loads(raw);record_items(g,body)"),
 ("t=time.monotonic();v=orig_filtered(cmd,cwd,env,effective_deadline,events,stderr,stdin,arm,out);STATE['agent_wall']=time.monotonic()-t",
  "t=time.monotonic();v=timed_filtered(h,cmd,cwd,env,effective_deadline,events,stderr,stdin,arm,out);STATE['agent_wall']=time.monotonic()-t"),
 ("\ndef install(h):",TIMING),
]

def setup():
 os.environ.update(ENV);sys.path.insert(0,str(R/'grader'))
 from lanes import common
 rc=json.loads((R/'replayconf-setup.json').read_text())
 ext=(R/'confirmation_ext.eu.py').read_text()
 assert sha(R/'confirmation_ext.eu.py')=='19c9755dd572750afd94f39d78b4d29dc8ec933377e77c3c7fc7fa1a79df7249' and ext.count(EU_R)==1
 ext=ext.replace(EU_R,str(R))
 for old,new in EDITS:
  assert ext.count(old)==1,old[:60];ext=ext.replace(old,new)
 (R/'confirmation_ext.py').write_text(ext)
 # The experiment binary: b8a4046 source (= the attested tree) + shell-yield.diff, built here with the
 # attested binary's settings (go 1.27.2 linux/amd64, CGO_ENABLED=1); unit tests ran before this setup.
 base_tree=common.sha256_tree(str(R/'build/base'),exclude=('.git','__pycache__'))
 here={'cache':common.sha256_tree(str(R/'cache-snapshot')),'grader_source':common.sha256_tree(str(R/'grader'),exclude=('.git','__pycache__')),'loop_source':common.sha256_tree(str(R/'source/kogen-loop'),exclude=('.git','__pycache__')),'harness':common.sha256_file(str(R/'harness/lanes_bare.py')),
  'binaries':{'loop-b8a4046':sha(R/'bin/loop-b8a4046'),'codex':sha(CODEX_DIR/'codex'),'codex-code-mode-host':sha(CODEX_DIR/'codex-code-mode-host')}}
 checks={k:here[k]==rc['here'][k] for k in ('cache','grader_source','loop_source','harness')}
 checks.update({'binary '+k:v==rc['here']['binaries'][k] for k,v in here['binaries'].items()})
 checks['loop-b8a4046 is 611cbb9d']=here['binaries']['loop-b8a4046']==LOOP_DEFAULT_SHA
 checks['patch base = attested loop source']=base_tree==here['loop_source']
 toolchains={'go':sha(shutil.which('go')),'node':sha(shutil.which('node')),'bwrap':sha('/usr/bin/bwrap')}
 checks.update({'toolchain '+k:v==rc['toolchains'][k] for k,v in toolchains.items()})
 (R/'tasks').mkdir(exist_ok=True)
 for t in TASKS:
  if not (R/'tasks'/t).exists():shutil.copytree(str(SRC/t),str(R/'tasks'/t),symlinks=True)
 save(R/'setup.json',{'utc':now(),'origin':'eu2 replayconf run dir (itself attested equal to the EU replay round); tasks from '+str(SRC),
  'extension_sha256':sha(R/'confirmation_ext.py'),'eu_extension_sha256':sha(R/'confirmation_ext.eu.py'),'extension_changes':['run dir path','boundary probe accepts cli/go.mod (kogen trees keep the module in cli/)','record_items: per-request shell tool parameter names and new tool items (measurement only)','timed_filtered: the harness reader copied with a receive-time stamp per line for shell calls / command items (measurement only; amendment 1, 20:5xZ: the first version tailed the block-buffered events file and saw bursts)'],
  'here':here,'toolchains':toolchains,'patch':{'diff_sha256':sha(R/'build/shell-yield.diff'),'base_tree_sha256':base_tree,'binary':'bin/scr-shell-yield-kogen-loop','binary_sha256':sha(R/'bin/scr-shell-yield-kogen-loop'),'build':'CGO_ENABLED=1 go build ./cmd/kogen-loop (go 1.27.2 linux/amd64, GOFLAGS=-p=1)','yield':'30s; session waits default 30 s, at most 300 s'},
  'tasks':{t:common.sha256_tree(str(R/'tasks'/t)) for t in TASKS},'equal':checks,'all_equal':all(checks.values())})
 print(json.dumps({'all_equal':all(checks.values()),'checks':checks}),flush=True)
 assert all(checks.values()),'copy differs from the replayconf attestation'

def qualify():
 os.environ.update(ENV);sys.path.insert(0,str(R/'grader'))
 from lanes import common,grading
 (R/'qualification').mkdir(exist_ok=True)
 rows=[]
 for name in TASKS:
  td=R/'tasks'/name;task=grading.load_task(str(td))
  entry={'task':name,'source':str(SRC/name),'tree_sha256':common.sha256_tree(str(td)),'runs':{},'utc':now()}
  expected=set(task['eval'].get('expected',{}).get('requested',[])+task['eval'].get('expected',{}).get('regression',[]))
  requested=task['eval'].get('expected',{}).get('requested',[])
  overlays=['reference']+['wrong/'+p.name for p in sorted((td/'wrong').iterdir()) if p.is_dir()]
  for overlay in overlays:
   t=time.monotonic()
   with grading.scratch(str(td),overlay,export=True) as tree:
    result=grading.evaluate_tree(task,tree)
   save(R/'qualification'/(name+'--'+overlay.replace('/','-')+'.json'),result)
   # The confirm5 wider-round rule (prepare_wide.py), unchanged.
   passed=(bool(expected) and result['all_passed'] and not result['infrastructure'] and set(result['observed_ids'])==expected) if overlay=='reference' else (not result['infrastructure'] and any(result['ids'].get(i)=='failed' for i in requested))
   missing=sorted(expected-set(result.get('observed_ids',[])))[:5];extra=sorted(set(result.get('observed_ids',[]))-expected)[:5]
   entry['runs'][overlay]={'qualifies':bool(passed),'all_passed':result['all_passed'],'infrastructure':result['infrastructure'],'wall_s':round(time.monotonic()-t,3),'observed_ids':len(result.get('observed_ids',[])),'missing_ids':missing,'unexpected_ids':extra}
   print(json.dumps({'qualification':name,'overlay':overlay,**entry['runs'][overlay]}),flush=True)
   if overlay=='reference' and not passed:break
  entry['qualified']=len(overlays)>1 and len(entry['runs'])==len(overlays) and all(x['qualifies'] for x in entry['runs'].values())
  rows.append(entry)
 save(R/'eligibility.json',rows)
 print(json.dumps({'qualified':[r['task'] for r in rows if r['qualified']],'not_qualified':[r['task'] for r in rows if not r['qualified']]}),flush=True)

if __name__=='__main__':
 {'setup':setup,'qualify':qualify}[sys.argv[1]]()
